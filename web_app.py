import streamlit as st
from services import get_knowledge_answer, get_interview_evaluation
from rag_utils import split_text, read_txt, retrieve_relevant_chunks

page = st.sidebar.radio("功能导航", ["AI面试官", "个人写手网文知识问答"])


if page == "AI面试官":
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
else:
    st.title("个人写手网文知识问答")
    st.write("上传你的资料，基于资料回答你的问题。")

    # 1. 读取文件并切片（这里先写死路径，后面你可以改成上传文件）
    file_path = "data/resume.txt"
    try:
        text = read_txt(file_path)
        chunks = split_text(text, chunk_size=200, overlap=50)
        st.info(f"资料加载成功，共切分为 {len(chunks)} 个片段。")

        # 2. 用户输入问题
        user_question = st.text_input("请输入关于资料的问题：")

        if st.button("向知识库提问"):
            if not user_question:
                st.warning("问题不能为空！")
            else:
                with st.spinner("AI 正在翻阅资料..."):
                    try:
                        # 先检索，不要全量拼接
                        relevant_chunks = retrieve_relevant_chunks(user_question, chunks, top_k=3)
                        # 只拼接这 3 个相关的片段（极大缩减 Token 长度）
                        context = "\n\n".join(relevant_chunks)
                        answer = get_knowledge_answer(user_question, context)
                        st.success("回答完成：")
                        st.write(answer)
                    except Exception as e:
                        st.error(f"发生错误：{e}")
    except FileNotFoundError:
        st.error(f"找不到文件：{file_path}，请确保你在 data 文件夹里创建了该文件。")
