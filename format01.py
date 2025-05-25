import os
import re

# 定义目录开始正则表达式
con_pattern = r"\b(?:contents|table\s+of\s+contents)\b.*$"
# 正文结尾正则表达式
# end_pattern = r"^(epilogue|index)$"
end_pattern = r"\b(?:index|epilogue|acknowledgments)\b.*$"

# 文章中无用的片段正则表达式
# Author’s Note
ignore_pattern = r"\b(?:prologue|preface|cover|title\s+page|dedication|epigraph|copyright(?:\s+page)?|also\s+by\s+[a-z]+(?:\s+[a-z]+)?|about\s+the\s+(?:book|author))\b.*$"

# result = []  # 存储处理后的结果
# content_result = []  # 存储目录的结果


def process_text(file_path):
    """
    处理小说文本，删除目录前的内容和epilogue后的内容，同时删除书源信息。

    :param file_path: 输入小说文件的路径
    :return: 处理后的小说内容
    """
    # 获取文章的目录
    content_result = save_content(file_path)
    print(content_result)
    return ''.join(content_result)

    # 如果目录中有明显的Chapater 则从Chapter后开始

    # 如果文章没有目录

    # 如果文章目录没有明显的chapter

    #

    # # 读取文件内容
    # with open(file_path, 'r', encoding='utf-8') as file:
    #     lines = file.readlines()
    # # 初始化变量
    # in_content = False  # 是否在目录部分
    # in_text = False  # 是否在正文部分
    # in_textTure = False
    #
    #
    # # 遍历每一行
    # for line in lines:
    #     line = line.strip()  # 去除行首尾的空白字符
    #     if not line:
    #         continue  # 如果该行为空，跳过
    #     # 跳过书源信息
    #     if line.lower() == "oceanofpdf.com":
    #         continue
    #
    #     # 检测目录开始
    #     if re.match(con_pattern, line, re.IGNORECASE):
    #         in_content = True  # 进入目录部分
    #         continue
    #     # 如果在目录部分，添加进目录中
    #     if in_content:
    #         # 检测目录结束，进入正文部分
    #         if line == "==================================================":
    #             in_content = False
    #             in_text = True  # 开始记录正文
    #         else:
    #             # 去除特殊目录如：1.***
    #             # 替换第一个点号为空字符串
    #             cleaned_line = re.sub(r"(\d+)\.\s*", r"\1", line)
    #             content_result.append(cleaned_line)
    #         continue
    #
    #
    #     # 如果在正文部分，记录内容
    #     if in_text:
    #         for content in content_result:
    #             if content.lower() == line.lower():
    #                 # 开始记录正文
    #                 in_textTure = True
    #                 break
    #         if re.match(ignore_pattern, line, re.IGNORECASE):
    #             in_textTure = False
    #         if line == "==================================================":
    #             in_textTure =False
    #         if line.lower() == "Acknowledgments":
    #             print("aa")
    #         # 检测epilogue结束
    #         if re.match(end_pattern, line, re.IGNORECASE):
    #             # in_textTure = False
    #             print(line)
    #             break
    #     if in_textTure:
    #         result.append(line)

    # return '\n'.join(content_result)  # 将处理后的内容合并为一个字符串

def save_content(file_path):
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    # 初始化变量
    in_content = False  # 是否在目录部分
    content_result = []
    # 遍历每一行
    for line in lines:
        line = line.strip()  # 去除行首尾的空白字符
        if not line:
            continue  # 如果该行为空，跳过
        # 跳过书源信息
        if line.lower() == "oceanofpdf.com":
            continue
        # 检测目录开始
        if re.match(con_pattern, line, re.IGNORECASE):
            in_content = True  # 进入目录部分
            continue
        # 如果在目录部分，添加进目录中
        if in_content:
            # 检测目录结束，进入正文部分
            if line == "==================================================":
                in_content = False
            else:
                # 去除特殊目录如：1.***
                # 替换第一个点号为空字符串
                cleaned_line = re.sub(r"(\d+)\.\s*", r"\1", line)
                content_result.append(cleaned_line)
            continue
    return '\n'.join(content_result)

if __name__ == '__main__':
    # 输入文件夹路径
    folder_path = 'D:/01YIHAO/小说txt/liout'
    # folder_path = 'D:/01YIHAO/project/novels/format/test_novel'
    # 输出文件夹路径
    output_path = 'D:/01YIHAO/project/novels/format/out_novel'

    # process_text("D:/01YIHAO/project/novels/format/test_novel/Dirty_Diana_-_Jen_Besser_Shana_Feste.txt")

    # 如果输出文件夹不存在，创建它
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    else:
        # 存在，清空输出文件夹中的所有文件
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

            # if not processed_content.strip():
            #     continue
            # 保存处理后的内容到输出文件夹
            output_file = os.path.join(output_path, file_name)
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(processed_content)
            print(f"Processed content saved to {output_file}")
