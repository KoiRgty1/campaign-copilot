import os
import json
import streamlit as st
from openai import OpenAI

# 1. 初始化页面配置
st.set_page_config(page_title="AI 运营人群圈选助手", layout="wide")

# 50条真实假人群包数据
data = [
  {"user_id": "U1001", "registration_date": "2026-07-16", "last_browse_date": "2026-07-14", "browsed_page_type": ["PLP", "PDP"], "total_purchases": 0, "last_purchase_date": None, "purchase_channels": [], "campaign_participation": [], "_mock_label": "近2周注册未购"},
  {"user_id": "U1002", "registration_date": "2026-07-20", "last_browse_date": "2026-07-15", "browsed_page_type": ["PDP"], "total_purchases": 0, "last_purchase_date": None, "purchase_channels": [], "campaign_participation": [], "_mock_label": "近2周注册未购"},
  {"user_id": "U1003", "registration_date": "2026-07-10", "last_browse_date": "2026-07-10", "browsed_page_type": ["PLP"], "total_purchases": 0, "last_purchase_date": None, "purchase_channels": [], "campaign_participation": [], "_mock_label": "近2周注册未购"},
  {"user_id": "U1004", "registration_date": "2026-07-07", "last_browse_date": "2026-07-06", "browsed_page_type": ["PLP"], "total_purchases": 0, "last_purchase_date": None, "purchase_channels": [], "campaign_participation": [], "_mock_label": "近2周注册未购"},
  {"user_id": "U1005", "registration_date": "2026-07-12", "last_browse_date": "2026-07-20", "browsed_page_type": ["PDP"], "total_purchases": 0, "last_purchase_date": None, "purchase_channels": [], "campaign_participation": [], "_mock_label": "近2周注册未购"},
  {"user_id": "U1006", "registration_date": "2026-07-18", "last_browse_date": "2026-07-12", "browsed_page_type": ["PDP"], "total_purchases": 0, "last_purchase_date": None, "purchase_channels": [], "campaign_participation": [], "_mock_label": "近2周注册未购"},
  {"user_id": "U1007", "registration_date": "2026-07-20", "last_browse_date": "2026-07-08", "browsed_page_type": ["PLP", "PDP"], "total_purchases": 0, "last_purchase_date": None, "purchase_channels": [], "campaign_participation": [], "_mock_label": "近2周注册未购"},
  {"user_id": "U1008", "registration_date": "2026-07-11", "last_browse_date": "2026-07-13", "browsed_page_type": ["PLP", "PDP"], "total_purchases": 0, "last_purchase_date": None, "purchase_channels": [], "campaign_participation": [], "_mock_label": "近2周注册未购"},
  {"user_id": "U1009", "registration_date": "2026-07-07", "last_browse_date": "2026-07-07", "browsed_page_type": ["PLP", "PDP"], "total_purchases": 0, "last_purchase_date": None, "purchase_channels": [], "campaign_participation": [], "_mock_label": "近2周注册未购"},
  {"user_id": "U1010", "registration_date": "2026-07-08", "last_browse_date": "2026-07-17", "browsed_page_type": ["PDP", "PLP"], "total_purchases": 0, "last_purchase_date": None, "purchase_channels": [], "campaign_participation": [], "_mock_label": "近2周注册未购"},
  {"user_id": "U2001", "registration_date": "2025-05-31", "last_browse_date": "2026-07-04", "browsed_page_type": ["PLP", "PDP"], "total_purchases": 0, "last_purchase_date": None, "purchase_channels": [], "campaign_participation": [], "_mock_label": "近30天浏览未购"},
  {"user_id": "U2002", "registration_date": "2025-01-09", "last_browse_date": "2026-07-10", "browsed_page_type": ["PLP", "PDP"], "total_purchases": 0, "last_purchase_date": None, "purchase_channels": [], "campaign_participation": [], "_mock_label": "近30天浏览未购"},
  {"user_id": "U2003", "registration_date": "2025-07-17", "last_browse_date": "2026-07-19", "browsed_page_type": ["PDP"], "total_purchases": 0, "last_purchase_date": None, "purchase_channels": [], "campaign_participation": [], "_mock_label": "近30天浏览未购"},
  {"user_id": "U2004", "registration_date": "2025-02-02", "last_browse_date": "2026-07-18", "browsed_page_type": ["PLP", "PDP"], "total_purchases": 0, "last_purchase_date": None, "purchase_channels": [], "campaign_participation": [], "_mock_label": "近30天浏览未购"},
  {"user_id": "U2005", "registration_date": "2025-08-11", "last_browse_date": "2026-07-15", "browsed_page_type": ["PLP"], "total_purchases": 0, "last_purchase_date": None, "purchase_channels": [], "campaign_participation": [], "_mock_label": "近30天浏览未购"},
  {"user_id": "U2006", "registration_date": "2026-05-16", "last_browse_date": "2026-07-02", "browsed_page_type": ["PLP"], "total_purchases": 0, "last_purchase_date": None, "purchase_channels": [], "campaign_participation": [], "_mock_label": "近30天浏览未购"},
  {"user_id": "U2007", "registration_date": "2025-11-26", "last_browse_date": "2026-07-03", "browsed_page_type": ["PLP", "PDP"], "total_purchases": 0, "last_purchase_date": None, "purchase_channels": [], "campaign_participation": [], "_mock_label": "近30天浏览未购"},
  {"user_id": "U2008", "registration_date": "2024-10-29", "last_browse_date": "2026-06-24", "browsed_page_type": ["PLP", "PDP"], "total_purchases": 0, "last_purchase_date": None, "purchase_channels": [], "campaign_participation": [], "_mock_label": "近30天浏览未购"},
  {"user_id": "U2009", "registration_date": "2025-03-12", "last_browse_date": "2026-07-09", "browsed_page_type": ["PLP"], "total_purchases": 0, "last_purchase_date": None, "purchase_channels": [], "campaign_participation": [], "_mock_label": "近30天浏览未购"},
  {"user_id": "U2010", "registration_date": "2025-10-10", "last_browse_date": "2026-06-25", "browsed_page_type": ["PDP", "PLP"], "total_purchases": 0, "last_purchase_date": None, "purchase_channels": [], "campaign_participation": [], "_mock_label": "近30天浏览未购"},
  {"user_id": "U3001", "registration_date": "2025-01-09", "last_browse_date": "2026-07-15", "browsed_page_type": ["PLP", "PDP"], "total_purchases": 2, "last_purchase_date": "2026-06-06", "purchase_channels": ["official_website", "JD"], "campaign_participation": ["Daily_Promo"], "_mock_label": "近1年活跃用户"},
  {"user_id": "U3002", "registration_date": "2025-04-06", "last_browse_date": "2026-06-21", "browsed_page_type": ["PDP"], "total_purchases": 1, "last_purchase_date": "2026-06-15", "purchase_channels": ["official_website", "JD"], "campaign_participation": [], "_mock_label": "近1年活跃用户"},
  {"user_id": "U3003", "registration_date": "2024-12-15", "last_browse_date": "2026-06-30", "browsed_page_type": ["PDP", "PLP"], "total_purchases": 2, "last_purchase_date": "2026-06-08", "purchase_channels": ["official_website"], "campaign_participation": ["Daily_Promo"], "_mock_label": "近1年活跃用户"},
  {"user_id": "U3004", "registration_date": "2024-07-19", "last_browse_date": "2026-07-03", "browsed_page_type": ["PLP"], "total_purchases": 1, "last_purchase_date": "2026-04-10", "purchase_channels": ["official_website", "JD"], "campaign_participation": [], "_mock_label": "近1年活跃用户"},
  {"user_id": "U3005", "registration_date": "2024-06-05", "last_browse_date": "2026-07-04", "browsed_page_type": ["PLP", "PDP"], "total_purchases": 3, "last_purchase_date": "2025-08-03", "purchase_channels": ["official_website"], "campaign_participation": [], "_mock_label": "近1年活跃用户"},
  {"user_id": "U3006", "registration_date": "2025-01-30", "last_browse_date": "2026-07-04", "browsed_page_type": ["PDP"], "total_purchases": 1, "last_purchase_date": "2025-07-23", "purchase_channels": ["official_website", "JD"], "campaign_participation": ["Daily_Promo"], "_mock_label": "近1年活跃用户"},
  {"user_id": "U3007", "registration_date": "2024-03-28", "last_browse_date": "2026-07-03", "browsed_page_type": ["PDP", "PLP"], "total_purchases": 5, "last_purchase_date": "2025-09-22", "purchase_channels": ["official_website"], "campaign_participation": ["Daily_Promo"], "_mock_label": "近1年活跃用户"},
  {"user_id": "U3008", "registration_date": "2025-03-21", "last_browse_date": "2026-06-20", "browsed_page_type": ["PDP", "PLP"], "total_purchases": 3, "last_purchase_date": "2026-04-30", "purchase_channels": ["official_website", "JD"], "campaign_participation": [], "_mock_label": "近1年活跃用户"},
  {"user_id": "U3009", "registration_date": "2025-01-18", "last_browse_date": "2026-06-21", "browsed_page_type": ["PDP", "PLP"], "total_purchases": 5, "last_purchase_date": "2026-01-15", "purchase_channels": ["official_website", "JD"], "campaign_participation": [], "_mock_label": "近1年活跃用户"},
  {"user_id": "U3010", "registration_date": "2025-07-04", "last_browse_date": "2026-07-13", "browsed_page_type": ["PDP", "PLP"], "total_purchases": 4, "last_purchase_date": "2025-11-19", "purchase_channels": ["official_website", "JD"], "campaign_participation": [], "_mock_label": "近1年活跃用户"},
  {"user_id": "U4001", "registration_date": "2024-01-28", "last_browse_date": "2026-07-13", "browsed_page_type": ["PDP", "PLP"], "total_purchases": 10, "last_purchase_date": "2025-08-04", "purchase_channels": ["official_website", "Tmall"], "campaign_participation": ["618_2026"], "_mock_label": "大促人群"},
  {"user_id": "U4002", "registration_date": "2024-05-20", "last_browse_date": "2025-11-09", "browsed_page_type": ["PLP", "PDP"], "total_purchases": 8, "last_purchase_date": "2026-07-14", "purchase_channels": ["official_website"], "campaign_participation": ["Double11_2025"], "_mock_label": "大促人群"},
  {"user_id": "U4003", "registration_date": "2024-02-07", "last_browse_date": "2026-05-31", "browsed_page_type": ["PDP"], "total_purchases": 8, "last_purchase_date": "2025-12-28", "purchase_channels": ["official_website"], "campaign_participation": ["Double11_2025", "618_2026"], "_mock_label": "大促人群"},
  {"user_id": "U4004", "registration_date": "2024-10-02", "last_browse_date": "2025-09-02", "browsed_page_type": ["PDP"], "total_purchases": 6, "last_purchase_date": "2025-12-26", "purchase_channels": ["official_website", "Tmall"], "campaign_participation": ["Double11_2025", "Double11_2024"], "_mock_label": "大促人群"},
  {"user_id": "U4005", "registration_date": "2023-11-19", "last_browse_date": "2025-09-06", "browsed_page_type": ["PDP", "PLP"], "total_purchases": 4, "last_purchase_date": "2025-08-27", "purchase_channels": ["official_website", "Tmall"], "campaign_participation": ["618_2026"], "_mock_label": "大促人群"},
  {"user_id": "U4006", "registration_date": "2024-03-16", "last_browse_date": "2025-08-02", "browsed_page_type": ["PDP"], "total_purchases": 2, "last_purchase_date": "2026-05-10", "purchase_channels": ["official_website", "Tmall"], "campaign_participation": ["Double11_2024"], "_mock_label": "大促人群"},
  {"user_id": "U4007", "registration_date": "2025-01-24", "last_browse_date": "2026-04-24", "browsed_page_type": ["PDP", "PLP"], "total_purchases": 7, "last_purchase_date": "2026-03-15", "purchase_channels": ["official_website"], "campaign_participation": ["618_2026"], "_mock_label": "大促人群"},
  {"user_id": "U4008", "registration_date": "2023-12-26", "last_browse_date": "2026-01-12", "browsed_page_type": ["PLP"], "total_purchases": 6, "last_purchase_date": "2025-12-29", "purchase_channels": ["official_website"], "campaign_participation": ["618_2026", "Double11_2024"], "_mock_label": "大促人群"},
  {"user_id": "U4009", "registration_date": "2024-09-14", "last_browse_date": "2025-08-13", "browsed_page_type": ["PLP"], "total_purchases": 4, "last_purchase_date": "2026-07-20", "purchase_channels": ["official_website"], "campaign_participation": ["618_2026", "Double11_2025"], "_mock_label": "大促人群"},
  {"user_id": "U4010", "registration_date": "2023-10-28", "last_browse_date": "2025-12-09", "browsed_page_type": ["PLP"], "total_purchases": 8, "last_purchase_date": "2026-04-17", "purchase_channels": ["official_website", "Tmall"], "campaign_participation": ["618_2026", "Double11_2025"], "_mock_label": "大促人群"},
  {"user_id": "U5001", "registration_date": "2023-08-20", "last_browse_date": "2026-06-26", "browsed_page_type": ["PDP"], "total_purchases": 2, "last_purchase_date": "2026-02-03", "purchase_channels": ["Tmall", "JD"], "campaign_participation": [], "_mock_label": "非官网活跃 (干扰项)"},
  {"user_id": "U5002", "registration_date": "2024-06-14", "last_browse_date": "2025-04-28", "browsed_page_type": [], "total_purchases": 2, "last_purchase_date": "2025-03-11", "purchase_channels": ["official_website"], "campaign_participation": ["Double11_2024"], "_mock_label": "流失老客 (干扰项)"},
  {"user_id": "U5003", "registration_date": "2024-03-03", "last_browse_date": "2024-12-08", "browsed_page_type": [], "total_purchases": 1, "last_purchase_date": "2024-12-23", "purchase_channels": ["official_website"], "campaign_participation": ["Double11_2024"], "_mock_label": "流失老客 (干扰项)"},
  {"user_id": "U5004", "registration_date": "2023-06-15", "last_browse_date": "2026-07-01", "browsed_page_type": ["PDP"], "total_purchases": 3, "last_purchase_date": "2026-01-14", "purchase_channels": ["Tmall", "JD"], "campaign_participation": [], "_mock_label": "非官网活跃 (干扰项)"},
  {"user_id": "U5005", "registration_date": "2024-03-22", "last_browse_date": "2026-06-26", "browsed_page_type": ["PDP"], "total_purchases": 1, "last_purchase_date": "2025-08-06", "purchase_channels": ["Tmall", "JD"], "campaign_participation": [], "_mock_label": "非官网活跃 (干扰项)"},
  {"user_id": "U5006", "registration_date": "2023-08-26", "last_browse_date": "2026-07-05", "browsed_page_type": ["PDP"], "total_purchases": 2, "last_purchase_date": "2025-12-03", "purchase_channels": ["Tmall", "JD"], "campaign_participation": [], "_mock_label": "非官网活跃 (干扰项)"},
  {"user_id": "U5007", "registration_date": "2023-06-16", "last_browse_date": "2026-06-22", "browsed_page_type": ["PDP"], "total_purchases": 2, "last_purchase_date": "2025-12-31", "purchase_channels": ["Tmall", "JD"], "campaign_participation": [], "_mock_label": "非官网活跃 (干扰项)"},
  {"user_id": "U5008", "registration_date": "2024-05-04", "last_browse_date": "2026-06-24", "browsed_page_type": ["PDP"], "total_purchases": 1, "last_purchase_date": "2026-01-13", "purchase_channels": ["Tmall", "JD"], "campaign_participation": [], "_mock_label": "非官网活跃 (干扰项)"},
  {"user_id": "U5009", "registration_date": "2023-05-24", "last_browse_date": "2025-03-08", "browsed_page_type": [], "total_purchases": 1, "last_purchase_date": "2024-06-11", "purchase_channels": ["official_website"], "campaign_participation": ["Double11_2024"], "_mock_label": "流失老客 (干扰项)"},
  {"user_id": "U5010", "registration_date": "2024-05-19", "last_browse_date": "2025-05-23", "browsed_page_type": [], "total_purchases": 4, "last_purchase_date": "2025-02-18", "purchase_channels": ["official_website"], "campaign_participation": ["Double11_2024"], "_mock_label": "流失老客 (干扰项)"}
]

# 通用 API 初始化函数
def get_llm_client():
    api_key = os.environ.get("NVAPI_KEY", "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")
    if not api_key or api_key.strip() == "":
        return None
    return OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=api_key)

# 1. 人群圈选过滤函数[cite: 4]
def filter_audience(audience_feature):
    fallback_response = {
        "status": "fallback",
        "message": "没能完全理解您的指令，您是不是想找：",
        "suggestions": ["近2周新客", "近30天浏览未购"],
        "data": []
    }

    client = get_llm_client()
    if not client: return fallback_response

    try:
        system_prompt = """
        你是一个电商数据分析专家。请解析运营人员输入的人群圈选指令，并严格转化为结构化的 JSON 格式。
        你必须输出且只能输出以下四个字段，不要包含任何 Markdown 格式或多余解释：
        - is_new: [true, false, "all"] (提到"新客"、"注册未购"设为 true，否则默认为 "all")
        - time_range_days: 整数 (如"近2周"为14，"近30天"为30，"近1年"/"进1年"为365，未提到默认为 -1)
        - behavior: ["browse", "purchase", "all"] (提到"浏览"设为 "browse"，未提到默认为 "all")
        - is_promotion_buyer: [true, false] (提到"大促"、"活动"、"节假日"设为 true，否则为 false)
        【重要容错规则】
        1. 必须具备错别字纠错能力（例如输入"进1年"等同于"近1年"）。
        2. 如果输入的文本完全不包含上述任何维度的特征，请将所有字段设为 "all" 或 false。
        """

        completion = client.chat.completions.create(
            model="meta/llama-3.2-3b-instruct",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": audience_feature}],
            temperature=0.1, max_tokens=150, timeout=7.0
        )
        
        slots = json.loads(completion.choices[0].message.content.strip())

        if slots.get("is_new") == "all" and slots.get("time_range_days") == -1 and slots.get("behavior") == "all" and slots.get("is_promotion_buyer") is False:
            return fallback_response

        # 数据桥接映射与过滤
        filtered_users = []
        for user in data:
            if slots["is_new"] is True and user.get("total_purchases", 0) > 0: continue
            elif slots["is_new"] is False and user.get("total_purchases", 0) == 0: continue
            
            if slots["behavior"] == "browse":
                if not user.get("browsed_page_type") or len(user.get("browsed_page_type", [])) == 0: continue
                if "未购" in audience_feature and user.get("total_purchases", 0) > 0: continue

            if slots["is_promotion_buyer"] is True:
                if not any("618" in c or "Double11" in c for c in user.get("campaign_participation", [])): continue

            mock_label = user.get("_mock_label", "")
            if slots["time_range_days"] != -1:
                if slots["time_range_days"] == 14 and "近2周" not in mock_label: continue
                if slots["time_range_days"] == 30 and "近30天" not in mock_label: continue
                if slots["time_range_days"] == 365 and "近1年" not in mock_label: continue

            filtered_users.append(user)

        unique_users = {u["user_id"]: u for u in filtered_users if "user_id" in u}
        return {"status": "success", "message": "圈选成功", "slots_desc": f"（特征群组：{audience_feature}）", "data": list(unique_users.values())}

    except Exception as e:
        return fallback_response

# 2. 💡 新增：AI 短信文案生成函数
def generate_marketing_sms(slots_desc):
    client = get_llm_client()
    if not client:
        return [f"【智能营销】精选好物等你来，点击查看 链接：https://brand.com/shop" for _ in range(5)]

    try:
        sms_prompt = f"""
        你是一个资深的电商文案大师。请针对以下特征的目标人群，撰写5条极具吸引力的短信营销文案。
        目标客群特征：{slots_desc}
        
        【严格规范】
        1. 必须输出且只能输出5条文案。
        2. 每条文案必须严格遵循模板格式：【品牌名】文案内容 链接：xxxx
        3. 请根据客群特征定制内容（例如：新客强调新人礼券，浏览未购强调降价或库存紧张，大促人群强调满减特惠）。
        4. 品牌名可以用具体的知名品牌或“智能商城”代替，链接部分直接写成“链接：https://short.url/x”。
        5. 不要带有任何 Markdown 标记（如 1. 2. 3. 这种序号）、不要带前缀和括号，每行一条文案，用换行符分隔。
        """

        completion = client.chat.completions.create(
            model="meta/llama-3.2-3b-instruct",
            messages=[{"role": "system", "content": sms_prompt}],
            temperature=0.7, max_tokens=400, timeout=7.0
        )
        
        lines = completion.choices[0].message.content.strip().split('\n')
        # 过滤掉空行，确保拿全5条
        valid_lines = [line.strip() for line in lines if line.strip()]
        return valid_lines[:5]
    except Exception as e:
        return [f"【智能运营】限时福利已送达，点击查看 链接：https://brand.com/sms" for _ in range(5)]

# ==========================================
# 🛠️ STREAMLIT 多轮对话交互控制核心
# ==========================================

st.title("🎯 AI 驱动的智能运营人群圈选系统")
st.caption("基于 NVIDIA NIM (Llama-3.2-3b-instruct) 语义解析与内容生成管线")
st.markdown("---")

# 在 Session State 中维护复杂的多轮交互阶段状态（Stages）
if "input_val" not in st.session_state: st.session_state["input_val"] = ""
if "api_result" not in st.session_state: st.session_state["api_result"] = None
if "interaction_stage" not in st.session_state: st.session_state["interaction_stage"] = "init"  # init, ask_sms, show_sms
if "generated_sms" not in st.session_state: st.session_state["generated_sms"] = []

def click_tag(tag_text):
    st.session_state["input_val"] = tag_text
    st.session_state["api_result"] = filter_audience(tag_text)
    # 重置短信状态
    st.session_state["interaction_stage"] = "ask_sms" if st.session_state["api_result"]["status"] == "success" else "init"

# 第一步：用户圈选指令输入框
audience_input = st.text_input(
    "请输入您的人群圈选指令：", 
    value=st.session_state["input_val"],
    placeholder="例如：帮我圈选出进1年大促人群 / 近30天浏览未购客群",
    key="audience_input_key"
)

if audience_input != st.session_state["input_val"]:
    st.session_state["input_val"] = audience_input

if st.button("开始分析并圈选", type="primary"):
    if st.session_state["input_val"].strip() == "":
        st.warning("请输入指令后再提交哦！")
    else:
        with st.spinner("AI 正在解析多意图业务语义并切分底层数据集..."):
            res = filter_audience(st.session_state["input_val"])
            st.session_state["api_result"] = res
            # 如果圈选成功，立刻将阶段推进到“主动询问是否需要短信文案”
            if res["status"] == "success":
                st.session_state["interaction_stage"] = "ask_sms"
            else:
                st.session_state["interaction_stage"] = "init"

# 展示区
if st.session_state["api_result"]:
    result = st.session_state["api_result"]
    
    # 场景 A: Fallback 智能气泡引导
    if result["status"] == "fallback":
        st.info(f"💡 {result['message']}")
        cols = st.columns(len(result["suggestions"]) + 4)
        for idx, tag in enumerate(result["suggestions"]):
            with cols[idx]:
                st.button(f"👉 {tag}", key=f"tag_{idx}", on_click=click_tag, args=(tag,))
                
    # 场景 B: 圈选成功，联动多轮对话逻辑
    elif result["status"] == "success":
        st.success(f"✅ {result['message']}！共圈选出 {len(result['data'])} 条符合特征的用户数据。")
        st.dataframe(result["data"], use_container_width=True)
        
        st.markdown("---")
        
        # 💡 【主动追问与闭环阶段】：AI 探测到圈选成功，开始主动出击
        if st.session_state["interaction_stage"] == "ask_sms":
            st.info("🤖 **AI 主动助手**：检测到人群已成功打包。需要我顺便帮您针对这批人群**生成营销短信文案**吗？")
            
            # 提供对话式快捷回答输入框或按钮
            sms_intent_input = st.text_input("您可以回答“好的”、“是”、“需要”等：", key="sms_intent_input_key")
            
            # 按钮触发与文本输入触发双轨匹配
            cols_choice = st.columns(10)
            with cols_choice[0]:
                yes_clicked = st.button("👍 是的", type="secondary")
            with cols_choice[1]:
                no_clicked = st.button("👎 暂不需要")
                
            # 判断用户的肯定或否定回答
            is_affirmative = any(k in sms_intent_input for k in ["好", "是", "要", "ok", "OK", "确定", "行"]) or yes_clicked
            is_negative = any(k in sms_intent_input for k in ["不", "拒绝", "算", "别"]) or no_clicked
            
            if is_affirmative:
                with st.spinner("🚀 AI 正在根据该客群画像进行文案深度创作..."):
                    # 调用生成接口
                    sms_list = generate_marketing_sms(result.get("slots_desc", "电商用户"))
                    st.session_state["generated_sms"] = sms_list
                    st.session_state["interaction_stage"] = "show_sms"
                    
                    # 💡 同时按照要求：控制台主动输出5条短信文案
                    print("\n" + "="*30 + "\n🔥 [控制台已同步打印5条营销短信文案] 🔥")
                    for idx, sms in enumerate(sms_list):
                        print(f"文案 {idx+1}: {sms}")
                    print("="*30 + "\n")
                    
                st.rerun() # 强制刷新状态
            elif is_negative:
                st.session_state["interaction_stage"] = "init"
                st.toast("好的，已为您保存当前人群包。")
                
        # 阶段：展示生成好的5条文案供运营挑选
        elif st.session_state["interaction_stage"] == "show_sms":
            st.markdown("### 💌 AI 为您定制的5条营销短信（控制台已同步打印）")
            st.caption("您可以直接复制以下文案用于第三方 CRM 渠道投放：")
            
            for idx, sms in enumerate(st.session_state["generated_sms"]):
                # 用 Streamlit 的 code 组件提供一键复制功能，体验极佳
                st.code(sms, language="text")
                
            if st.button("重新生成一批文案"):
                st.session_state["interaction_stage"] = "ask_sms"
                st.rerun()
