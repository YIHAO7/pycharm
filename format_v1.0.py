# 把小说中content目录前的内容和epilogue后的内容删除掉
# 删除小说中的书源

# 或者index后的内容也要删除掉
import os
import re


output = {}  # 用于存储结果，键是标题，值是对应的正文内容列表

def process_text(file_path):
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 初始化变量
    in_content = False  #是否在目录部分
    in_text = False     #是否在正文部分
    content_result = [] #存储目录
    result = []         #存储处理后的结果
    line1 = []

    # 遍历每一行
    for line in lines:
        line = line.strip()
        # 如果该行为空，跳过
        if not line:
            continue

        line1.append(line)

    # 把目录中的内容存在list中
    # 根据目录找到正文部分，有的chapter下面并不是正文
    '''=======保存有用的信息放在result中，包括章节题目和正文'''
    for i in range(len(line1)):
        line = line1[i].strip()
        if line == "==================================================":
            if in_content:
                in_content = False
                in_text = True
                continue
            continue
        # 出现网站信息，跳过
        if line.lower() == "oceanofpdf.com":
            continue
        if line.lower() == "contents":
            in_content = True  # 进入目录部分
            continue
        if in_content:
            content_result.append(line)  # 存储content内容
            continue
        if in_text:
            if line.lower() == 'epilogue' or line.lower() == 'index':
                break
            result.append(line)

    '''=======将题目和正文放在一个字典中============'''
    i = 0 # 遍历result索引
    while i < len(result):
        line = result[i]
        if line in content_result:
            # 当前行为标题，下面就是正文
            current_title = line
            content_lines = []  # 存储标题下的正文内容
            i += 1 # 移动到下一行
            while i < len(result) and result[i] not in content_result:
                content_lines.append(result[i])
                i += 1
            output[current_title] = content_lines #将标题和对应的正文内容存储到结果字典中
        else:
            i += 1 #如果不是标题，直接跳过

    # 现在output[current_title]的值就是本文中的内容
    # 遍历output[current_title]中的内容
    print(output)

    # 将结果保存到文件
    # output_file = "output.txt"  # 定义输出文件的名称
    # with open(output_file, "w", encoding="utf-8") as file:
    #     for title, content in output.items():
    #         file.write(f"{title}\n")
    #         for line in content:
    #             file.write(f"{line}\n")
    #
    # print(f"结果已保存到文件 {output_file}")


    return '\n'.join(result)



if __name__ == '__main__':
    # folder_path = 'D:/01YIHAO/小说txt/liout'
    folder_path = 'D:/01YIHAO/project/novels/format/test_novel'
    output_path = 'D:/01YIHAO/project/novels/format/out_novel'

    if not os.path.exists(output_path):
        os.makedirs(output_path)
    else:
        # 清空输出文件夹中的所有文件
        for file_name in os.listdir(output_path):
            file_path = os.path.join(output_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)

    files = os.listdir(folder_path)
    for file_name in files:
        if file_name.endswith('txt'):

            file_path = os.path.join(folder_path,file_name)
            processed_content = process_text(file_path)

            # 保存处理后的内容到新文件
            output_file = os.path.join(output_path, f"{file_name}")
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(processed_content)
            print(f"Processed content saved to {output_file}")
