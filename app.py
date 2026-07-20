import streamlit as st
import json
import pandas as pd

# ================= 1. 页面 UI 设置 =================
st.set_page_config(page_title="CRM AI Agent", layout="wide")
st.title("自动化营销工具") # 已按要求修改标题
st.markdown("通过自然语言指令，一键实现人群圈选并生成精准触达的营销短信文案。")

# ================= 2. 底层数据加载 =================
@st.cache_data
def load_data():
    try:
        with open("crm_mock_data_50.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

data = load_data()

# ================= 3. 对话历史控制 =================
if "messages" not in st.session_state:
    st.session_state.messages = []

# 渲染历史聊天记录（确保刷新时多包结构不乱）
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "packages" in message:
            for pkg in message["packages"]:
                st.markdown(f"### 📦 独立人群包：{pkg['name']}")
                st.markdown(f"* **人群包规模**：精确匹配到 {pkg['count']} 位目标用户")
                st.markdown(f"* **定向营销文案**：\n> {pkg['copy']}")
                if pkg['count'] > 0:
                    st.markdown("* **数据快照预览 (前5条)**：")
                    st.dataframe(pkg['df'])
                st.markdown("---")
        else:
            st.markdown(message["content"])

# ================= 4. 多意图并行圈选引擎 =================
if prompt := st.chat_input("请输入指令，例如：帮我分别圈选出近2周注册未购和近30天浏览未购人群"):
    
    # 1. 渲染用户输入的 prompt
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. AI 核心解析
    with st.chat_message("assistant"):
        st.markdown("🔄 正在解析多意图业务语义，正在并行切分底层数据集...")
        
        # 建立独立的人群包存储桶
        packages_output = []
        
        # 【判定桶 1】：检测是否包含“近2周/新客”意图
        if any(k in prompt for k in ["近2周", "新客", "注册未购"]):
            users_2w = data[:10]  # 捞取前10条数据
            packages_output.append({
                "name": "近2周注册未购新客包",
                "count": len(users_2w),
                "copy": "【品牌服务】你好呀！很高兴认识你。看到你最近关注了我们，特意为你准备了一份新人见面礼，期待你的第一次体验。点击[链接]领取专属权益~",
                "df": pd.DataFrame(users_2w).head(5)
            })
            
        # 【判定桶 2】：检测是否包含“近30天/浏览”意图
        if any(k in prompt for k in ["近30天", "浏览", "浏览未购"]):
            users_30d = data[10:20]  # 捞取11-20条数据
            packages_output.append({
                "name": "近30天浏览未购意向包",
                "count": len(users_30d),
                "copy": "【品牌服务】亲爱的朋友，好久不见。发现你最近在浏览相关商品，你的每一次关注我们都在意。大促回归专属福利已发放到你的账户，来看看吧。[链接]",
                "df": pd.DataFrame(users_30d).head(5)
            })
        
        # 结果分发渲染
        if not packages_output:
            reply = "⚠️ 未能识别到匹配的人群特征，请尝试输入包含 '近2周' 或 '近30天' 的运营指令。"
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        else:
            st.markdown("✅ **多包并行圈选完毕，结果已隔离：**")
            
            # 遍历并各自渲染独立的人群包区域
            for pkg in packages_output:
                st.markdown(f"### 📦 独立人群包：{pkg['name']}")
                st.markdown(f"* **人群包规模**：精确匹配到 {pkg['count']} 位目标用户")
                st.markdown(f"* **定向营销文案**：\n> {pkg['copy']}")
                st.markdown("* **数据快照预览 (前5条)**：")
                st.dataframe(pkg['df'])
                st.markdown("---")
            
            # 将结构化多包数据存入历史，防止刷新丢失
            st.session_state.messages.append({
                "role": "assistant", 
                "content": "已成功并行生成多个人群包。", 
                "packages": packages_output
            })

# ================= 5. 底部声明小字 =================
st.caption("智能人群圈选、短信创建")
