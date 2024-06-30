
x = '''
#
interface Eth-Trunk100.3457
 statistic enable
 encapsulation dot1q-termination
 dot1q termination vid 3457
 traffic-policy QOS_O&M inbound
 trust upstream PTCL-MSC
 l2 binding vsi NMS-Taxila
 qos phb disable
#
interface Eth-Trunk99.3488
#
interface Eth-Trunk99.3457
 vlan-type dot1q 3489
 ip binding vpn-instance nms-access
 ip address 10.140.7.149 255.255.255.253
 statistic enable
 traffic-policy QOS_O&M inbound
 trust upstream PTCL-MSC
 qos phb disable
 '''


y = '''
#
interface Eth-Trunk99.3457
 statistic enable
 encapsulation dot1q-termination
 dot1q termination vid 3458
 traffic-policy QOS_O&M inbound
 trust upstream PTCL-MSC
 l2 binding vsi NMS-Taxila
 qos phb disable
#
interface Eth-Trunk100.3488
 statistic enable
 encapsulation dot1q-termination
 dot1q termination vid 3489
 trust upstream PTCL-MSC
 l2 binding vsi vpls-north-cx-taxla-hsi
 qos phb disable
#
interface Eth-Trunk99.3489
 vlan-type dot1q 3489
 ip binding vpn-instance nms-access
 ip address 10.140.7.149 255.255.255.252
 statistic enable
 traffic-policy QOS_O&M inbound
 trust upstream PTCL-MSC
 qos phb disable
 '''




interface_mapping = {
    "Eth-Trunk99.3457": "Eth-Trunk99.3489",
    "Eth-Trunk100.3457": "Eth-Trunk99.3457"
    # 添加其他接口映射
}


# old_router_config = {}
# router_config = x.strip().split('#')
# for old_router_config_str in router_config:
#     # print(old_router_config_str)
#     line = old_router_config_str.strip().split('\n', 1)
#     if line[0].startswith('interface'):  
#         # print(line[0])  
#         interface_name = line[0].split()[1]
#         old_router_config[interface_name] = {}
#         old_router_config[interface_name] = line[1]
# # print(old_router_config)

# new_router_config = {}
# router_config02 = y.strip().split('#')
# for new_router_config_str in router_config02:
#     # print(old_router_config_str)   
#     line = new_router_config_str.strip().split('\n', 1)
#     if line[0].startswith('interface'):  
#         # print(line[0])  
#         interface_name = line[0].split()[1]
#         new_router_config[interface_name] = {}
#         new_router_config[interface_name] = line[1]
# # print(new_router_config)


# # 比较配置
# for key in old_router_config:
#     if key in interface_mapping:
#         new_key = interface_mapping[key]
#         if old_router_config[key] != new_router_config.get(new_key):
#             print(f"接口 {key} 的配置不匹配：")
#             print(f"旧路由器配置：{old_router_config[key]}")
#             print(f"新路由器配置：{new_router_config.get(new_key)}")

import tkinter as tk
from tkinter import filedialog
import re 
import pandas as pd
from pprint import pprint

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
    

def find_matching_paragraphs(file_path, search):
    content = read_file_with_fallback(file_path)
    device_name, device_ip = get_device_info(content)
    if device_name:
        pattern = r'<{}>'.format(device_name)
        paragraphs = re.split(pattern, content)
        for paragraph in paragraphs:
            if search in paragraph:
                # print(paragraph)

                return paragraph

def compare_interface_configs(old_config, new_config, interface_mapping):
    old_router_config = {}
    router_config = old_config.strip().split('#')
    for old_router_config_str in router_config:
        line = old_router_config_str.strip().split('\n', 1)
        # print(line)
        if line[0].startswith(f'interface'): 
            # print(line) 
            interface_name = line[0].split()[1]
            old_router_config[interface_name] = {}
            if len(line) > 1:
                old_router_config[interface_name] = line[1]
            else:
                old_router_config[interface_name] = ''
    # pprint(old_router_config)

    new_router_config = {}
    router_config02 = new_config.strip().split('#')
    for new_router_config_str in router_config02:
        line = new_router_config_str.strip().split('\n', 1)
        # print(line)
        if line[0].startswith('interface'):  
            interface_name = line[0].split()[1]
            new_router_config[interface_name] = {}
            if len(line) > 1:
                new_router_config[interface_name] = line[1]
            else:
                new_router_config[interface_name] = ''

    results = ""
    for key in old_router_config:
        if key in interface_mapping:
            new_key = interface_mapping[key]
            if old_router_config[key] != new_router_config.get(new_key):
                result = f"接口 {key} 的配置不匹配：\n"
                result += f"旧配置：{old_router_config[key]}\n"
                result += f"接口 {new_key} 的配置不匹配：\n"
                result += f"新配置：{new_router_config.get(new_key)}\n"
                result += "==" * 20 + "\n\n"
                results += result
    return results
                

# def main():
#     # 弹出文件选择窗口，让用户选择旧路由器配置文件
#     root = tk.Tk()
#     root.withdraw()
#     old_file_path = filedialog.askopenfilename(title="选择旧配置文件", filetypes=[("Text Files", "*.txt")])

#     # 弹出文件选择窗口，让用户选择新路由器配置文件
#     new_file_path = filedialog.askopenfilename(title="选择新配置文件", filetypes=[("Text Files", "*.txt")])

#     # 弹出文件选择窗口，让用户选择接口映射文件  [("Excel Files", "*.xlsx")]
#     interface_mapping_path = filedialog.askopenfilename(title="选择接口映射文件", filetypes=[("Excel Files", "*.xlsx")])

#     old_config = find_matching_paragraphs(old_file_path, 'display current-configuration')
#     new_config = find_matching_paragraphs(new_file_path, 'display current-configuration')
#     # interface_mapping = {}
#     # print(interface_mapping)
#     df = pd.read_excel(interface_mapping_path)
#     # print(df)
#     interface_mapping = dict(zip(df['old port'], df['new port']))
#     # print(interface_mapping)
#     # with open(interface_mapping_path, "r") as f:
#     # for line in f:
#     #     print(line)
#     #     old_interface, new_interface = line.strip().split(",")
#     #     interface_mapping[old_interface] = new_interface
#     results = compare_interface_configs(old_config, new_config, interface_mapping)
#     print(results)


if __name__ == '__main__':
    # main()
    print(compare_interface_configs(x, y, interface_mapping))