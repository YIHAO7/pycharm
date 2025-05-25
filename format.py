import os
import re

# 目录开始
con_pattern = r"\b(?:contents|table\s+of\s+contents)\b.*$"
# 结尾
# end_pattern = r"^(epilogue|index)$"
end_pattern = r"\b(?:index|epilogue|acknowledgments)\b.*$"
# 文章中无用的片段
# Author’s Note
ignore_pattern = r"\b(?:prologue|preface|cover|title\s" \
                 r"+page|dedication|epigraph|copyright(?:\s+page)?|" \
                 r"also\s+by\s+[a-z]+(?:\s+[a-z]+)?|about\s" \
                 r"+the\s+(?:book|author))\b.*$"

def eng_format(line):
    # 定义正则表达式模式，匹配 "Chapter" 后面跟着的单词
    eng_pattern = r"Chapter\s+(One|two|three" \
              r"|Four|Five|Six|Seven|Eight|" \
              r"Nine|ten|Eleven|twelve|thirteen|" \
              r"Fourteen|Fifteen|Sixteen|Seventeen|" \
              r"Eighteen|Nineteen|twenty|twenty-One|" \
              r"twenty-two|twenty-three|twenty-Four|" \
              r"twenty-Five|twenty-Six|twenty-Seven|" \
              r"twenty-Eight|twenty-Nine|thirty|" \
              r"thirty-One)"
    number_pattern = r"(One|two|three" \
                  r"|Four|Five|Six|Seven|Eight|" \
                  r"Nine|ten|Eleven|twelve|thirteen|" \
                  r"Fourteen|Fifteen|Sixteen|Seventeen|" \
                  r"Eighteen|Nineteen|twenty|twenty-One|" \
                  r"twenty-two|twenty-three|twenty-Four|" \
                  r"twenty-Five|twenty-Six|twenty-Seven|" \
                  r"twenty-Eight|twenty-Nine|thirty|" \
                  r"thirty-One)"
    # 定义一个字典，将英文单词映射到对应的数字
    word_to_number = {
        "one": "1", "two": "2", "three": "3", "four": "4", "five": "5",
        "six": "6", "seven": "7", "eight": "8", "nine": "9", "ten": "10",
        "eleven": "11", "twelve": "12", "thirteen": "13", "fourteen": "14",
        "fifteen": "15", "sixteen": "16", "seventeen": "17", "eighteen": "18",
        "nineteen": "19", "twenty": "20", "twenty-one": "21", "twenty-two": "22",
        "twenty-three": "23", "twenty-four": "24", "twenty-five": "25",
        "twenty-six": "26", "twenty-seven": "27", "twenty-eight": "28",
        "twenty-nine": "29", "thirty": "30", "thirty-one": "31"
    }

    pattern = re.compile(eng_pattern, re.IGNORECASE)
    match = pattern.match(line)
    if match:
        # 提取英文序号部分
        english_number = match.group(1).lower()
        # 替换为对应的数字序号
        line = f'Chapter {word_to_number[english_number]}'
    pattern = re.compile(number_pattern, re.IGNORECASE)
    match = pattern.match(line)
    if match:
        # 提取英文序号部分
        english_number = match.group(1).lower()
        # 替换为对应的数字序号
        line = f'Chapter {word_to_number[english_number]}'
    return line

def process_text(index,file_path):
    """
    处理小说文本，删除目录前的内容和epilogue后的内容，同时删除书源信息。
    格式化章节标题
    """

    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    # 初始化变量
    in_content = False  # 是否在目录部分
    in_text = False  # 是否在正文部分
    in_textTure = False
    result = []  # 存储处理后的结果
    content_result = []  # 存储目录的结果
    format_content = []  # 存储格式化后的目录结果

    # 定义目录-格式后的字典
    content_dict = {}

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
            # 根据==========检测目录结束，进入正文部分
            if line == "==================================================":
                in_content = False
                in_text = True  # 开始记录正文
            else:
                # 处理特殊章节目录
                # 去除特殊目录如：1.***
                # 替换第一个点号为空字符串
                line = re.sub(r"(\d+)\.\s*", r"\1", line)
                # 如果出现数字 统一更改格式为chapter+数字
                number_match = re.match(r'^(\d+)(.*)', line)
                if number_match:
                    chapter_number = number_match.group(1)
                    format_line = f'Chapter {chapter_number}'
                    content_dict[line] = format_line
                    format_content.append(format_line)
                # 如果出现英文，统一格式化
                engLine = eng_format(line)
                if not engLine == line:
                    content_dict[line] = engLine
                    format_content.append(engLine)
                content_result.append(line)
            continue

        # 如果在正文部分，记录内容
        if in_text:
            for content in content_result:
                if content.lower() == line.lower():
                    # 正式开始记录正文，避免目录下，章节前的无用信息
                    in_textTure = True
                    break
            # 排除需要忽略的文章内容
            if re.match(ignore_pattern, line, re.IGNORECASE):
                in_textTure = False
            # 排除============部分
            if line == "==================================================":
                in_textTure = False
            # 判断正文结束
            if re.match(end_pattern, line, re.IGNORECASE):
                break
        if in_textTure:
            if line in content_dict:
                    # and content_dict[line]:
                # 保存章节题目为格式化之后的题目
                result.append(content_dict[line])
            else:
                result.append(line)
            index += 1

    # content_file = os.path.join(content_path, file_name)
    # with open(content_file, 'w', encoding='utf-8') as file:
    # #     # file.write('\n'.join(content_result))
    #     file.write('\n'.join(content_result))
    # format_file = os.path.join(format_path, file_name)
    # with open(format_file, 'w', encoding='utf-8') as file:
    #     file.write('\n'.join(format_content))
    return index, '\n'.join(result)  # 将处理后的内容合并为一个字符串


if __name__ == '__main__':
    # 输入文件夹路径
    folder_path = 'D:/01YIHAO/小说txt/liout'
    # folder_path = 'D:/01YIHAO/project/novels/format/test_novel'
    # 输出文件夹路径
    output_path = 'D:/01YIHAO/project/novels/format/out_novel'

    content_path = 'D:/01YIHAO/project/novels/format/content_path'
    format_path = 'D:/01YIHAO/project/novels/format/format_path'

    # 如果输出文件夹不存在，创建它
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    else:
        # 存在，清空输出文件夹中的所有文件
        for file_name in os.listdir(output_path):
            file_path = os.path.join(output_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        # for file_name in os.listdir(content_path):
        #     file_path = os.path.join(content_path, file_name)
        #     if os.path.isfile(file_path):
        #         os.remove(file_path)
        # for file_name in os.listdir(format_path):
        #     file_path = os.path.join(format_path, file_name)
        #     if os.path.isfile(file_path):
        #         os.remove(file_path)
    sum = 0
    # 遍历输入文件夹中的所有文件
    files = os.listdir(folder_path)
    for file_name in files:
        if file_name.endswith('txt'):  # 只处理txt文件
            index = 0
            file_path = os.path.join(folder_path, file_name)
            index, processed_content = process_text(index , file_path)  # 处理文件内容

            if not processed_content.strip() or index <= 150:
                continue
            # 保存处理后的内容到输出文件夹
            output_file = os.path.join(output_path, file_name)
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(processed_content)
            print(f"Processed content saved to {output_file}")
            sum += 1
    print(f"共格式化{sum}个文件")