import os
import re


def process_text(file_path):
    """
    处理小说文本，删除目录前的内容和epilogue后的内容，同时删除书源信息。

    :param file_path: 输入小说文件的路径
    :return: 处理后的小说内容
    """
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 初始化变量
    in_content = False  # 是否在目录部分
    in_text = False  # 是否在正文部分
    result = []  # 存储处理后的结果

    # 遍历每一行
    for line in lines:
        line = line.strip()  # 去除行首尾的空白字符
        if not line:
            continue  # 如果该行为空，跳过

        # 检测目录开始
        if line.lower() == "contents":
            in_content = True  # 进入目录部分
            continue

        # 检测目录结束
        if line == "==================================================":
            if in_content:
                in_content = False
                in_text = True  # 开始记录正文
            continue

        # 跳过书源信息
        if line.lower() == "oceanofpdf.com":
            continue

        # 如果在目录部分，跳过
        if in_content:
            continue

        # 如果在正文部分，记录内容
        if in_text:
            # 检测epilogue结束
            if line.lower() == 'epilogue':
                break
            result.append(line)

    return '\n'.join(result)  # 将处理后的内容合并为一个字符串


if __name__ == '__main__':
    # 输入文件夹路径
    folder_path = 'D:/01YIHAO/小说txt/liout'
    # 输出文件夹路径
    output_path = 'D:/01YIHAO/project/novels/format/out_novel'

    # 如果输出文件夹不存在，创建它
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    else:
        # 清空输出文件夹中的所有文件
        for file_name in os.listdir(output_path):
            file_path = os.path.join(output_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)

    # 遍历输入文件夹中的所有文件
    files = os.listdir(folder_path)
    for file_name in files:
        if file_name.endswith('txt'):  # 只处理txt文件
            file_path = os.path.join(folder_path, file_name)
            processed_content = process_text(file_path)  # 处理文件内容

            # 保存处理后的内容到输出文件夹
            output_file = os.path.join(output_path, file_name)
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(processed_content)
            print(f"Processed content saved to {output_file}")