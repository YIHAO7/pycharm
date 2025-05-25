import re

# 定义字符串
text = "Acknowledgments"

# 定义正则表达式模式
end_pattern = r"\b(?:index|epilogue|acknowledgments)\b"

# 使用 re.search() 检查是否匹配
if re.search(end_pattern, text, re.IGNORECASE):
    print("匹配到换行符")
else:
    print("没有匹配到换行符")