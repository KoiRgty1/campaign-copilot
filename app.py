import streamlit as st
import json
import pandas as pd

# ================= 1. 页面 UI 设置 =================
st.set_page_config(page_title="CRM AI Agent", layout="wide")
st.title("🚀 Campaign Copilot: 智能对话式运营指挥舱")
st.markdown("通过自然语言指令，一键实现人群圈选与带有人文关怀的智能文案生成。")

# ================= 2. 底层数据加载 =================
@st.cache_data
def load_data():
    try:
        with open("crm_mock_data_50.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

data = load_data()

# ================= 3. 核心业务逻辑 (已修复 Bug) =================
def filter_audience(audience_feature):
    """
    根据输入的人群特征筛选用户
    支持特征：近2周新客/注册未购、近30天浏览未购等
    """
    # 默认返回空数组，无法识别指令时返回0条
    filtered_users = []
    
    # 提取模拟数据：前10条为近2周，接下来10条为近30天
    new_customer_2w = data[:10]  
    browse_30d = data[10:20] 
    
    # 强化关键词解析
    if any(keyword in audience_feature for keyword in ["近2周", "新客", "注册未购"]):
        filtered_users.extend(new_customer_2w)
    
    if any(keyword in audience_feature for keyword in ["近30天", "浏览", "浏览未购"]):
        filtered_users.extend(browse_30d)
    
    # 按user_id去重，确保无重复用户
    unique_users = {}
    for user in filtered_users:
        user_id = user.get("user_id") 
        if user_id:  
            unique_users[user_id] = user
            
    return list(unique_users.values())

def generate_marketing_copy(count, prompt_text):
    """根据人群特征和规模，生成具备场景感知和信任构建的营销文案"""
    if count == 0:
        return "未能识别到匹配的人群，请尝试调整查询指令（例如：帮我圈出近2周注册新客）。"
    
    if "新客" in prompt_text or "2周" in prompt_text:
        return "【品牌服务】你好呀！很高兴认识你。看到你最近关注了我们，特意为你准备了一份新人见面礼，期待你的第一次体验。点击[链接]领取专属权益~"
    else:
        return "【品牌服务】亲爱的朋友，好久不见。发现你最近在浏览相关商品，你的每一次关注我们都在意。大促回归专属福利已发放到你的账户，来看看吧。[链接]"

# ================= 4. 对话工作流渲染 =================
# 初始化对话历史记录
if "messages" not in st.session_state:
    st.session_state.messages = []

# 在页面上渲染之前的聊天记录
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # 如果历史记录里包含表格，也一并渲染出来
        if "table_data" in message:
            st.dataframe(message["table_data"])

# 监听用户底部的输入框
if prompt := st.chat_input("请输入指令，例如：帮我圈出近2周注册新客，并生成文案"):
    
    # 1. 把用户的话显示在屏幕上
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. AI 开始工作
    with st.chat_message("assistant"):
        st.markdown("🔄 正在解析业务语义并执行底层数据库圈选...")
        
        # 执行筛选和文案生成逻辑
        result_users = filter_audience(prompt)
        count = len(result_users)
        copywriting = generate_marketing_copy(count, prompt)
        
        # 构建回复内容
        reply_content = f"✅ **执行完毕**\n* **人群包规模**：精确匹配到 {count} 位目标用户\n* **智能营销文案**：\n> {copywriting}"
        st.markdown(reply_content)
        
        # 如果有数据，展示前5条预览
        if count > 0:
            st.markdown("* **底层数据快照 (前5条预览)**：")
            df = pd.DataFrame(result_users).head(5)
            st.dataframe(df)
            # 保存到 session state
            st.session_state.messages.append({"role": "assistant", "content": reply_content, "table_data": df})
        else:
            st.session_state.messages.append({"role": "assistant", "content": reply_content})
