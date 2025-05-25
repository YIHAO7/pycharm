import re


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
