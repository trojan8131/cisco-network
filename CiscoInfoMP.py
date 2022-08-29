from errno import ESTALE
from ipaddress import ip_address
from pydoc import describe
from traceback import print_tb
from ciscoconfparse import CiscoConfParse
import ipaddress
import re
import glob
import os
import sys

#Made by: Maciej Piotrowski 


file_path = 'config_output.txt'

###########DISPLAY OPTIONS ##############
show_conf=1
show_subnets=1
show_standby=1
#########################################


#Output to terminal or file, comment for change
sys.stdout = open(file_path, "w")


line_width=100
i=0
ip_sub=[]
configs=[]


for filename in glob.glob('Configs\*.cfg'):
   with open(os.path.join(os.getcwd(), filename), 'r') as f:
        if show_conf:
            print(re.match(r"Configs\\(.+)\.cfg",filename).group(1).center(line_width, '*'))
        parse = CiscoConfParse(filename, syntax='ios')
        desc=""
        for intf_obj in parse.find_objects_w_child('^interface','^\s+ip address'):
            intf_name = intf_obj.re_match_typed('^interface\s+(\S.+?)$')
            for children in intf_obj.children:
                ip=children.re_match_typed(r'ip\saddress\s(\d+.\d+.\d+.\d+)',group=1,default="",result_type=str)
                mask=children.re_match_typed(r'ip\saddress\s\d+.\d+.\d+.\d+(.+)',group=1,default="",result_type=str).strip("/").strip()
                x=children.re_match_typed(r'description\s(.+)',group=1,default="",result_type=str)
                if x != "":
                    desc=children.re_match_typed(r'description\s(.+)',group=1,default="",result_type=str)
                if ip != "":
                    network = ipaddress.IPv4Network(ip+"/"+mask, strict=False)
                    ip_sub.append(str(network.network_address).strip())
                    configs.append([re.match(r"Configs\\(.+)\.cfg",filename).group(1),intf_obj.text.strip("interface "),ip.strip(),str(network.network_address).strip(),mask.strip(),desc])
                    if show_conf:
                        print(intf_obj.text.strip("interface ")+";"+ip.strip()+";"+str(network.network_address).strip()+";"+mask.strip()+";"+desc)
                    desc=""
                    i=i+1



#List without duplicates 
ip_add_list=set(ip_sub)

if show_subnets:
    for i in ip_add_list:
        print(i.center(line_width, '*'))
        for x in configs:
            if(x[3]==i):
                print(*x, sep = ";")
                print(x[0].center(line_width, '*'))
                print(x[1])
                print(x[2]+"/"+x[4])
                print("*".center(line_width, '*'))




if show_standby:
    for filename in glob.glob('Configs\*.cfg'):
       with open(os.path.join(os.getcwd(), filename), 'r') as f:
            print(re.match(r"Configs\\(.+)\.cfg",filename).group(1).center(line_width, '*'))
            parse = CiscoConfParse(filename, syntax='ios')
            desc=""
            for intf_obj in parse.find_objects_w_child('^interface','^\s+ip address'):
                intf_name = intf_obj.re_match_typed('^interface\s+(\S.+?)$')
                for children in intf_obj.children:
                    standby=children.re_match_typed(r'standby.+',group=0,default="",result_type=str)
                    if standby != "":
                        print(intf_obj.text.strip("interface ")+";"+standby+";")
                        desc=""




    


            
