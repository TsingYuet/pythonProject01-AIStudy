import requests
import json


# 1.配置API信息
API_KEY = "你的API_KEY"
URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions" # URL是什么，怎么决定填写什么的


# 2.准备要发送给AI的数据
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}
# 花括号这种是叫json格式吗×   {}叫字典，键值对

data = {
    "model": "glm-4-flash",
    "messages": [
        {"role": "system", "content": "你是一个只有7岁智商的小朋友，说话很喜欢用感叹号！"},
        {"role": "user", "content": "请用一句话给我讲个关于程序员的冷笑话。"}
    ]  # []叫列表
    # 这个是叫提示词prompt吗？  准确来说data是一份请求体，content内容是prompt
}

# 3.发送请求
print("正在向AI发送请求...")
response = requests.post(URL, headers=headers, json=data)
# 这个函数是干什么的？  post向服务器提交数据，URL（发给谁）、headers（你的身份凭证，比如 API Key）、json=data（你要寄的包裹内容）


# 4.处理返回结果
if response.status_code == 200:
    result = response.json()
    ai_reply = result['choices'][0]['message']['content']
    print("\n=== AI 的回复 ===\n")
    print(ai_reply)
elif response.status_code == 401:
    print("错误：API Key 无效，请检查你的 Key 是否正确。")
elif response.status_code == 402:
    print("错误：余额不足。")
elif response.status_code == 429:
    print("错误：请求太频繁，被限流了。")
else:
    print(f"未知错误，状态码：{response.status_code}")
    print(response.text)