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
        #     table_data.append(data)
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


def main():
    # Get all subfolders in the current directory
    # folders = os.listdir()
    # print(folders)

    # 初始化表头和空数据
    table_header = ["Device name", "Device ip", "VSI Name", "PW Signaling",
                    "VSI State", "VSI ID", "Peer Ip Address", "PW Last Up Time"]
    table_data = []

    # Loop over root folder and all subfolders
    # for folder in folders:
    script_path = os.getcwd()
    # print(script_path)
    for folder_path, subfolders, files in os.walk(script_path):
        # print(files)
        for filename in files:
            # Check if file name ends with ".txt"
            if filename.endswith((".txt", ".log")):
                # Open file and read data
                with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                    file_data = file.read()
                    # print(file_data)
                    # 获取设备名称和设备IP地址
                    device_name, device_ip = get_device_info(file_data)

                    paragraph = find_matching_paragraphs(
                        file_data, device_name)
                    # 获取表格数据
                    data_list = get_table_data(paragraph)
                    if data_list is not None:
                        for data in data_list:
                            data["Device name"] = device_name
                            data["Device ip"] = device_ip
                            table_data.append(data)
    # pprint(table_data)

    # 将数据写入 Pandas DataFrame
    df = pd.DataFrame(table_data, columns=table_header)
    # print(df)

    excel_file = os.path.join(script_path, 'pw peer state.xlsx')  # Excel 文件路径
    with pd.ExcelWriter(excel_file) as writer:
        df.to_excel(writer, index=False)


if __name__ == '__main__':
    main()
