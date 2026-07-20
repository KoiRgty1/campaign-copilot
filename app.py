import streamlit as st
import json
import pandas as pd
from datetime import datetime

# 1. 页面标题
st.set_page_config(page_title="CRM AI Agent", layout="wide")
st.title("🚀 Campaign Copilot: 智能大促指挥舱")

# 2. 加载数据
@st.cache_data
def load_data():
    with open("crm_mock_data_50.json", "r", encoding="utf-8") as f:
        return json.load(f)

data = load_data()

# 3. 核心筛选函数：根据人群特征筛选用户
def filter_audience(audience_feature):
    """
    根据输入的人群特征筛选用户
    支持特征：近2周新客、大促沉默人群、2026年未购买、618参与用户、Double11参与用户等
    """
    # 初始化筛选结果
    filtered_users = data
    
    # 按特征筛选逻辑
    if "近2周新客" in audience_feature:
        filtered_users = data[:10]  # 模拟近2周新客数据
    if "大促沉默人群" in audience_feature or "2026年未购买" in audience_feature:
        filtered_users = [
            u for u in filtered_users 
            if any("618" in c or "Double11" in c for c in u.get("campaign_participation", [])) 
            and (u.get("last_purchase_date") is None or u.get("last_purchase_date") < "2026-01-01")
        ]
    if "618参与用户" in audience_feature:
        filtered_users = [
            u for u in filtered_users 
            if any("618" in c for c in u.get("campaign_participation", []))
        ]
    if "Double11参与用户" in audience_feature:
        filtered_users = [
            u for u in filtered_users 
            if any("Double11" in c for c in u.get("campaign_participation", []))
        ]
    
    return filtered_users

# 4. AI文案生成函数：根据筛选人群生成定制化短信文案
def generate_ai_copy(audience_feature, user_count):
    """根据人群特征和数量生成个性化短信文案"""
    base_copy = "【迪卡侬】亲爱的会员"
    if "沉默" in audience_feature:
        base_copy += "，好久不见！特为您准备了大促专属回归礼包，点击领取立减50元，仅限3天～"
    elif "新客" in audience_feature:
        base_copy += "，恭喜成为迪卡侬新会员！大促期间首单立减30元，新人专享福利等你来～"
    elif "618" in audience_feature:
        base_copy += "，618狂欢开启！您参与过往期618活动，专属优惠券已到账，速来抢购～"
    elif "Double11" in audience_feature:
        base_copy += "，双11预售抢先购！专属折扣+满减，错过再等一年～"
    else:
        base_copy += "，大促福利来袭！全场商品低至5折，会员额外9折，速来选购～"
    
    # 补充人群数量信息
    final_copy = f"{base_copy}\n（本次筛选目标人群共{user_count}人）"
    return final_copy

# 5. 聊天交互逻辑
# 初始化聊天历史（避免刷新丢失）
if "messages" not in st.session_state:
    st.session_state.messages = []

# 展示历史聊天记录
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 聊天输入框
if prompt := st.chat_input("请输入人群特征（例如：大促沉默人群、近2周新客、618参与用户）"):
    # 1. 展示用户输入
    st.chat_message("user").markdown(f"筛选条件：{prompt}")
    st.session_state.messages.append({"role": "user", "content": f"筛选条件：{prompt}"})
    
    # 2. 调用筛选函数
    filtered_users = filter_audience(prompt)
    user_count = len(filtered_users)
    
    # 3. 生成AI文案
    ai_copy = generate_ai_copy(prompt, user_count)
    
    # 4. 组装回复内容
    response = f"""
### 筛选结果
共筛选出 **{user_count}** 位目标用户

### AI生成召回短信文案
{ai_copy}

### 人群数据预览（前5条）
"""
    # 5. 展示助手回复
    with st.chat_message("assistant"):
        st.markdown(response)
        # 展示前5条数据表格
        if filtered_users:
            st.table(pd.DataFrame(filtered_users[:5]))
        else:
            st.warning("未筛选出符合条件的用户")
    
    # 6. 保存到聊天历史
    st.session_state.messages.append({
        "role": "assistant", 
        "content": response + (f"\n\n```\n{pd.DataFrame(filtered_users[:5]).to_string()}\n```" if filtered_users else "\n\n未筛选出符合条件的用户")
    })

# 6. 保留原有侧边栏筛选（可选，如需保留历史功能）
st.sidebar.header("📋 快捷筛选（备用）")
query_type = st.sidebar.radio("选择筛选策略", ["近2周新客", "大促沉默人群 (排除2026年购买)"])

def filter_data(query_type):
    if query_type == "大促沉默人群 (排除2026年购买)":
        return [u for u in data if any("618" in c or "Double11" in c for c in u.get("campaign_participation", [])) 
                and (u.get("last_purchase_date") is None or u.get("last_purchase_date") < "2026-01-01")]
    return data[:10]

# 展示快捷筛选结果（可选）
if st.sidebar.button("查看快捷筛选结果"):
    quick_filtered = filter_data(query_type)
    st.sidebar.write(f"快捷筛选结果：{len(quick_filtered)} 人")
