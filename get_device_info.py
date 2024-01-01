import os
import re
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils.dataframe import dataframe_to_rows
from pprint import pprint
import codecs


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
    if device_name:
        pattern = rf'<{re.escape(device_name)}>'
        paragraphs = re.split(pattern, content)
        for paragraph in paragraphs:
            if search in paragraph:
                return paragraph

def get_table_data(paragraph, field_name_list, split_char, name_field):
    if paragraph is not None:
        entries = paragraph.split(split_char)
        table_data = []
        for entry in entries:
            if not entry.strip():
                continue
            data = {"Device name": "", "Device ip": ""}
            data[name_field] = "N/A"
            for field_name in field_name_list:
                data[field_name] = "N/A"
            lines = entry.split("\n")
            for line in lines:
                parts = line.split(" : ")
                if len(parts) == 2:
                    field_name = parts[0].strip()
                    field_value = parts[1].strip()
                    if field_name in field_name_list:
                        data[field_name] = field_value
                    elif field_name == name_field:
                        data[name_field] = field_value
            table_data.append(data)
        return table_data

def process_file(filename):
    try:
        with codecs.open(filename, 'r', encoding='utf-16') as file:
            file_data = file.read()
    except UnicodeError:
        with codecs.open(filename, 'r', encoding='utf-8') as file:
            file_data = file.read()

    device_name, device_ip = get_device_info(file_data)
    paragraph_vsi = find_matching_paragraphs(file_data, device_name, 'display vsi verbose')
    paragraph_l2vc = find_matching_paragraphs(file_data, device_name, 'display mpls l2vc brief')
    
    data_list_peer = get_table_data(paragraph_vsi, ["VSI Name", "PW Signaling", "VSI State", "VSI ID"],
                                    "***", "Peer Ip Address")
    data_list_port = get_table_data(paragraph_vsi, ["Interface Name", "State", "Ac Block State", "Export"],
                                    "***", "VSI Name")
    data_list_l2vc = get_table_data(paragraph_l2vc, ["Interface", "AC status", "VC State", "VC ID", "VC Type", "session state", "Destination", "link state"],
                                    "*", "Interface")

    for data in data_list_peer:
        data["Device name"] = device_name
        data["Device ip"] = device_ip
    for data in data_list_port:
        data["Device name"] = device_name
        data["Device ip"] = device_ip
    for data in data_list_l2vc:
        data["Device name"] = device_name
        data["Device ip"] = device_ip

    return data_list_peer, data_list_port, data_list_l2vc

def main():
    table_header_interface = ["Device name", "Device ip", "VSI Name", "PW Signaling", "VSI State", "VSI ID", "Interface Name", "Interface State", "Ac Block State"]
    table_data_interface = []

    table_header_l2vc = ["Device name", "Device ip", "Client Interface", "AC status", "VC State", "VC ID", "VC Type", "session state", "Destination", "link state"]
    table_data_l2vc = []

    table_header = ["Device name", "Device ip", "VSI Name", "PW Signaling", "VSI State", "VSI ID", "Peer Ip Address", "PW Last Up Time"]
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

    pprint(table_data)

    # df1 = pd.DataFrame(table_data, columns=table_header)
    # df2 = pd.DataFrame(table_data_interface, columns=table_header_interface)
    # df3 = pd.DataFrame(table_data_l2vc, columns=table_header_l2vc)
    # excel_file = os.path.join(script_path, 'VSI and L2vc State.xlsx')
    # with pd.ExcelWriter(excel_file) as writer:
    #     df1.to_excel(writer, sheet_name='Vsi peer status', index=False)
    #     df2.to_excel(writer, sheet_name='Vsi Interface status', index=False)
    #     df3.to_excel(writer, sheet_name='L2vc status', index=False)

if __name__ == '__main__':
    main()