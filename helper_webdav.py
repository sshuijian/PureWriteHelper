import os
import configparser
import helper_main

def list_look(address,username,password):
    os.system("WinSCP.com /command \"open dav://"+username+":"+password+"@"+address+"PureWriter/Backups/\" \"ls\" \"exit\"")

def download(address,username,password,pwb_name):
    os.system("WinSCP.com /command \"open dav://"+username+":"+password+"@"+address+"\" \"get PureWriter/Backups/PureWriterBackup-*-*-"+pwb_name+" pwb\\"+pwb_name+"\" \"exit\"")

def upload(address,username,password,pwb_newest):
    os.system("WinSCP.com /command \"open dav://"+username+":"+password+"@"+address+"PureWriter/Backups/\" \"put pwb\\"+pwb_newest+"\" \"exit\"")
 
# 读取配置
def read_ini():  
    conf = configparser.ConfigParser()
    try:
        conf.readfp(open('config.ini',encoding="utf-8"))
    except:
        print("读取配置文件失败！")
    address = conf.get("webdav","address")
    username = conf.get("webdav","username")
    password = conf.get("webdav","password")
    return address,username,password

# webdav 界面
def gui():
    os.system("cls")
    print("0:返回\n1:打开配置\n2:查看目录\n3:拉取备份\n4:上传备份")
    ctrl()

def ctrl(): 
    print("====================")
    values = read_ini()
    web_num = int(input())
    if web_num == 0:
        helper_main.gui_main()
    elif web_num == 1:
        try:
            os.startfile("config.ini")
        except:
            print("打开配置文件失败！")
        else:
            print("打开配置文件成功！")
    elif web_num == 2:
        list_look(values[0],values[1],values[2])
    elif web_num == 3:
        print("请输入需要拉取的备份名：\n（形如0502132757-v15.2.9.pwb即可）")
        pwb_name = input()
        download(values[0],values[1],values[2],pwb_name)
    elif web_num == 4:
        pwb_newest = helper_main.findnewestfile("pwb")
        upload(values[0],values[1],values[2],pwb_newest)
    else:
        exit()
    ctrl()
