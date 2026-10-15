import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv
from services import get_interview_evaluation

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
            try:
                # 【关键】直接调用服务层，拿回解析好的字典
                content_dict = get_interview_evaluation(user_input)

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
            except Exception as e:
                # 捕获服务层抛出的异常，优雅地展示在网页上
                st.error(f"面试过程发生错误：{e}")