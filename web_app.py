import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()
API_KEY = os.getenv("ZHIPU_API_KEY")
URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

# 设置网页标题


st.title("AI面试官")
st.write("请输入你的自我介绍，AI将为你打分")

# 创建网页输入框和按钮
user_input = st.text_area("你的自我介绍：","我今年刚毕业，只会一点点python，还没做过项目，但我很愿意学")

if st.button("提交面试"):
    if not user_input:
        st.warning("请先输入自我介绍")
    else:
        with st.spinner("面试官正在评估中，请稍候..."):
            # 准备请求数据
            data = {
                "model": "glm-4-flash",
                "messages": [
                    {
                        "role": "system",
                        "content": "你是一个残酷无情的面试官，只看硬技能，绝不心软。你必须输出纯JSON格式的数据，不要任何多余的解释，不要加Markdown代码块标记（不要```json）。格式为：{'得分': 0到100的数字, '优点': ['优点1', '优点2'], '缺点': ['缺点1'], '是否通过': true或false}"
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
            response = requests.post(URL, headers=headers, json=data)

            if response.status_code == 200:
                result = response.json()
                content_str = result['choices'][0]['message']['content']
                content_dict = json.loads(content_str)

                # 在网页上展示结果
                st.success("评估完成！")
                st.metric(label="面试得分",value=f"{content_dict.get('得分')}分")

                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("优点")
                    for item in content_dict.get("优点", []):
                        st.write(f"- {item}")
                with col2:
                    st.subheader("缺点")
                    for item in content_dict.get("缺点", []):
                        st.write(f"- {item}")

                if content_dict.get("是否通过"):
                    st.balloons()
                    st.success("恭喜通过面试")
                else:
                    st.error("遗憾淘汰")
            else:
                st.error(f"请求失败，错误码：{response.status_code}")
                st.write(response.text)