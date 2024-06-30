import os
from tkinter import Tk, filedialog
import re
import datetime
from pprint import pprint
import codecs
import json
from textfsm import TextFSM
from sqlalchemy.orm import sessionmaker
from sqlite3_orm_create_table_device_info import Router, Interface, L2vc, Arp, Lldp, Bgp, Vsi, Vsi_peer, Vpn_instance, engine

Session = sessionmaker(bind=engine)
session = Session()


class DeviceDataExtractor:
    def __init__(self, file_data):
        self.file_data = file_data
        self.device_name, self.device_ip = self.get_device_info()

    def get_device_info(self):
        device_name, device_ip = "", ""
        for line in self.file_data.split("\n"):
            if line.startswith("sysname"):
                device_name = line.split()[1]
            if line.startswith("router id") or line.startswith("mpls lsr-id"):
                device_ip = line.split()[2]
                break
        return device_name, device_ip1

    def find_matching_paragraph(self, search):
        if self.device_name:
            pattern = rf'<{re.escape(self.device_name)}>'
            paragraphs = re.split(pattern, self.file_data)
            for paragraph in paragraphs:
                if search in paragraph:
                    return paragraph
        return None

    # @staticmethod
    # def parse_table_data(paragraph, fields):
    #     table_data = []
    #     if paragraph is not None:
    #         entries = paragraph.split("***")
    #         for entry in entries:
    #             if not entry.strip():
    #                 continue
    #             data = {field: [] for field in fields}
    #             lines = entry.split("\n")
    #             for line in lines:
    #                 parts = line.split(" : ")
    #                 if len(parts) == 2:
    #                     field_name = parts[0].strip()
    #                     field_value = parts[1].strip()
    #                     if field_name in data:
    #                         data[field_name].append(field_value)
    #             for i in range(max(len(data[field]) for field in fields)):
    #                 new_data = {field: data[field][i] if i < len(data[field]) else "" for field in fields}
    #                 table_data.append(new_data)
    #     return table_data

    @staticmethod
    def parse_table_data(paragraph, fields):
        table_data = []
        fields_lower = [field.lower() for field in fields]  # 转换为小写

        if paragraph is not None:
            entries = paragraph.split("***")
            for entry in entries:
                if not entry.strip():
                    continue
                data = {field: [] for field in fields_lower}
                lines = entry.split("\n")
                for line in lines:
                    parts = line.split(" : ")
                    if len(parts) == 2:
                        field_name = parts[0].strip().lower()  # 转换为小写
                        field_value = parts[1].strip()
                        if field_name in data:
                            data[field_name].append(field_value)

                prev_data = {}
                for i in range(max(len(data[field]) for field in fields_lower)):
                    new_data = {}
                    for field in fields:
                        lower_field = field.lower()
                        if i < len(data[lower_field]):
                            new_data[field] = data[lower_field][i]
                            prev_data[lower_field] = data[lower_field][i]
                        else:
                            new_data[field] = prev_data.get(lower_field, "")
                    table_data.append(new_data)
        return table_data

    def get_table_data_interface(self, paragraph):
        fields = ["Interface", "Physical State", "Protocol State", "Description", "ip_address", "Port_bw", "Port_max_bw", "Transceiver Mode",
                  "WaveLength", "Transmission Distance", "Rx Power", "Tx Power", "Last physical down time", "Input bandwidth", "Output bandwidth"]
        data_list_interface = []
        with open('../template/display_interface.template') as f:
            template = TextFSM(f)
        if paragraph is None:
            return []
        parsed_data = re.split(r'\n\n+', paragraph)
        for entry in parsed_data:
            interface_data = template.ParseText(entry)
            for item in interface_data:
                data_list_interface.append(dict(zip(fields, item)))
        return data_list_interface

    def get_table_data_info(self, raw_result):
        fields = ["IP ADDRESS", "MAC ADDRESS", "EXPIRE",
                  "TYPE", "INTERFACE", "VPN-INSTANCE"]
        arp_info = []
        with open('../template/display_arp.template') as f:
            template = TextFSM(f)
            show_arp_dict = template.ParseText(raw_result)

            headers = template.header
            arp_info = [dict(zip(headers, item)) for item in show_arp_dict]
            # for item in show_arp_dict:
            #     arp_info.append(dict(zip(fields, item)))
        return arp_info

    def get_table_lldp(self, raw_result):
        fields = ["Local_Port", "Peer_Port", "Peer_Device"]
        data_lldp = []
        try:
            with open('../template/display_lldp_neighbor.template', encoding='utf-8') as f:
                template = TextFSM(f)
                lldp = template.ParseText(raw_result)
                for item in lldp:
                    data_lldp.append(dict(zip(fields, item)))
            return data_lldp
        except Exception as e1:
            print(f"Error with template 1: {e1}")
        return []

    def get_table_bgp(self, raw_result):
        fields = ["peer", "version", "AS number", "status"]
        data_bgp = []
        with open('../template/display_bgp.template') as f:
            template = TextFSM(f)
            bgp = template.ParseText(raw_result)
            for item in bgp:
                data_bgp.append(dict(zip(fields, item)))
        return data_bgp

    def get_table_vpn(self, raw_result):
        # print(raw_result)
        vpn_blocks = re.split(r'\n\s*\n', raw_result.strip())
        # print(vpn_blocks)
        data_vpn_list = []
        for data_str in vpn_blocks:
            if 'VPN-Instance Name and ID' in data_str:
                vpn_instance_name_id = re.search(
                    r'VPN-Instance Name and ID : (.*)', data_str).group(1)
                interfaces = re.findall(
                    r'Interfaces : (.*)', data_str) + re.findall(r'               (.*)', data_str)
                route_distinguisher = re.search(
                    r'Route Distinguisher : (.*)', data_str).group(1)
                export_vpn_targets = re.search(
                    r'Export VPN Targets : (.*)', data_str).group(1)
                import_vpn_targets = re.search(
                    r'Import VPN Targets : (.*)', data_str).group(1)

                interfaces = [iface.strip(',') for iface in interfaces]
                # 定义数据
                data_vpn = {
                    "vpn_instance_name_id": vpn_instance_name_id,
                    "interfaces": interfaces,
                    "route_distinguisher": route_distinguisher,
                    "export_vpn_targets": export_vpn_targets,
                    "import_vpn_targets": import_vpn_targets
                }
                data_vpn_list.append(data_vpn)
        # print(data_vpn_list)
        return data_vpn_list

    def extract_data(self):
        data_dict = {'device_name': self.device_name,
                     'device_ip': self.device_ip}
        paragraph_vsi = self.find_matching_paragraph('display vsi verbose')
        paragraph_l2vc = self.find_matching_paragraph(
            'display mpls l2vc brief')
        paragraph_interface = self.find_matching_paragraph('display interface')
        paragraph_arp = self.find_matching_paragraph('display arp all')
        paragraph_lldp = self.find_matching_paragraph('display lldp neighbor')
        paragraph_bgp = self.find_matching_paragraph(
            'display bgp vpnv4 all peer')
        paragraph_vpn = self.find_matching_paragraph(
            'display ip vpn-instance verbose')

        data_dict['vsi_peer'] = self.parse_table_data(paragraph_vsi, [
                                                      "VSI Name", "PW Signaling", "VSI State", "VSI ID", "*Peer Ip Address", "PW Last Up Time"])
        data_dict['vsi'] = self.parse_table_data(paragraph_vsi, [
                                                 "VSI Name", "PW Signaling", "VSI State", "VSI ID", "Interface Name", "State", "Ac Block State"])
        data_dict['l2vc'] = self.parse_table_data(paragraph_l2vc, [
                                                  "Interface", "AC status", "VC state", "VC ID", "VC Type", "session state", "Destination", "link state"])
        data_dict['arp'] = self.get_table_data_info(paragraph_arp)
        data_dict['interface'] = self.get_table_data_interface(
            paragraph_interface)
        data_dict['lldp'] = self.get_table_lldp(paragraph_lldp)
        data_dict['bgp'] = self.get_table_bgp(paragraph_bgp)
        data_dict['vpn_instance'] = self.get_table_vpn(paragraph_vpn)
        # print(data_dict['vsi'])
        return data_dict


def check_expiration():
    expiration_date = datetime.datetime(2024, 7, 1)
    return datetime.datetime.now() <= expiration_date


def get_folder_path():
    root = Tk()
    root.withdraw()
    return filedialog.askdirectory(title="Select Folder")


def get_all_files(script_path):
    files = []
    for folder_path, _, filenames in os.walk(script_path):
        for filename in filenames:
            if filename.endswith((".txt", ".log")):
                files.append(os.path.join(folder_path, filename))
    return files


def process_file(filename):
    try:
        with codecs.open(filename, 'r', encoding='utf-8') as file:
            file_data = file.read()
    except UnicodeError:
        with codecs.open(filename, 'r', encoding='utf-16') as file:
            file_data = file.read()

    extractor = DeviceDataExtractor(file_data)
    return extractor.extract_data()


def main():
    folder_path = get_folder_path()
    files = get_all_files(folder_path)

    for filename in files:
        data_dict = process_file(filename)

        router_device = Router(
            routername=data_dict['device_name'], ip=data_dict['device_ip'], routernamenew=data_dict['device_name'].replace('/', '-')
        )
        session.add(router_device)

        for interface in data_dict['interface']:
            # print(interface)
            rx_power_str = ','.join(map(str, interface['Rx Power']))
            tx_power_str = ','.join(map(str, interface['Tx Power']))
            device_interface = Interface(
                router=router_device,
                interface_name=interface['Interface'],
                Physical_State=interface['Physical State'],
                Protocol_State=interface['Protocol State'],
                Description=interface['Description'],
                ip_address=interface['ip_address'],
                Current_BW=interface['Port_bw'],
                Port_max_bw=interface['Port_max_bw'],
                Transceiver_Mode=interface['Transceiver Mode'],
                WaveLength=interface['WaveLength'],
                Transmission_Distance=interface['Transmission Distance'],
                Rx_Power=rx_power_str,  # 使用转换后的字符串
                Tx_Power=tx_power_str,  # 使用转换后的字符串
                # Rx_Power=','.join(interface['Rx Power']),
                # Tx_Power=','.join(interface['Tx Power']),
                Last_physical_down_time=interface['Last physical down time'],
                Input_bandwidth=interface['Input bandwidth'],
                Output_bandwidth=interface['Output bandwidth']
            )
            session.add(device_interface)

        for l2vc in data_dict['l2vc']:
            device_l2vc = L2vc(
                router=router_device,
                interface=l2vc['Interface'],
                AC_status=l2vc['AC status'],
                VC_State=l2vc['VC state'],
                VC_ID=l2vc['VC ID'],
                VC_Type=l2vc['VC Type'],
                session_state=l2vc['session state'],
                Destination=l2vc['Destination'],
                link_state=l2vc['link state']
            )
            session.add(device_l2vc)

        for arp in data_dict['arp']:
            device_arp = Arp(
                router=router_device,
                IP_ADDRESS=arp['IP_ADDRESS'],
                MAC_ADDRESS=arp['MAC_ADDRESS'],
                EXPIRE=arp['EXPIRE'],
                TYPE=arp['TYPE'],
                INTERFACE=arp['INTERFACE'],
                VPN_INSTANCE=arp['VPN_INSTANCE']
            )
            session.add(device_arp)

        for lldp in data_dict['lldp']:
            device_lldp = Lldp(
                router=router_device,
                Local_Port=lldp['Local_Port'],
                Peer_Port=lldp['Peer_Port'],
                Peer_Device=lldp['Peer_Device']
            )
            session.add(device_lldp)

        for bgp in data_dict['bgp']:
            device_bgp = Bgp(
                router=router_device,
                Peer=bgp['peer'],
                Version=bgp['version'],
                AS_number=bgp['AS number'],
                Peer_status=bgp['status']
            )
            session.add(device_bgp)

        for vsi in data_dict['vsi']:
            device_vsi = Vsi(
                router=router_device,
                VSI_Name=vsi['VSI Name'],
                PW_Signaling=vsi['PW Signaling'],
                VSI_State=vsi['VSI State'],
                VSI_ID=vsi['VSI ID'],
                Interface_Name=vsi['Interface Name'],
                Interface_State=vsi['State'],
                Ac_Block_State=vsi['Ac Block State']
            )
            session.add(device_vsi)

        for vsi_peer in data_dict['vsi_peer']:
            device_vsi_peer = Vsi_peer(
                router=router_device,
                VSI_Name=vsi_peer['VSI Name'],
                PW_Signaling=vsi_peer['PW Signaling'],
                VSI_State=vsi_peer['VSI State'],
                VSI_ID=vsi_peer['VSI ID'],
                Peer_Ip_Address=vsi_peer['*Peer Ip Address'],
                PW_Last_Up_Time=vsi_peer['PW Last Up Time']
            )
            session.add(device_vsi_peer)

        for vpn_instance in data_dict['vpn_instance']:
            interfaces_str = ''.join(map(str, vpn_instance['interfaces']))
            # print(interfaces_str)
            device_vpn_instance = Vpn_instance(
                router=router_device,
                vpn_instance_name=vpn_instance['vpn_instance_name_id'],
                interfaces=interfaces_str,
                # interfaces=vpn_instance['interfaces'],
                route_distinguisher=vpn_instance['route_distinguisher'],
                export_vpn_targets=vpn_instance['export_vpn_targets'],
                import_vpn_targets=vpn_instance['import_vpn_targets']
            )
            session.add(device_vpn_instance)

        session.commit()


if __name__ == '__main__':
    if check_expiration():
        main()
