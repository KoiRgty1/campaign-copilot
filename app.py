import os
import json
import streamlit as st
from openai import OpenAI

# 1. 初始化页面配置（必须放在 Streamlit 代码的最顶部）
st.set_page_config(page_title="AI 运营人群圈选助手", layout="wide")

# 模拟数据源
data = [
    {"user_id": "U2001", "is_new": True, "behavior": "none", "is_promotion_buyer": False},
    {"user_id": "U2002", "is_new": False, "behavior": "browse", "is_promotion_buyer": False},
    {"user_id": "U2003", "is_new": False, "behavior": "none", "is_promotion_buyer": True},
    {"user_id": "U2004", "is_new": True, "behavior": "browse", "is_promotion_buyer": False},
    {"user_id": "U2005", "is_new": False, "behavior": "browse", "is_promotion_buyer": True},
]

def filter_audience(audience_feature):
    # 默认兜底返回结构
    fallback_response = {
        "status": "fallback",
        "message": "没能完全理解您的指令，您是不是想找：",
        "suggestions": ["近2周新客", "近30天浏览未购"],
        "data": []
    }

    # 优先从环境变量读取，没有则直接使用你提供的明文 Key
    api_key = os.environ.get("NVAPI_KEY", "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")
    
    # 【修复硬伤】：只有当没有配置任何 Key 时才拦截
    if not api_key or api_key.strip() == "":
        print("❌ 警告: 未配置有效的 NVIDIA API Key，触发前端兜底策略。")
        return fallback_response

    try:
        client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=api_key
        )

        system_prompt = """
        你是一个电商数据分析专家。请解析运营人员输入的人群圈选指令，并严格转化为结构化的 JSON 格式。
        
        你必须输出且只能输出以下四个字段，不要包含任何 Markdown 格式（如 ```json）或多余解释：
        - is_new: [true, false, "all"] (提到"新客"、"注册未购"设为 true，否则默认为 "all")
        - time_range_days: 整数 (如"近2周"为14，"近30天"为30，"近1年"/"进1年"为365，未提到默认为 -1)
        - behavior: ["browse", "purchase", "all"] (提到"浏览"设为 "browse"，未提到默认为 "all")
        - is_promotion_buyer: [true, false] (提到"大促"、"活动"、"节假日"设为 true，否则为 false)
        
        【重要容错规则】
        1. 必须具备错别字纠错能力（例如输入"进1年"应等同于"近1年"，将其 time_range_days 解析为 365）。
        2. 如果输入的文本完全不包含上述任何维度的特征（如输入"哈哈"或"大白菜"），请将所有字段设为 "all" 或 false。
        """

        completion = client.chat.completions.create(
            model="meta/llama-3.2-3b-instruct",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": audience_feature}
            ],
            temperature=0.1,
            max_tokens=150,
            timeout=7.0  # 设置超时防止无限死等
        )
        
        response_text = completion.choices[0].message.content.strip()
        slots = json.loads(response_text)
        print(f"💡 [NVIDIA AI 语义解析成功]: {slots}")

        # 判断是否完全没有匹配到任何有效特征
        is_empty_intent = (
            slots.get("is_new") == "all" and 
            slots.get("time_range_days") == -1 and 
            slots.get("behavior") == "all" and 
            slots.get("is_promotion_buyer") is False
        )
        
        if is_empty_intent:
            return fallback_response

        # 数据过滤逻辑
        filtered_users = []
        for user in data:
            if slots["is_new"] != "all" and user.get("is_new") != slots["is_new"]:
                continue
            if slots["behavior"] != "all" and user.get("behavior") != slots["behavior"]:
                continue
            if slots["is_promotion_buyer"] and not user.get("is_promotion_buyer"):
                continue
            filtered_users.append(user)

        # 按 user_id 去重机制
        unique_users = {}
        for user in filtered_users:
            user_id = user.get("user_id")
            if user_id:
                unique_users[user_id] = user
        
        return {
            "status": "success",
            "message": "圈选成功",
            "suggestions": [],
            "data": list(unique_users.values())
        }

    except Exception as e:
        print(f"❌ AI 解析失败或发生异常: {e}")
        return fallback_response

# ==========================================
# 🛠️ STREAMLIT 前端 UI 渲染部分（为你补齐的代码）
# ==========================================

st.title("AI驱动的智能营销系统，一键实现人群圈选、营销短信文案")
st.caption("基于 NVIDIA NIM (Llama-3.2-3b-instruct) 语义解析架构")
st.markdown("---")

# 初始化 Streamlit 的 Session State，用于处理点击气泡时的输入框文本联动
if "input_val" not in st.session_state:
    st.session_state["input_val"] = ""
if "api_result" not in st.session_state:
    st.session_state["api_result"] = None

# 定义点击推荐标签时的回调事件
def click_tag(tag_text):
    st.session_state["input_val"] = tag_text
    # 自动执行查询
    st.session_state["api_result"] = filter_audience(tag_text)

# 用户输入区
audience_input = st.text_input(
    "请输入您的人群圈选指令：", 
    value=st.session_state["input_val"],
    placeholder="例如：帮我圈选出进1年大促人群 / 近30天浏览未购客群",
    key="audience_input_key"
)

# 当用户手动打字输入更新时，同步更新状态
if audience_input != st.session_state["input_val"]:
    st.session_state["input_val"] = audience_input

if st.button("开始分析并圈选", type="primary"):
    if st.session_state["input_val"].strip() == "":
        st.warning("请输入指令后再提交哦！")
    else:
        with st.spinner("AI 正在解析多意图业务语义并切分底层数据集..."):
            st.session_state["api_result"] = filter_audience(st.session_state["input_val"])

# 展示区
if st.session_state["api_result"]:
    result = st.session_state["api_result"]
    
    # 💡 核心亮点：当前端收到 fallback 状态时的交互优化策略
    if result["status"] == "fallback":
        st.write("") # 留空增加视觉间隔
        # 用 info 气泡展示友好提示
        st.info(f"💡 {result['message']}")
        
        # 横向并排渲染可点击的推荐标签按钮
        cols = st.columns(len(result["suggestions"]) + 4)
        for idx, tag in enumerate(result["suggestions"]):
            with cols[idx]:
                st.button(f"👉 {tag}", key=f"tag_{idx}", on_click=click_tag, args=(tag,))
                
    elif result["status"] == "success":
        st.success(f"✅ {result['message']}！共圈选出 {len(result['data'])} 条符合特征的用户数据。")
        if len(result["data"]) > 0:
            st.dataframe(result["data"], use_container_width=True)
        else:
            st.info("大模型已成功解析标签，但当前数据库中未检索到完全匹配此特征的用户。")
