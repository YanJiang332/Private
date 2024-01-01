import os
import re
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils.dataframe import dataframe_to_rows
from textfsm import TextFSM
from pprint import pprint
import codecs


# Get the current script directory

# print(os.getcwd())

with open(f'display_interface.template') as f:
    template = TextFSM(f)

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


def get_table_data_port(paragraph):
    """
    从文件内容中获取表格数据
    """

    if paragraph is not None:
        entries = paragraph.split("***")
        table_data = []
        for entry in entries:
            if not entry.strip():
                continue
            data = {"Device name": "", "Device ip": "", "VSI Name": "N/A", "PW Signaling": "N/A", "VSI State": "N/A",
                    "VSI ID": "N/A", "Interface Name": [], "Interface State": [], "Ac Block State": []}
            lines = entry.split("\n")
            # print(lines)
            for line in lines:
                parts = line.split(" : ")
                if len(parts) == 2:
                    field_name = parts[0].strip()
                    field_value = parts[1].strip()
                    if field_name == "VSI Name":
                        data["VSI Name"] = field_value
                    elif field_name == "PW Signaling":
                        data["PW Signaling"] = field_value
                    elif field_name == "VSI State":
                        data["VSI State"] = field_value
                    elif field_name == "VSI ID":
                        data["VSI ID"] = field_value
                        data["Export"] = field_value
                    elif field_name == "Interface Name":
                        data["Interface Name"].append(field_value)
                    elif field_name == "State":
                        data["Interface State"].append(field_value)
                    elif field_name == "Ac Block State":
                        data["Ac Block State"].append(field_value)
        #     table_data.append(data)
        # return table_data

            # 分别处理 Peer Ip Address 和 PW Last Up Time，将其拆分为多个字段
            for i in range(max(len(data["Interface Name"]), len(data["Interface State"]), len(data["Ac Block State"]))):
                new_data = data.copy()
                new_data["Interface Name"] = data["Interface Name"][i] if i < len(
                    data["Interface Name"]) else ""
                new_data["Interface State"] = data["Interface State"][i] if i < len(
                    data["Interface State"]) else ""
                new_data["Ac Block State"] = data["Ac Block State"][i] if i < len(
                    data["Ac Block State"]) else ""
                table_data.append(new_data)
        return table_data


def get_table_data_l2vc(paragraph):
    """
    从文件内容中获取表格数据
    """
    if paragraph is not None:
        # print(paragraph)
        entries = paragraph.split("*")
        table_data = []
        for entry in entries:
            # print(entry)
            if not entry.strip():
                continue
            data = {"Device name": "", "Device ip": "", "Interface": "N/A", "AC status": "N/A", "VC State": "N/A",
                    "VC ID": "N/A", "VC Type": "N/A", "session state": "N/A", "Destination": "N/A", "link state": "N/A"}
            lines = entry.split("\n")
            # print(lines)
            for line in lines:
                parts = line.split(" : ")
                if len(parts) == 2:
                    field_name = parts[0].strip()
                    field_value = parts[1].strip()
                    if field_name == "Client Interface":
                        data["Interface"] = field_value
                    elif field_name == "AC status":
                        data["AC status"] = field_value
                    elif field_name == "VC State":
                        data["VC State"] = field_value
                    elif field_name == "VC ID":
                        data["VC ID"] = field_value
                    elif field_name == "VC Type":
                        data["VC Type"] = field_value
                    elif field_name == "session state":
                        data["session state"] = field_value
                    elif field_name == "Destination":
                        data["Destination"] = field_value
                    elif field_name == "link state":
                        data["link state"] = field_value
            table_data.append(data)
            # print(table_data)
        return table_data


def get_table_data(paragraph):
    """
    从文件内容中获取表格数据
    """
    if paragraph is not None:
        entries = paragraph.split("***")
        table_data = []
        for entry in entries:
            # print(entry)
            if not entry.strip():
                continue
            data = {"Device name": "", "Device ip": "", "VSI Name": "N/A", "PW Signaling": "N/A", "VSI State": "N/A",
                    "VSI ID": "N/A", "Peer Ip Address": [], "PW Last Up Time": []}
            lines = entry.split("\n")
            for line in lines:
                parts = line.split(" : ")
                if len(parts) == 2:
                    field_name = parts[0].strip()
                    field_value = parts[1].strip()
                    if field_name == "VSI Name":
                        data["VSI Name"] = field_value
                    elif field_name == "PW Signaling":
                        data["PW Signaling"] = field_value
                    elif field_name == "VSI State":
                        data["VSI State"] = field_value
                    elif field_name == "VSI ID":
                        data["VSI ID"] = field_value
                        data["Export"] = field_value
                    elif field_name == "*Peer Ip Address":
                        data["Peer Ip Address"].append(field_value)
                    elif field_name == "PW Last Up Time":
                        data["PW Last Up Time"].append(field_value)
            # table_data.append(data)
        # return table_data

            # 分别处理 Peer Ip Address 和 PW Last Up Time，将其拆分为多个字段
            for i in range(max(len(data["Peer Ip Address"]), len(data["PW Last Up Time"]))):
                new_data = data.copy()
                new_data["Peer Ip Address"] = data["Peer Ip Address"][i] if i < len(
                    data["Peer Ip Address"]) else ""
                new_data["PW Last Up Time"] = data["PW Last Up Time"][i] if i < len(
                    data["PW Last Up Time"]) else ""
                table_data.append(new_data)
        # print(table_data)
        return table_data


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


def process_file(filename):
    try:
        with codecs.open(filename, 'r', encoding='utf-16') as file:
            file_data = file.read()
    except UnicodeError:
        with codecs.open(filename, 'r', encoding='utf-8') as file:
            file_data = file.read()

            device_name, device_ip = get_device_info(file_data)
            paragraph_vsi = find_matching_paragraphs(
                file_data, device_name, 'display vsi verbose')
            paragraph_l2vc = find_matching_paragraphs(
                file_data, device_name, 'display mpls l2vc brief')
            paragraph_interface = find_matching_paragraphs(
                file_data, device_name, 'display interface')
            # print(paragraph_interface)
    
            data_list_peer = get_table_data(paragraph_vsi)
            if data_list_peer is not None:
                for data in data_list_peer:
                    data["Device name"] = device_name
                    data["Device ip"] = device_ip
    
            data_list_port = get_table_data_port(paragraph_vsi)
            if data_list_port is not None:
                for data in data_list_port:
                    data["Device name"] = device_name
                    data["Device ip"] = device_ip
    
            data_list_l2vc = get_table_data_l2vc(paragraph_l2vc)
            if data_list_l2vc is not None:
                for data in data_list_l2vc:
                    data["Device name"] = device_name
                    data["Device ip"] = device_ip

        return data_list_peer, data_list_port, data_list_l2vc



def main():
    # script_path = '.'  # replace with your script path
    table_header_interface = ["Device name", "Device ip", "VSI Name", "PW Signaling",
                              "VSI State", "VSI ID", "Interface Name", "Interface State", "Ac Block State"]
    table_data_interface = []

    table_header_l2vc = ["Device name", "Device ip", "Interface", "AC status", "VC State",
                         "VC ID", "VC Type", "session state", "Destination", "link state"]
    table_data_l2vc = []

    table_header = ["Device name", "Device ip", "VSI Name", "PW Signaling",
                    "VSI State", "VSI ID", "Peer Ip Address", "PW Last Up Time"]
    table_data = []

    script_path = os.getcwd()
    files = get_all_files(script_path)
    for filename in files:
        data_list_peer, data_list_port, data_list_l2vc = process_file(filename)
        if data_list_peer is not None:
            table_data.extend(data_list_peer)
        if data_list_port is not None:
            table_data_interface.extend(data_list_port)
        if data_list_l2vc is not None:
            table_data_l2vc.extend(data_list_l2vc)

    # pprint(table_data)

    # #
    df1 = pd.DataFrame(table_data, columns=table_header)
    df2 = pd.DataFrame(table_data_interface, columns=table_header_interface)
    df3 = pd.DataFrame(table_data_l2vc, columns=table_header_l2vc)
    excel_file = os.path.join(script_path, 'VSI and L2vc State.xlsx')
    with pd.ExcelWriter(excel_file) as writer:
        df1.to_excel(writer, sheet_name='Vsi peer status', index=False)
        df2.to_excel(writer, sheet_name='Vsi Interface status', index=False)
        df3.to_excel(writer, sheet_name='L2vc status', index=False)

if __name__ == '__main__':
    main()
