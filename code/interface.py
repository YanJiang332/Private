
from jinja2 import Template
tem_path = './template/'


with open(tem_path + 'interface.template') as f:
    interface_config_template = Template(f.read())



interface_config_list = [{"interface_name": '2/1/2',
                          "interface_ip": '10.1.1.1',
                          "interface_mask": '255.255.255.0'
                          },
                          {"interface_name": '2/1/3',
                          "interface_ip": '10.1.1.5',
                          "interface_mask": '255.255.255.0'
                          }
                        ]

interface_config_result = interface_config_template.render(interface_list=interface_config_list)
print(interface_config_result)