## 输出读取错误的文件


import os

def copy_non_empty_files(folder_path, test_path, output_path):
    # 确保输出文件夹存在
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # 遍历folder_path中的所有文件
    files = os.listdir(folder_path)
    for file_name in files:
        # 构造folder_path和test_path中的文件路径
        folder_file_path = os.path.join(folder_path, file_name)
        test_file_path = os.path.join(test_path, file_name)
        output_file_path = os.path.join(output_path, file_name)

        # 检查文件是否为空
        if os.path.getsize(folder_file_path) == 0:
            # 如果文件为空，从test_path中复制文件到output_path
            with open(test_file_path, 'r', encoding='utf-8') as test_file, \
                 open(output_file_path, 'w', encoding='utf-8') as output_file:
                content = test_file.read()
                output_file.write(content)
            print(f"Copied {file_name} from {test_path} to {output_path}")
        else:
            print(f"File {file_name} in {folder_path} is not empty, skipping.")

# 指定文件夹路径
folder_path = 'D:/01YIHAO/project/novels/format/out_novel'
test_path = 'D:/01YIHAO/小说txt/liout'
output_path = 'D:/01YIHAO/project/novels/format/question_novel'

# 调用函数
copy_non_empty_files(folder_path, test_path, output_path)