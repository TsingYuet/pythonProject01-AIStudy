import requests
import json
import os
from dotenv import load_dotenv

# 自动加载。env文件里的变量
load_dotenv()

# 1.配置API信息
API_KEY = os.getenv("ZHIPU_API_KEY")
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
        {"role": "system", "content": "你是一个残酷无情的面试官，只看硬技能，绝不心软。你必须输出纯JSON格式的数据，不要任何多余的解释，不要加Markdown代码块标记（不要```json）。格式为：{'得分': 0到100的数字, '优点': ['优点1', '优点2'], '缺点': ['缺点1'], '是否通过': true或false}"},
        {"role": "user", "content": "这是我的面试自我介绍：'我今年刚毕业，只会一点点Python，还没做过项目，但我很愿意学。' 请根据我的表现打分。"}
    ],
    "response_format": {"type": "json_object"} # 强迫模型输出 JSON 对象
}

# 3.发送请求
print("正在向AI发送请求...")
response = requests.post(URL, headers=headers, json=data)
# 这个函数是干什么的？  post向服务器提交数据，URL（发给谁）、headers（你的身份凭证，比如 API Key）、json=data（你要寄的包裹内容）


# 4.处理返回结果
if response.status_code == 200:
    result = response.json()
    # 注意：拿到的是字符串（String）
    content_str = result['choices'][0]['message']['content']
    print("原始返回：", content_str)

    # 【核心知识点】用 json.loads() 把字符串转换成 Python 字典
    content_dict = json.loads(content_str)

    # 现在可以用字典的方式取值了
    print("\n=== 面试结果 ===")
    print("得分：", content_dict.get("得分"))
    print("优点：", content_dict.get("优点"))
    print("缺点：", content_dict.get("缺点"))
    print("是否通过：", "通过" if content_dict.get("是否通过") else "淘汰")
else:
    print("请求失败，错误码：", response.status_code)
    print(response.text)