

# from textfsm import TextFSM
# from pprint import pprint


# raw_result = '''
# display health
# --------------------------------------------------------------------
# Slot                           CPU Usage  Memory Usage(Used/Total)
# --------------------------------------------------------------------
# 17          MPU(Master)             3%          19%   6093MB_30708MB
# 1           LPU                    12%          30%   4679MB/15496MB
# 2           LPU                     3%          25%   3878MB/15496MB
# 6           LPU                     3%          24%   3824MB/15496MB
# 7           LPU                    11%          30%   4689MB/15496MB
# 19          SFU                     0%          19%    359MB/1843MB
# 20          SFU                     0%          19%    359MB/1843MB
# 21          SFU                     1%          19%    359MB/1843MB
# 22          SFU                     1%          19%    359MB/1843MB
# 18          MPU(Slave)              2%          16%   4915MB/30708MB
# '''


# with open(f'./template/cpu_mem_health.template') as f:
#     template = TextFSM(f)
#     print(template)
#     data = template.ParseText(raw_result)
#     print(data)


from textfsm import TextFSM
from pprint import pprint
import re
import os
import pandas as pd


script_path = os.getcwd()


def get_all_files(script_path):
    # 当前工作目录下所有子文件夹的名称组成的列表
    folders = [folder for folder in os.listdir(
        script_path) if os.path.isdir(os.path.join(script_path, folder))]
    files = []
    for folder in folders:
        root_folder_path = os.path.join(script_path, folder)
        for folder_path, subfolders, filenames in os.walk(root_folder_path):
            for filename in filenames:
                if filename.endswith((".txt", ".log")):
                    files.append(os.path.join(folder_path, filename))
    return files


def read_file_with_fallback(file_path, fallback_encoding='utf-16'):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # 如果UTF-8打开失败，则尝试使用指定的回退编码
        with open(file_path, 'r', encoding=fallback_encoding) as f:
            content = f.read()
            # print(content)
    # 检查文件内容是否包含需要的关键字和分隔符
    if "sysname " not in content or "router id" not in content or "<" not in content:
        return None  # 返回None表示文件内容不符合预期格式
    else:
        return content


def get_device_info(file_data):
    """
    从文件内容中获取设备名称和设备IP地址
    """
    device_name = ""
    device_ip = ""
    if file_data:
        for line in file_data.split("\n"):
            if line.startswith("sysname "):
                device_name = line.split()[1]
                # print(device_name)
            if line.startswith("router id"):
                device_ip = line.split()[2]
                break
        return device_name, device_ip
    

def find_matching_paragraphs(content, device_name, search):
    # paragraphs = re.split(rf'<{device_name}>', content)
    if device_name:
        pattern = r'<{}>'.format(device_name)
        paragraphs = re.split(pattern, content)
        for paragraph in paragraphs:
            if search in paragraph:
                # print(paragraph)

                return paragraph


def parse_data_with_template(template_path, raw_result):
    with open(template_path) as f:
        template = TextFSM(f)
        data = template.ParseText(raw_result)
    return data


def cpu_mem(script_path):
    cpu_mem_template_path = './template/cpu_mem_health.template'
    cpu_mem_data = []
    files = get_all_files(script_path)
    for filename in files:
        content = read_file_with_fallback(filename)
        if content:
            device_name, device_ip = get_device_info(content)
            # print(device_ip)
            paragraphs = find_matching_paragraphs(content, device_name, "display health")
            data = parse_data_with_template(cpu_mem_template_path, paragraphs)
            for item in data:
                item.insert(0, device_name)
                item.insert(1, device_ip)
            # data.insert(0, device_name)
            cpu_mem_data.append(data)
            # pprint(data)

    data = [item for sublist in cpu_mem_data for item in sublist]
    pprint(data)
    # table_header = ['device_name', 'device_ip','Slot', 'TYPE', 'CPU', 'MEM', 'USED', 'TOTAL']
    # df = pd.DataFrame(data, columns=table_header)
    # print(df)
    # excel_file = os.path.join(script_path, 'cpu_mem_usage.xlsx')
    # with pd.ExcelWriter(excel_file) as writer:
    #     df.to_excel(writer, index=False)



if __name__ == '__main__':
    cpu_mem(script_path)

