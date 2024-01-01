

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
    for line in file_data.split("\n"):
        if line.startswith("sysname "):
            device_name = line.split()[1]
            # print(device_name)
            break
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


def process_data(data):
    eth_trunks = {}
    for item in data:
        if '.' not in item[0]:
            # print(item)
            if item[0].startswith('Eth-Trunk'):
                eth_trunks[item[0]] = []
            elif len(eth_trunks) > 0 and list(eth_trunks.keys())[-1].startswith('Eth-Trunk'):
                list(eth_trunks.values())[-1].append(item[0])
            else:
                eth_trunks[item[0]] = []
    return eth_trunks


def format_result(eth_trunks):
    result = []
    for key, values in eth_trunks.items():
        if values:
            for value in values:
                result.append([key, value])
        else:
            result.append(['N/A', key])
    return result


def remove_brackets_from_interfaces(result):
    for item in result:
        item[1] = re.sub(r'\(.*?\)', '', item[1])
    return result


# 使用函数
def interface_brief(script_path):
    interface_template_path = './template/display_interface_brief.template'
    lldp_template_path = './template/display_lldp_neighbor_brief.template'
    interface_data = []
    files = get_all_files(script_path)
    for filename in files:
        print(filename)
        content = read_file_with_fallback(filename)
        if content is None:  # 如果文件内容为None，表示不符合预期格式，跳过执行下一个文件
            continue
        device_name, device_ip = get_device_info(content)
        paragraphs = find_matching_paragraphs(
            content, device_name, "display interface brief")
        # if paragraphs is not None:
        #   print(paragraphs)
        raw_result = paragraphs.split('GigabitEthernet0/0/0')
        data = parse_data_with_template(interface_template_path, raw_result[0])
        data1 = parse_data_with_template(
            interface_template_path, raw_result[1])
        eth_trunks = process_data(data)
        eth_trunks1 = process_data(data1)
        eth_trunk_port = format_result(eth_trunks)
        eth_trunk_port1 = format_result(eth_trunks1)
        interface_port = remove_brackets_from_interfaces(
            eth_trunk_port + eth_trunk_port1)

        lldp_paragraphs = find_matching_paragraphs(
            content, device_name, "display lldp neighbor brief")
        lldp_data = parse_data_with_template(
            lldp_template_path, lldp_paragraphs)
        lldp_dict = {item[0]: item[1:] for item in lldp_data}
        # print(lldp_dict)

        for item in interface_port:
            if item[1] in lldp_dict:
                item.extend(lldp_dict[item[1]])
            item.insert(0, device_name)
        interface_data.append(interface_port)
    # return interface_data

    data = [item for sublist in interface_data for item in sublist]
    # pprint(data)
    table_header = ['Device', 'Eth-Trunk', 'Interface', 'Neighbor Device', 'Neighbor Interface']
    df = pd.DataFrame(data, columns=table_header)
    # print(df)
    excel_file = os.path.join(script_path, 'LLDP Interface State.xlsx')
    with pd.ExcelWriter(excel_file) as writer:
        df.to_excel(writer, index=False)


if __name__ == '__main__':
    interface_brief(script_path)
