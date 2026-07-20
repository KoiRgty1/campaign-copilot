import os
import json
from openai import OpenAI

# 假定你的 mock 数据源，为了配合 AI 检索，我们为数据丰富一些底层标签字段
# 建议在文件顶部或外部定义好 data 数据
data = [
    {"user_id": "U2001", "is_new": True, "behavior": "none", "is_promotion_buyer": False},
    {"user_id": "U2002", "is_new": False, "behavior": "browse", "is_promotion_buyer": False},
    {"user_id": "U2003", "is_new": False, "behavior": "none", "is_promotion_buyer": True},
    {"user_id": "U2004", "is_new": True, "behavior": "browse", "is_promotion_buyer": False},
    {"user_id": "U2005", "is_new": False, "behavior": "browse", "is_promotion_buyer": True},
]

def filter_audience(audience_feature):
    """
    【AI驱动版本】根据输入的人群特征，通过 NVIDIA Llama-3.2-3b 识别意图并筛选用户。
    同时支持前端 Fallback 气泡提示策略。
    
    返回格式: 
    {
        "status": "success" | "fallback",
        "message": "提示文本",
        "suggestions": ["推荐标签1", "推荐标签2"],  # 用于前端气泡
        "data": [...]                           # 筛选出的用户列表
    }
    """
    # 默认兜底返回结构
    fallback_response = {
        "status": "fallback",
        "message": "没能完全理解您的指令，您是不是想找：",
        "suggestions": ["近2周新客", "近30天浏览未购"],
        "data": []
    }

    # 1. 初始化 NVIDIA API 客户端
    # 优先从系统环境变量读取 NVAPI_KEY，如果没有则请替换为你的明文 Key
    api_key = os.environ.get("NVAPI_KEY", "你的_NVIDIA_API_KEY")
    
    if not api_key or api_key == "你的_NVIDIA_API_KEY":
        print("❌ 警告: 未配置有效的 NVIDIA API Key，触发前端兜底策略。")
        return fallback_response

    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=api_key
    )

    # 2. 构建面向 Slot-Filling 的 System Prompt
    system_prompt = """
    你是一个电商数据分析专家。请解析运营人员输入的人群圈选指令，并严格转化为结构化的 JSON 格式。
    
    你必须输出且只能输出以下四个字段，不要包含任何 Markdown 格式（如 ```json）或多余解释：
    - is_new: [true, false, "all"] (提到"新客"、"注册未购"设为 true，否则默认为 "all")
    - time_range_days: 整数 (如"近2周"为14，"近30天"为30，"近1年"/"进1年"为365，未提到默认为 -1)
    - behavior: ["browse", "purchase", "all"] (提到"浏览"设为 "browse"，提到"未购"但没提浏览不作为browse，未提到默认为 "all")
    - is_promotion_buyer: [true, false] (提到"大促"、"活动"、"节假日"设为 true，否则为 false)
    
    【重要容错规则】
    1. 必须具备错别字纠错能力（例如输入"进1年"应等同于"近1年"，将其 time_range_days 解析为 365）。
    2. 如果输入的文本完全不包含上述任何维度的特征（如输入"哈哈"或"大白菜"），请将所有字段设为 "all" 或 false。
    """

    try:
        # 3. 调用 NVIDIA NIM 接口
        completion = client.chat.completions.create(
            model="meta/llama-3.2-3b-instruct",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": audience_feature}
            ],
            temperature=0.1,  # 降低随机性确保 JSON 格式稳定
            max_tokens=150
        )
        
        response_text = completion.choices[0].message.content.strip()
        slots = json.loads(response_text)
        print(f"💡 [NVIDIA AI 语义解析成功]: {slots}")

        # 4. 判断是否完全没有匹配到任何有效特征（触发 Fallback 条件 1）
        is_empty_intent = (
            slots.get("is_new") == "all" and 
            slots.get("time_range_days") == -1 and 
            slots.get("behavior") == "all" and 
            slots.get("is_promotion_buyer") is False
        )
        
        if is_empty_intent:
            return fallback_response

        # 5. 根据大模型解析出的槽位（Slots）过滤本地 mock 数据（遵守原去重规则）[cite: 2]
        filtered_users = []
        for user in data:
            if slots["is_new"] != "all" and user.get("is_new") != slots["is_new"]:
                continue
            if slots["behavior"] != "all" and user.get("behavior") != slots["behavior"]:
                continue
            if slots["is_promotion_buyer"] and not user.get("is_promotion_buyer"):
                continue
            # 注：此处未强制绑定具体天数逻辑，可根据实际 data 的 date 字段进一步扩充过滤
            filtered_users.append(user)

# 6. 按 user_id 去重机制
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
        # 7. API 报错或 JSON 解析异常拦截（触发 Fallback 条件 2）
        print(f"❌ AI 解析失败或发生异常: {e}")
        return fallback_response
