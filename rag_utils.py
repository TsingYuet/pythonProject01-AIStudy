import re

def retrieve_relevant_chunks(question: str, chunks: list, top_k: int = 3) -> list:
    """
    手写简易检索：计算问题里的字符在片段中出现的次数，打分并排序。
    相当于 C++ 里的 std::sort 配合自定义比较器。
    """
    scored_chunks = []
    for chunk in chunks:
        score = 0
        # 粗暴的字符匹配：如果问题里的字在片段里出现，就加1分
        for char in question:
            if char in chunk:
                score += 1
        scored_chunks.append((score, chunk))

    # 按分数从高到低排序
    scored_chunks.sort(key=lambda x: x[0],reverse=True)

    # 返回得分最高的前top_k个片段
    return [chunk for score, chunk in scored_chunks[:top_k]]

def read_txt(file_path: str) -> str:
    """读取txt文件并返回字符串"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def split_text(text: str, chunk_size: int = 200,overlap: int = 50) -> list:
    """
    把长文本切片，类似 C++ 的 vector<string>
    chunk_size: 每片多少字
    overlap: 相邻两片之间重叠多少字（防止刚好把一句话切断，导致语义丢失）
    """
    chunks = []
    start = 0
    text_length = len(text)

    # 类似于C++的while（start<length)
    while start < text_length:
        end = start + chunk_size
        # 切片操作，类似substr（start，length）
        chunks.append(text[start:end])
        # 下一次的起点，往回退overlap个字符
        start += (chunk_size - overlap)

    return chunks
