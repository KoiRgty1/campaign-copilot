def filter_audience(audience_feature):
    """
    根据输入的人群特征筛选用户
    支持特征：近2周新客/注册未购、近30天浏览未购等
    规则：
    1. 默认返回空数组，无法识别指令时返回0条
    2. 解析多意图关键词，匹配则加入对应人群
    3. 按user_id去重，确保无重复用户
    """
    # 1. 默认状态为空数组（遵守规则1）
    filtered_users = []
    
    # 模拟数据：近2周注册未购人群（10人）
    new_customer_2w = data[:10]  # 沿用原有模拟逻辑
    # 模拟数据：近30天浏览未购人群（10人，取data中11-20条）
    browse_30d = data[11:21] if len(data) >= 21 else data[10:]
    
    # 2. 强化关键词解析（遵守规则2）
    # 识别"近2周"或"新客"关键词，加入对应人群
    if any(keyword in audience_feature for keyword in ["近2周", "新客", "注册未购"]):
        filtered_users.extend(new_customer_2w)
    
    # 识别"近30天"或"浏览"关键词，加入对应人群
    if any(keyword in audience_feature for keyword in ["近30天", "浏览", "浏览未购"]):
        filtered_users.extend(browse_30d)
    
    # 3. 去重机制：按user_id去重（遵守规则3）
    # 先通过字典去重（利用字典key唯一特性），再转回列表
    unique_users = {}
    for user in filtered_users:
        user_id = user.get("user_id")  # 假设数据中有user_id字段作为唯一标识
        if user_id:  # 确保user_id存在才去重
            unique_users[user_id] = user
    
    # 转回列表返回
    return list(unique_users.values())
