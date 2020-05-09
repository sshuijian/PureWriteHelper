import os
import configparser
import helper_main
import helper_book

def list_look(address,username,password):
    os.system("WinSCP.com /command \"open dav://"+username+":"+password+"@"+address+"PureWriter/Backups/\" \"ls\" \"exit\"")

def download(address,username,password,pwb_name):
    os.system("WinSCP.com /command \"open dav://"+username+":"+password+"@"+address+"\" \"get PureWriter/Backups/PureWriterBackup-*-*-"+pwb_name+".pwb pwb\\"+pwb_name+"\" \"exit\"")

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
def gui(num):
    if num == 1:
        values = read_ini()
        pwb_newest = helper_main.findnewestfile("pwb")
        upload(values[0],values[1],values[2],pwb_newest)
        helper_main.gui_main()
    os.system("cls")
    print("0:返回\n1:查看目录\n2:拉取备份\n3:上传备份\n4:解压备份并打开书架")
    ctrl()

def ctrl(): 
    print("====================")
    values = read_ini()
    web_num = int(input())
    if web_num == 0:
        helper_main.gui_main()
    elif web_num == 1:
        list_look(values[0],values[1],values[2])
    elif web_num == 2:
        print("请输入需要拉取的备份名：\n（例如：0502132757-v15.2.9）")
        pwb_name = input()
        download(values[0],values[1],values[2],pwb_name)
    elif web_num == 3:
        pwb_newest = helper_main.findnewestfile("pwb")
        upload(values[0],values[1],values[2],pwb_newest)
    elif web_num == 4:
        helper_main.unzip()
        helper_book.gui()
    else:
        exit()
    ctrl()

if __name__ == "__main__":
    gui(1)