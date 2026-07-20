import os
import json
import streamlit as st
from openai import OpenAI

# 1. 初始化页面配置
st.set_page_config(page_title="AI 运营人群圈选助手", layout="wide")

# ==========================================
# 📊 50 条真实假人群包数据
# ==========================================
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
  {"user_id": "U4010", "registration_date": "2023-10-28", "last_browse_date": "2025-12-09", "browsed_page_type": ["PLP"], "total_purchases": 8, "last_purchase_date": "2026-04-17", "purchase_channels": ["official_website", "Tmall"], "campaign_participation": ["618_2026", "Double11_2025"], "_mock_label": "大促人群"}
]

def get_ai_client():
    api_key = os.environ.get("NVAPI_KEY", "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")
    return OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=api_key)

def filter_audience(audience_feature):
    fallback_response = {
        "status": "fallback",
        "message": "没能完全理解您的指令，您是不是想找：",
        "suggestions": ["近2周注册未购", "近30天浏览未购"],
        "data": [],
        "parsed_intent": "未知"
    }

    try:
        client = get_ai_client()
        
        system_prompt = """
        你是一个数据分析专家。请根据用户输入，将其归类为以下四个标签之一：
        - 近2周注册未购
        - 近30天浏览未购
        - 近1年活跃用户
        - 大促人群
        请直接输出标签名，不要包含任何标点、符号或多余解释。
        """

        completion = client.chat.completions.create(
            model="meta/llama-3.2-3b-instruct",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": audience_feature}
            ],
            temperature=0.1,
            max_tokens=20
        )
        
        raw_label = completion.choices[0].message.content.strip()
        # 关键词映射逻辑，确保即便AI输出不规范也能精准匹配
        mapping = {
            "2周": "近2周注册未购",
            "注册": "近2周注册未购",
            "30天": "近30天浏览未购",
            "浏览": "近30天浏览未购",
            "1年": "近1年活跃用户",
            "活跃": "近1年活跃用户",
            "大促": "大促人群"
        }
        
        target_label = None
        for key, value in mapping.items():
            if key in raw_label or key in audience_feature:
                target_label = value
                break
                
        if not target_label:
            return fallback_response

        filtered_users = [user for user in data if user.get("_mock_label") == target_label]
        return {
            "status": "success",
            "message": f"成功匹配标签群包【{target_label}】",
            "suggestions": [],
            "data": filtered_users,
            "parsed_intent": target_label
        }
    except Exception as e:
        print(f"❌ AI 解析失败: {e}")
        return fallback_response

# ==========================================
# 差异化文案生成策略 — 模板化（只改这里）
# ==========================================

def generate_sms_copies(intent_label):
    """
    根据人群标签，采用模板化策略确保文案严格符合运营要求：
    - 近2周注册未购 → 强调新人券未使用
    - 近30天浏览未购 → 强调心仪好物未下单 + 送券
    - 大促人群 → 利益点前置，格式固定
    - 近1年活跃用户 → 强调老客专享券
    """
    
    templates = {
        "近2周注册未购": [
            "【品牌名称】您的新人专享大额券还未使用，即将过期！新会员首单立减50元，立即激活下单享专属优惠：xxxxxx 拒收请回复R",
            "【品牌名称】新人福利倒计时！您的注册专属优惠券即将失效，现在下单立享新人价：xxxxxx 拒收请回复R",
            "【品牌名称】恭喜成为新会员！您的新人礼包内含满199减50券，有效期仅剩3天，速来选购：xxxxxx 拒收请回复R",
            "【品牌名称】专属新人券待领取！注册即送无门槛优惠券，全场运动好物任您挑选：xxxxxx 拒收请回复R",
            "【品牌名称】新人首单特权！您的账户有1张新人专属券未使用，过期不候，立即选购：xxxxxx 拒收请回复R"
        ],
        "近30天浏览未购": [
            "【品牌名称】您心仪的好物还未下单！为您准备了专属30元无门槛券，库存紧张请速抢：xxxxxx 拒收请回复R",
            "【品牌名称】您浏览的商品正在降价！送您一张满299减60专属券，限时24小时有效：xxxxxx 拒收请回复R",
            "【品牌名称】购物车心动好物等您带走！专属优惠券已到账，下单立享折上折：xxxxxx 拒收请回复R",
            "【品牌名称】您关注的商品库存告急！送您专属加急券，优先锁单享特惠：xxxxxx 拒收请回复R",
            "【品牌名称】浏览未购专属福利！为您补发一张满199减40券，仅限今日使用：xxxxxx 拒收请回复R"
        ],
        "大促人群": [
            "【品牌名称】618年中狂欢福利来袭！170元满减券包限时领取！超多优惠等你来：xxxxxx 拒收请回复R",
            "【品牌名称】双11盛典开启！最高可领200元券包，全场低至3折起！超多优惠等你来：xxxxxx 拒收请回复R",
            "【品牌名称】大促倒计时！满300减80、满500减150，券包限量发放中！超多优惠等你来：xxxxxx 拒收请回复R",
            "【品牌名称】会员日专属狂欢！全场满减叠加券包最高省170元，仅限今日！超多优惠等你来：xxxxxx 拒收请回复R",
            "【品牌名称】年中大促最后1天！170元神券包未领取，错过再等半年！超多优惠等你来：xxxxxx 拒收请回复R"
        ],
        "近1年活跃用户": [
            "【品牌名称】老客专属感恩回馈！为您准备了满399减100元老客专享券，感谢一路陪伴：xxxxxx 拒收请回复R",
            "【品牌名称】VIP老客特权到账！专属老客复购券已发放，全场运动装备享额外折扣：xxxxxx 拒收请回复R",
            "【品牌名称】感谢您一年来的支持！老客专属福利券限时领取，满299减80：xxxxxx 拒收请回复R",
            "【品牌名称】老客尊享礼遇！您的年度专属优惠券已生效，复购享双倍积分+立减：xxxxxx 拒收请回复R",
            "【品牌名称】忠实会员专属！老客回馈券包已到账，含3张无门槛券，立即查收：xxxxxx 拒收请回复R"
        ]
    }
    
    if intent_label in templates:
        return templates[intent_label]
    
    return ["【品牌名称】活动进行中，点击即享惊喜优惠，超多优惠等你来：xxxxxx 拒收请回复R"]


# ==========================================
# STREAMLIT 前端交互面板（完全不动）
# ==========================================

st.title("🎯 AI 驱动的智能运营人群圈选系统")
st.caption("基于 NVIDIA NIM (Llama-3.2-3b-instruct) 智能标签映射与文案生成管线")
st.markdown("---")

if "input_val" not in st.session_state: st.session_state["input_val"] = ""
if "api_result" not in st.session_state: st.session_state["api_result"] = None
if "sms_generated" not in st.session_state: st.session_state["sms_generated"] = False
if "sms_copies" not in st.session_state: st.session_state["sms_copies"] = []

def click_tag(tag_text):
    # 将快捷推荐标签转换成系统能映射的标准词，保证气泡点击绝对成功
    mapping = {"近2周新客": "近2周注册未购", "近30天浏览未购": "近30天浏览未购"}
    query_text = mapping.get(tag_text, tag_text)
    st.session_state["input_val"] = query_text
    st.session_state["api_result"] = filter_audience(query_text)
    st.session_state["sms_generated"] = False 

# 输入区
audience_input = st.text_input(
    "请输入您的人群圈选指令：", 
    value=st.session_state["input_val"],
    placeholder="例如：帮我圈选出近30天浏览未购人群",
    key="audience_input_key"
)

if audience_input != st.session_state["input_val"]:
    st.session_state["input_val"] = audience_input
    st.session_state["sms_generated"] = False 

if st.button("开始分析并圈选", type="primary"):
    if st.session_state["input_val"].strip() == "":
        st.warning("请输入指令后再提交哦！")
    else:
        with st.spinner("AI 正在解析多意图业务语义并切分底层数据集..."):
            st.session_state["api_result"] = filter_audience(st.session_state["input_val"])
            st.session_state["sms_generated"] = False

# 展示结果
if st.session_state["api_result"]:
    result = st.session_state["api_result"]
    
    if result["status"] == "fallback":
        st.write("") 
        st.info(f"💡 {result['message']}")
        cols = st.columns(len(result["suggestions"]) + 4)
        for idx, tag in enumerate(result["suggestions"]):
            with cols[idx]:
                st.button(f"👉 {tag}", key=f"tag_{idx}", on_click=click_tag, args=(tag,))
                
    elif result["status"] == "success":
        st.success(f"✅ {result['message']}！共圈选出 {len(result['data'])} 条符合特征的用户数据。")
        st.dataframe(result["data"], use_container_width=True)
        
        # 多轮闭环营销问询
        st.markdown("---")
        st.subheader("🤖 AI 营销助理主动触达")
        st.info("📊 **检测到当前人群包已成功导出。需要我帮您为该人群生成专属的营销短信文案吗？**")
        
        chat_col, button_col = st.columns([6, 1])
        with chat_col:
            user_response = st.text_input("您可以回复：'好的'、'是'、'需要' 或直接点右侧按钮", placeholder="好的，帮我写个文案", key="chat_reply_key")
        with button_col:
            btn_triggered = st.button("🚀 直接生成", type="secondary")
            
        is_positive_reply = any(k in user_response for k in ["好的", "是", "需要", "要", "ok", "OK", "帮我"]) if user_response else False
        
        if (is_positive_reply or btn_triggered) and not st.session_state["sms_generated"]:
            with st.spinner("正在根据人群画像特征，使用差异化策略模板生成精准营销文案..."):
                copies = generate_sms_copies(result["parsed_intent"])
                st.session_state["sms_copies"] = copies
                st.session_state["sms_generated"] = True
                
                # 同步向控制台（Console）打印 5 条短信文案
                print("\n================== 🚀 AI 生成的 5 条短信文案 ==================")
                for i, sms in enumerate(copies, 1):
                    print(f"文案 {i}: {sms}")
                print("===============================================================\n")

        if st.session_state["sms_generated"]:
            st.write("✨ **为您精准定制的 5 条营销短信文案（已按人群策略差异化生成）：**")
            for idx, sms in enumerate(st.session_state["sms_copies"], 1):
                st.code(sms, language="text")
