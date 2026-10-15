import requests, json, os
from dotenv import load_dotenv
import re

# 切片
def extract_json(text: str) ->str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    start = text.find("{")
    end = text.rfind("}")
    return text[start:end+1]



# 加载环境变量
load_dotenv()
API_KEY = os.getenv("ZHIPU_API_KEY")
URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

def get_interview_evaluation(user_input: str):
    # 准备请求数据
    data = {
        "model": "glm-4-flash",
        "messages": [
            {
                "role": "system",
                "content": '你是一个残酷无情的面试官，只看硬技能，绝不心软。你必须输出纯JSON格式的数据，不要任何多余的解释，不要加Markdown代码块标记（不要```json）。格式为：{"得分": 0到100的数字, "优点": ["优点1", "优点2"], "缺点": ["缺点1"], "是否通过": true或false}'
            },
            {"role": "user", "content": user_input}
        ],
        "response_format": {"type": "json_object"}
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    # 发送请求
    response = requests.post(URL, headers=headers, json=data, timeout=30)

    # 如果状态码不是200，抛出异常（让上层UI去处理）
    if response.status_code != 200:
        raise Exception(f"API请求失败，状态码：{response.status_code}，信息：{response.text}")

    # 解析JSON数据
    result = response.json()
    content_str = result['choices'][0]['message']['content']
    content_str = extract_json(content_str)
    content_dict = json.loads(content_str)

    return content_dict