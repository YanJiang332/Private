
import os
import re

def process_cfg_file(file_path):
    try:
        with open(file_path, 'r') as file:
            file_data = file.read()
            name = re.search(r'sysname\s+(.*)', file_data).groups()[0]

            # 定义替换规则
            replace_rules = {
                r'FTP client-source -a\s+([\d.]+)': 'FTP client-source -a LoopBack0',
                r'(rsa|ecc) peer-public-key.*?peer-public-key end\n\#\n': '',
                r'diffserv domain QoSCXRNCPolicy.*?#': '''diffserv domain NewQosPolicy
 8021p-inbound 0 phb be green  
 8021p-inbound 1 phb af1 green 
 8021p-inbound 3 phb af2 green       
 8021p-inbound 4 phb af3 green       
 8021p-inbound 5 phb af4 green       
 8021p-inbound 6 phb ef green        
 8021p-inbound 7 phb cs7 green       
 8021p-outbound be green map 0       
 8021p-outbound be yellow map 0      
 8021p-outbound be red map 0         
 8021p-outbound af1 green map 1      
 8021p-outbound af1 yellow map 1     
 8021p-outbound af1 red map 1        
 8021p-outbound af2 green map 3      
 8021p-outbound af2 yellow map 3     
 8021p-outbound af2 red map 3        
 8021p-outbound af3 green map 4      
 8021p-outbound af3 yellow map 4     
 8021p-outbound af3 red map 4        
 8021p-outbound af4 green map 5      
 8021p-outbound af4 yellow map 5     
 8021p-outbound af4 red map 5        
 8021p-outbound ef green map 6       
 8021p-outbound ef yellow map 6      
 8021p-outbound ef red map 6         
 8021p-outbound cs6 green map 6      
 8021p-outbound cs6 yellow map 6     
 8021p-outbound cs6 red map 6        
 8021p-outbound cs7 green map 7      
 8021p-outbound cs7 yellow map 7     
 8021p-outbound cs7 red map 7        
 ip-dscp-inbound 0 phb be green      
 ip-dscp-inbound 1 phb be green      
 ip-dscp-inbound 2 phb be green      
 ip-dscp-inbound 3 phb be green      
 ip-dscp-inbound 4 phb be green      
 ip-dscp-inbound 5 phb be green      
 ip-dscp-inbound 6 phb be green      
 ip-dscp-inbound 7 phb be green      
 ip-dscp-inbound 8 phb af1 green     
 ip-dscp-inbound 9 phb be green      
 ip-dscp-inbound 10 phb af1 green    
 ip-dscp-inbound 11 phb be green     
 ip-dscp-inbound 12 phb af1 yellow   
 ip-dscp-inbound 13 phb be green     
 ip-dscp-inbound 14 phb af1 red      
 ip-dscp-inbound 15 phb be green     
 ip-dscp-inbound 16 phb af2 green    
 ip-dscp-inbound 17 phb be green     
 ip-dscp-inbound 18 phb af2 green    
 ip-dscp-inbound 19 phb be green     
 ip-dscp-inbound 20 phb af2 yellow   
 ip-dscp-inbound 21 phb be green     
 ip-dscp-inbound 22 phb af2 red      
 ip-dscp-inbound 23 phb be green     
 ip-dscp-inbound 24 phb af3 green    
 ip-dscp-inbound 25 phb be green     
 ip-dscp-inbound 26 phb af3 green    
 ip-dscp-inbound 27 phb be green     
 ip-dscp-inbound 28 phb af3 yellow   
 ip-dscp-inbound 29 phb be green     
 ip-dscp-inbound 30 phb af3 red      
 ip-dscp-inbound 31 phb be green     
 ip-dscp-inbound 32 phb af4 green    
 ip-dscp-inbound 33 phb be green     
 ip-dscp-inbound 34 phb af4 green    
 ip-dscp-inbound 35 phb be green     
 ip-dscp-inbound 36 phb af4 yellow   
 ip-dscp-inbound 37 phb be green     
 ip-dscp-inbound 38 phb af4 red      
 ip-dscp-inbound 39 phb be green     
 ip-dscp-inbound 40 phb ef green     
 ip-dscp-inbound 41 phb be green     
 ip-dscp-inbound 42 phb be green     
 ip-dscp-inbound 43 phb be green     
 ip-dscp-inbound 44 phb be green     
 ip-dscp-inbound 45 phb be green     
 ip-dscp-inbound 46 phb ef green     
 ip-dscp-inbound 47 phb be green     
 ip-dscp-inbound 48 phb cs6 green    
 ip-dscp-inbound 49 phb be green     
 ip-dscp-inbound 50 phb be green     
 ip-dscp-inbound 51 phb be green     
 ip-dscp-inbound 52 phb be green     
 ip-dscp-inbound 53 phb be green     
 ip-dscp-inbound 54 phb be green     
 ip-dscp-inbound 55 phb be green     
 ip-dscp-inbound 56 phb cs7 green    
 ip-dscp-inbound 57 phb be green     
 ip-dscp-inbound 58 phb be green     
 ip-dscp-inbound 59 phb be green     
 ip-dscp-inbound 60 phb be green     
 ip-dscp-inbound 61 phb be green     
 ip-dscp-inbound 62 phb be green     
 ip-dscp-inbound 63 phb be green     
 ip-dscp-outbound be green map 0     
 ip-dscp-outbound be yellow map 0    
 ip-dscp-outbound be red map 0       
 ip-dscp-outbound af1 green map 10   
 ip-dscp-outbound af1 yellow map 12  
 ip-dscp-outbound af1 red map 14     
 ip-dscp-outbound af2 green map 18   
 ip-dscp-outbound af2 yellow map 20  
 ip-dscp-outbound af2 red map 22     
 ip-dscp-outbound af3 green map 26   
 ip-dscp-outbound af3 yellow map 28  
 ip-dscp-outbound af3 red map 30     
 ip-dscp-outbound af4 green map 34   
 ip-dscp-outbound af4 yellow map 36  
 ip-dscp-outbound af4 red map 38     
 ip-dscp-outbound ef green map 46    
 ip-dscp-outbound ef yellow map 46   
 ip-dscp-outbound ef red map 46      
 ip-dscp-outbound cs6 green map 48   
 ip-dscp-outbound cs6 yellow map 48  
 ip-dscp-outbound cs6 red map 48     
 ip-dscp-outbound cs7 green map 56   
 ip-dscp-outbound cs7 yellow map 56  
 ip-dscp-outbound cs7 red map 56     
 mpls-exp-inbound 0 phb be green     
 mpls-exp-inbound 1 phb af1 green    
 mpls-exp-inbound 3 phb AF2 green    
 mpls-exp-inbound 4 phb AF3 green    
 mpls-exp-inbound 5 phb AF4 green    
 mpls-exp-inbound 6 phb EF green     
 mpls-exp-inbound 7 phb cs7 green    
 mpls-exp-outbound be green map 0    
 mpls-exp-outbound be yellow map 0   
 mpls-exp-outbound be red map 0      
 mpls-exp-outbound af1 green map 1   
 mpls-exp-outbound af1 yellow map 1  
 mpls-exp-outbound af1 red map 1     
 mpls-exp-outbound AF2 green map 3   
 mpls-exp-outbound AF2 yellow map 3  
 mpls-exp-outbound AF2 red map 3     
 mpls-exp-outbound AF3 green map 4   
 mpls-exp-outbound AF3 yellow map 4  
 mpls-exp-outbound AF3 red map 4     
 mpls-exp-outbound AF4 green map 5   
 mpls-exp-outbound AF4 yellow map 5  
 mpls-exp-outbound AF4 red map 5     
 mpls-exp-outbound ef green map 6    
 mpls-exp-outbound ef yellow map 6   
 mpls-exp-outbound ef red map 6      
 mpls-exp-outbound cs6 green map 6   
 mpls-exp-outbound cs6 yellow map 6  
 mpls-exp-outbound cs6 red map 6     
 mpls-exp-outbound cs7 green map 7   
 mpls-exp-outbound cs7 yellow map 7  
 mpls-exp-outbound cs7 red map 7  
#
port split dimension interface 100GE0/2/24 split-type 1*50GE
port split dimension interface 100GE0/2/25 split-type 1*50GE
port split dimension interface 100GE0/2/26 split-type 1*50GE
port split dimension interface 100GE0/2/27 split-type 1*50GE
#
license
 active port-basic slot 2 port 16-23,24-27
#''',
                r'aaa.*?authentication-scheme default0': '''aaa
 user-password password-force-change disable
 local-user hwuser password irreversible-cipher Airtel@12
 local-user hwuser service-type ftp telnet ssh
 local-user hwuser level 3
 local-user hwuser state block fail-times 3 interval 5
 local-user netconf password irreversible-cipher Airtel@123
 local-user netconf service-type ftp telnet ssh
 local-user netconf level 3
 local-user netconf state block fail-times 3 interval 5
 local-user netconf user-group manage-ug
 local-user telco360 password irreversible-cipher Airtel@123
 local-user telco360 service-type ftp telnet ssh
 local-user telco360 level 3
 local-user telco360 state block fail-times 3 interval 5
 authentication-scheme default0''',
                r'is-name\s+\S+': f'is-name {name}',
                r'controller NA.*? undo shutdown\n\#\n': '',
                r'interface Serial0/2/0:1.*? dcn\n\#\n': '',
                r'trust upstream \S+': 'trust upstream NewQosPolicy',
                r'interface (25GE|50GE|100GE|GigabitEthernet)0/2/\d+.4094.*?ip address unnumbered interface LoopBack1023\n\#\n': '',
                r'snmp-agent.*tunnel-policy nms-tunnel-policy': f'''acl number 2700
 description ** FOR SNMPv3 COMMUNICATION**
 rule 10 permit source 10.57.122.68 0
 rule 20 permit source 10.57.122.196 0
#
snmp-agent
snmp-agent acl 2700
snmp-agent sys-info contact R&D Beijing, Huawei Technologies co., Ltd.
snmp-agent sys-info location {name}
snmp-agent sys-info version v3
snmp-agent mib-view included snmpview1 iso
snmp-agent group v3 KE_AIRTEL privacy read-view snmpview1 write-view snmpview1 notify-view snmpview1
snmp-agent target-host host-name IPRAN_NCE_PRIMARY trap address udp-domain 10.57.122.68 params securityname KE_AIRTEL v3 privacy private-netmanager
snmp-agent target-host host-name IPRAN_NCE_SECONDERY trap address udp-domain 10.57.122.196 params securityname KE_AIRTEL v3 privacy private-netmanager
snmp-agent usm-user v3 netconf
snmp-agent usm-user v3 netconf group KE_AIRTEL
snmp-agent trap source LoopBack0
snmp-agent protocol source-interface LoopBack0
snmp-agent trap enable
#
snetconf server enable
stelnet server enable
sftp server enable
sftp client-source -i LoopBack0
#
ssh user netconf
ssh user netconf authentication-type password
ssh user netconf service-type snetconf stelnet sftp
ssh user netconf sftp-directory cfcard:/
ssh user hwuser
ssh user hwuser authentication-type password
ssh user hwuser service-type stelnet
ssh user telco360
ssh user telco360 authentication-type password
ssh user telco360 service-type stelnet snetconf
ssh client first-time enable
ssh server-source all-interface
ssh ipv6 server-source all-interface
ssh authorization-type default aaa
#
tunnel-policy nms-tunnel-policy''',
                r'user-interface maximum-vty.*protocol inbound ssh': '''user-interface maximum-vty 21
user-interface con 0
user-interface vty 0 15
 authentication-mode aaa
 user privilege level 3
 protocol inbound all''',
                r'binding instance-type interface instance NA.\d+\n': ''
            }

            # 遍历替换规则
            updated_data = file_data
            print(updated_data)
            for pattern, replacement in replace_rules.items():
                updated_data = re.sub(pattern, replacement, updated_data, flags=re.DOTALL)
            # print(updated_data)
            output_folder = os.path.dirname(file_path)
            output_file = os.path.join(output_folder, f'{name}.cfg')
            # 保存更新后的数据
            with open(output_file, 'w') as updated_file:
                updated_file.write(updated_data)
            print(f"File {file_path} updated successfully.")

    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")

def get_all_files(script_path):
    files = []
    for folder_path, subfolders, filenames in os.walk(script_path):
        for filename in filenames:
            if filename.endswith((".cfg")):
                files.append(os.path.join(folder_path, filename))
    return files

if __name__ == '__main__':
    # 指定要处理的文件夹路径
    folder_path = 'C:\\Users\\y84292119\\Desktop\\KENYA\\code\\'
    files = get_all_files(folder_path)
    for file_path in files:
        process_cfg_file(file_path)