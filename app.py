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
        "suggestions": ["近2周新客", "近30天浏览未购"],
        "data": [],
        "parsed_intent": "未知"
    }

    try:
        client = get_ai_client()
        
        system_prompt = """
        你是一个数据分析专家。请根据运营人员输入的人群圈选指令，判断它最符合以下哪一种既定的受众特征分类。
        你必须且只能输出这四个分类标签的其中一个，不要包含任何 Markdown 格式（如星号、```等），也不要回答任何废话。
        
        【可选分类标签】：
        - 近2周注册未购
        - 近30天浏览未购
        - 近1年活跃用户
        - 大促人群
        
        【判定规则】
        1. 必须有极强的错别字及错词包容力。如输入"进1年大促人群"归类为"大促人群"；输入"帮我圈选出近30天浏览未购人群"归类为"近30天浏览未购"。
        2. 如果输入完全无关乱码（如"哈哈"），请输出 UNKNOWN。
        """

        completion = client.chat.completions.create(
            model="meta/llama-3.2-3b-instruct",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": audience_feature}
            ],
            temperature=0.1,
            max_tokens=30,
            timeout=7.0
        )
        
        # 💡 【核心修复】：移除任何可能混入的 Markdown 标记、引号、空格或换行
        raw_label = completion.choices[0].message.content.strip()
        cleaned_label = raw_label.replace('"', '').replace("'", "").replace("*", "").replace("`", "").strip()
        print(f"💡 [NVIDIA AI 吐出的原始文本]: {repr(raw_label)}")
        print(f"💡 [清洗后的解析标签]: {repr(cleaned_label)}")

        # 💡 【模糊匹配兜底】：防止大模型吐出“根据判断，应归为：近30天浏览未购”这种长句子
        target_label = None
        for candidate in ["近2周注册未购", "近30天浏览未购", "近1年活跃用户", "大促人群"]:
            if candidate in cleaned_label:
                target_label = candidate
                break
                
        if not target_label:
            return fallback_response

        # 精准切分底层对应的 10 条数据
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

def generate_sms_copies(intent_label):
    try:
        client = get_ai_client()
        prompt = f"""
        你是一个拥有10年经验的中国本土电商CRM营销专家，专门负责撰写高点击率的短信触达文案。
        请为购买偏好特征为“{intent_label}”的精准用户，撰写 5 条极具诱惑力、极富催单效果的促销短信文案。
        
        【严格文案结构模板】
        每一条文案必须严格完全遵循以下结构，严禁夹带中英夹杂词（如Buy、Click）：
        【狄卡侬】[利益点/狂欢主题]！[针对近30天浏览未购用户的催单/券包福利文案]！超多优惠等你来：xxxxxx 拒收请回复R
        
        【用户画像与切入点】
        当前人群偏好为“近30天浏览未购”。他们对产品有明确兴趣。
        你需要用不同的营销钩子（如：年中狂欢、限时满减、购物车催单、专享无门槛券、限时秒杀）来包装这5条文案。
        
        【优秀案例参考（必须严格模仿这种精炼的运营文风）】
        - 【狄卡侬】618年中狂欢福利来袭！170元满减券包限时领取！超多优惠等你来：xxxxxx 拒收请回复R
        - 【狄卡侬】您关注的心仪好物降价啦！专属购物车特惠津贴已到账！超多优惠等你来：xxxxxx 拒收请回复R
        
        【输出规范】
        直接输出 5 条文案，每条占独立的一行。绝对不要写任何序号（如 1. 2.），也不要有任何开头介绍或客套解释。
        """

        completion = client.chat.completions.create(
            model="meta/llama-3.2-3b-instruct",
            messages=[
                {"role": "system", "content": "你是一个只输出规定模板短信的电商运营小秘书。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=400,
            timeout=10.0
        )
        
        raw_output = completion.choices[0].message.content.strip()
        # 清洗掉可能带出来的乱七八糟序号
        lines = raw_output.split('\n')
        copies = []
        for line in lines:
            line_str = line.strip()
            if not line_str: continue
            # 滤除类似 "1. " 或 "1、" 的行首前缀
            if line_str[0].isdigit() and len(line_str) > 2 and line_str[1] in ['.', '、', ' ']:
                line_str = line_str[2:].strip()
            copies.append(line_str)
            
        return copies[:5]
    except Exception as e:
        print(f"❌ 文案生成失败: {e}")
        return [
            "【甄选好物】您关注的心仪商品正在限时特惠，购物车满减活动今晚截止，速戳！ 链接：xxxx",
            "【限时秒杀】专属您的惊喜回馈礼券已到账！点击进入挑选爆款立减！ 链接：xxxx",
            "【粉丝福利】您心心念念的宝贝库又有新动作啦！点击一键领取粉丝限时特价 链接：xxxx",
            "【狂欢加码】错过等一年！全场商品低至5折起，点击链接直达狂欢会场抢购 链接：xxxx",
            "【老客特权】感谢一路相伴，特为您申请的保价权益已生效，戳链接速查 链接：xxxx"
        ]

# ==========================================
# 🛠️ STREAMLIT 前端交互面板
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
            with st.spinner("正在根据人群画像特征，使用 Llama-3.2 智能拟定差异化营销文案..."):
                copies = generate_sms_copies(result["parsed_intent"])
                st.session_state["sms_copies"] = copies
                st.session_state["sms_generated"] = True
                
                # 同步向控制台（Console）打印 5 条短信文案
                print("\n================== 🚀 AI 生成的 5 条短信文案 ==================")
                for i, sms in enumerate(copies, 1):
                    print(f"文案 {i}: {sms}")
                print("===============================================================\n")

        if st.session_state["sms_generated"]:
            st.write("✨ **为您精准定制的 5 条营销短信文案（已同步输出至控制台供系统挑选）：**")
            for idx, sms in enumerate(st.session_state["sms_copies"], 1):
                st.code(sms, language="text")
