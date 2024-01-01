import os
import re
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils.dataframe import dataframe_to_rows
from pprint import pprint

# Get the current script directory
script_path = os.getcwd()
# print(os.getcwd())


def get_device_info(file_data):
    """
    从文件内容中获取设备名称和设备IP地址
    """
    device_name = ""
    device_ip = ""
    for line in file_data.split("\n"):
        if line.startswith("sysname"):
            device_name = line.split()[1]
        if line.startswith("router id"):
            device_ip = line.split()[2]
        if line.startswith("mpls lsr-id"):
            device_ip = line.split()[2]
            break
    return device_name, device_ip


def find_matching_paragraphs(content, device_name):
    # paragraphs = re.split(rf'<{device_name}>', content)
    if device_name:
        pattern = r'<{}>'.format(device_name)
        paragraphs = re.split(pattern, content)
        for paragraph in paragraphs:
            if "display vsi verbose" in paragraph:
                # print(paragraph)

                return paragraph


def get_table_data(paragraph):
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
                    elif field_name == "Import vpn target":
                        data["Import"] = field_value
                    elif field_name == "Export vpn target":
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


def get_all_files(script_path):
    #当前工作目录下所有子文件夹的名称组成的列表
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
    with open(filename, 'r', encoding='utf-8') as file:
        file_data = file.read()
        device_name, device_ip = get_device_info(file_data)
        paragraph = find_matching_paragraphs(file_data, device_name)
        data_list = get_table_data(paragraph)
        if data_list is not None:
            for data in data_list:
                data["Device name"] = device_name
                data["Device ip"] = device_ip
    return data_list

def main():
    # script_path = '.'  # replace with your script path
    table_header = ["Device name", "Device ip", "VSI Name", "PW Signaling", "VSI State", "VSI ID", "Interface Name", "Interface State", "Ac Block State"]
    table_data = []

    files = get_all_files(script_path)
    for filename in files:
        data_list = process_file(filename)
        if data_list is not None:
            table_data.extend(data_list)
    # pprint(table_data)

    df = pd.DataFrame(table_data, columns=table_header)
    excel_file = os.path.join(script_path, 'VSI Interface State.xlsx')
    with pd.ExcelWriter(excel_file) as writer:
        df.to_excel(writer, index=False)

if __name__ == '__main__':
    main()
