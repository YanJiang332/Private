# import subprocess
# import paramiko
# import time

# # 全局字典用于存储上一次执行ACL操作的时间戳
# last_acl_operation_time = {}

# def ping_device(ip):
#     try:
#         subprocess.check_output(["ping", "-c", "1", ip], timeout=3)
#         return True
#     except subprocess.CalledProcessError:
#         return False
#     except subprocess.TimeoutExpired:
#         return False

# # def add_firewall_rule(ip):
# #     ssh = paramiko.SSHClient()
# #     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
# #     # 替换为你的SSH登录信息
# #     ssh.connect('your_firewall_host', username='your_username', password='your_password')

# #     # 替换为你的防火墙命令，用于添加ACL规则
# #     command = f'add_acl_command {ip}'
    
# #     # 执行SSH命令
# #     ssh.exec_command(command)
    
# #     # 更新上一次执行ACL操作的时间戳
# #     last_acl_operation_time[ip] = time.time()
    
# #     ssh.close()

# # def remove_firewall_rule(ip):
# #     ssh = paramiko.SSHClient()
# #     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
# #     # 替换为你的SSH登录信息
# #     ssh.connect('your_firewall_host', username='your_username', password='your_password')

# #     # 替换为你的防火墙命令，用于删除ACL规则
# #     command = f'remove_acl_command {ip}'
    
# #     # 执行SSH命令
# #     ssh.exec_command(command)
    
# #     # 更新上一次执行ACL操作的时间戳
# #     last_acl_operation_time[ip] = time.time()
    
# #     ssh.close()

# def monitor_devices(device_ips):
#     while True:
#         for ip in device_ips:
#             if not ping_device(ip):
#                 # 如果ping不通且距离上一次执行ACL操作已经过了三分钟，则添加规则
#                 if ip not in last_acl_operation_time or time.time() - last_acl_operation_time[ip] >= 5:
#                     print(ip)
#                     last_acl_operation_time[ip] = time.time()
#                     # add_firewall_rule(ip)
#             # else:
#             #     # 如果ping通且距离上一次执行ACL操作已经过了三分钟，则删除规则
#             #     if ip in last_acl_operation_time and time.time() - last_acl_operation_time[ip] >= 20:
#             #         print(ip)
#             #         # remove_firewall_rule(ip)

#         time.sleep(60)

# if __name__ == "__main__":
#     # 替换为你的设备IP地址列表
#     devices = ["100.64.220.1", "10.48.28.1", "127.0.0.1", "127.0.0.0"]
    
#     monitor_devices(devices)


import subprocess
import time
import random
from concurrent.futures import ThreadPoolExecutor


# 全局字典用于存储上一次执行ACL操作的时间戳
last_acl_operation_time = {}
# 全局字典用于存储设备状态，True表示设备ping通，False表示设备不通
device_status = {}
# 全局字典用于存储设备不通的开始时间
device_down_time = {}
# 全局字典用于存储是否已经添加ACL规则，True表示已添加，False表示未添加
acl_added = {}
# 设定 ACL 规则添加的最小时间间隔，单位为秒
acl_cooldown_time = 60
# 全局集合用于存储已使用的ACL规则编号
used_acl_numbers = set()
# 全局字典用于存储每个设备当前使用的ACL规则编号
current_acl_number = {}


def ping_device(ip):
    try:
        subprocess.run(["ping", "-n", "1", ip], timeout=3, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return True
    except subprocess.CalledProcessError:
        return False
    except subprocess.TimeoutExpired:
        return False

def add_acl_rule(ip):
    global current_acl_number, used_acl_numbers
    # 获取当前设备的ACL规则编号，确保规则编号唯一
    acl_number = current_acl_number.get(ip, random.randint(1, 1000))
    while acl_number in used_acl_numbers:
        acl_number = random.randint(1, 1000)

    # 添加ACL规则的操作
    acl_rule = f"rule {acl_number} deny ip source {ip} 0.0.15.255"
    print(f"Adding ACL rule for device {ip}: {acl_rule}")
    # ...

    # 更新设备当前使用的ACL规则编号和已使用的规则集合
    current_acl_number[ip] = acl_number
    used_acl_numbers.add(acl_number)


def remove_acl_rule(ip):
    global current_acl_number, used_acl_numbers
    # 获取当前设备的ACL规则编号
    acl_number = current_acl_number.get(ip)  # 默认从20开始
    # 删除ACL规则的操作
    acl_rule = f"rule {acl_number} deny ip source {ip} 0.0.15.255"
    print(f"Removing ACL rule for device {ip}: {acl_rule}")
    # ...
    used_acl_numbers.remove(acl_number)
    current_acl_number.pop(ip)

def process_device(ip):
    current_status = ping_device(ip)
    
    # 如果设备状态发生变化
    if ip in device_status and device_status[ip] != current_status:
        if current_status:
            # 设备从不通变为通，删除防火墙规则
            print(f"Device {ip} is now online.")
            if ip in acl_added and acl_added[ip]:
                # 设备之前不通，已添加ACL规则，现在已经通了，删除ACL规则
                remove_acl_rule(ip)
                acl_added[ip] = False
        else:
            # 设备从通变为不通，更新设备不通的开始时间
            device_down_time[ip] = time.time()
            # 如果ACL规则未添加，则添加ACL规则
            if ip not in acl_added or not acl_added[ip]:
                add_acl_rule(ip)
                acl_added[ip] = True
            
    # # 更新设备状态
    # device_status[ip] = current_status
    
    # 如果设备连续不通超过三分钟，则添加规则
    if not current_status:
        current_time = time.time()
        if ip not in last_acl_operation_time or current_time - last_acl_operation_time[ip] >= acl_cooldown_time:
            print(f"Device {ip} is now offline.")
            # 更新时间戳
            last_acl_operation_time[ip] = current_time
            # 如果ACL规则未添加，则添加ACL规则
            if ip not in acl_added or not acl_added[ip]:
                add_acl_rule(ip)
                acl_added[ip] = True

    device_status[ip] = current_status   



def monitor_devices(device_ips):
    global device_status, device_down_time, last_acl_operation_time, acl_added, current_acl_number # 声明全局变量
    
    with ThreadPoolExecutor(max_workers=50) as executor:  # 根据系统性能调整工作进程的数量
        while True:
            futures = [executor.submit(process_device, ip) for ip in device_ips]
            for future in futures:
                future.result()

            print(device_status)
            print(device_down_time)
            print(last_acl_operation_time)
            print(acl_added)
            print(used_acl_numbers)
            print(current_acl_number)
                    
            time.sleep(5)

if __name__ == "__main__":
    # 替换为你的设备IP地址列表
    devices = ["100.64.220.1", "10.48.28.1", "127.0.0.1", "127.0.0.0"]
    
    monitor_devices(devices)