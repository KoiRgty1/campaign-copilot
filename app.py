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

# 3. 侧边栏：交互式筛选逻辑 (模拟 Text-to-Logic)
st.sidebar.header("📋 智能人群筛选")
query_type = st.sidebar.radio("选择筛选策略", ["近2周新客", "大促沉默人群 (排除2026年购买)"])

def filter_data(query_type):
    if query_type == "大促沉默人群 (排除2026年购买)":
        return [u for u in data if any("618" in c or "Double11" in c for c in u.get("campaign_participation", [])) 
                and (u.get("last_purchase_date") is None or u.get("last_purchase_date") < "2026-01-01")]
    return data[:10] # 默认

# 4. 主区域：展示结果
filtered_users = filter_data(query_type)
st.write(f"共筛选出 {len(filtered_users)} 位目标用户")
st.table(pd.DataFrame(filtered_users))

# 5. 亮点功能：一键生成文案
if st.button("生成召回短信文案"):
    st.success("AI 建议文案：【迪卡侬】亲爱的会员，好久不见！特为您准备了一份大促专属回归礼包，点击领取...")