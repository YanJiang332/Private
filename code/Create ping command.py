
from textfsm import TextFSM
from pprint import pprint
import tkinter as tk
from tkinter import filedialog
import codecs
import datetime
import re
import os
from tkinter import Tk, filedialog


def check_expiration():
    expiration_date = datetime.datetime(2024, 5, 1)

    # 获取当前日期
    current_date = datetime.datetime.now()

    if current_date > expiration_date:
        print("不能继续执行。")
        return False
    else:
        return True

def get_all_files(script_path):
    # 当前工作目录下所有子文件夹的名称组成的列表
    # folders = [folder for folder in os.listdir(script_path) if os.path.isdir(os.path.join(script_path, folder))]
    files = []
    # for folder in folders:
    #     root_folder_path = os.path.join(script_path, folder)
    for folder_path, subfolders, filenames in os.walk(script_path):
        for filename in filenames:
            if filename.endswith((".txt", ".log")):
                files.append(os.path.join(folder_path, filename))
    return files


def get_device_info(file_data):
    """
    从文件内容中获取设备名称和设备IP地址
    """
    device_name = ""
    device_ip = ""
    for line in file_data.split("\n"):
        if line.startswith("sysname"):
            device_name = line.split()[1]
        if line.startswith("router id") or line.startswith("mpls lsr-id"):
            device_ip = line.split()[2]
            break
    device_name = device_name.replace('/', '-')      
    return device_name, device_ip


def find_matching_paragraphs(content, device_name, search):
    # paragraphs = re.split(rf'<{device_name}>', content)
    if device_name:
        pattern = rf'<{re.escape(device_name)}>'
        # print(pattern)
        paragraphs = re.split(pattern, content)
        # print(paragraphs)
        for paragraph in paragraphs:
            if search in paragraph:
                # print(paragraph)

                return paragraph


def parse_arp_info(raw_result):
    arp_info = []

    with open(f'./template/display_arp.template') as f:
        template = TextFSM(f)
        show_vlan_dict = template.ParseText(raw_result)
        arp_info.extend(show_vlan_dict)

    return arp_info


def generate_ping_commands(arp_info):
    # 创建一个字典用于存储源和目的的对应关系，按照接口进行分组
    interface_mapping = {}

    # 遍历ARP信息
    for entry in arp_info:
        ip_address = entry[0]
        mac_address = entry[1]
        expire = entry[2]
        arp_type = entry[3]
        interface = entry[4].strip()
        vpn_instance = entry[5].strip()

        # 判断是源还是目的
        source_dest_indicator = "I" if arp_type.startswith("I") else "D"

        # 将源和目的的对应关系添加到字典中，按接口分组
        if interface not in interface_mapping:
            interface_mapping[interface] = {"sources": {}, "destinations": {}}

        if source_dest_indicator == "I":
            # 忽略 vpn_instance 为 '__dcn_vpn__' 的情况
            if vpn_instance != '__dcn_vpn__':            
                interface_mapping[interface]["sources"][ip_address] = {
                    "vpn_instance": vpn_instance}
        elif source_dest_indicator == "D":
            # 忽略 vpn_instance 为 '__dcn_vpn__' 的情况
            if vpn_instance != '__dcn_vpn__':            
                interface_mapping[interface]["destinations"][ip_address] = {
                    "vpn_instance": vpn_instance}

    # 生成ping测试命令
    ping_commands = []
    for interface, mapping in interface_mapping.items():
        for source_ip, source_info in mapping["sources"].items():
            # 查找相应的目的
            destinations = mapping["destinations"]
            for dest_ip, dest_info in destinations.items():
                # 检查是否有相应的源，如果有则生成ping命令
                if source_ip == dest_ip:
                    continue  # 源和目的IP相同，跳过

                # 判断是否有 VPN 实例，决定是否包含 -vpn-instance
                vpn_instance_option = f"-vpn-instance {source_info['vpn_instance']}" if source_info['vpn_instance'] else ""

                ping_command = f"ping {vpn_instance_option} -a {source_ip} {dest_ip}"
                ping_commands.append(ping_command)
    ping_commands = sorted(ping_commands)
    return ping_commands

# # 使用示例
# raw_result = """
# # your raw result here
# """

# arp_info = parse_arp_info(raw_result)
# ping_commands = generate_ping_commands(arp_info)

# # 打印生成的ping命令
# pprint(arp_info)
# pprint(ping_commands)


def process_file(filename):
    try:
        with codecs.open(filename, 'r', encoding='utf-16') as file:
            file_data = file.read()
    except UnicodeError:
        with codecs.open(filename, 'r', encoding='utf-8') as file:
            file_data = file.read()

            device_name, device_ip = get_device_info(file_data)
            paragraph_arp = find_matching_paragraphs(
                file_data, device_name, 'display arp all')
        return paragraph_arp, device_name


def get_folder_path():
    root = Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title="Select Folder")
    return folder_path


def main():
    folder_path = get_folder_path()
    files = get_all_files(folder_path)

    # 获取当前时间
    now_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')

    for filename in files:
        paragraph_arp, device_name = process_file(filename)
        arp_info = parse_arp_info(paragraph_arp)
        ping_commands = generate_ping_commands(arp_info)

        # 获取文件夹路径
        output_folder = os.path.dirname(filename)
        # 创建 PING 文件夹
        ping_folder = os.path.join(output_folder, 'PING')
        os.makedirs(ping_folder, exist_ok=True)

        # 构建输出文件的完整路径
        output_file_path = os.path.join(ping_folder, f'ping_command {device_name} {now_time}.txt')
        print(output_file_path)

        # 打开文件并写入 ping 命令
        with open(output_file_path, 'w') as f:
            for ping in ping_commands:
                f.write(ping + '\n')


if __name__ == '__main__':
    if check_expiration():
        main()