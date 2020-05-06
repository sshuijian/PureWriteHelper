# python3
import os
import configparser
import sqlite3
import shutil

# 找到最新文件
def findnewestfile(file_path):
    filenames = os.listdir(file_path)
    name_ = []
    time_ = []
    for filename in filenames:
        c_time = os.path.getctime(file_path+'\\'+filename)
        name_.append(filename)
        time_.append(c_time)
    newest_file = name_[time_.index(max(time_))]
    return newest_file


def init():
    # 创建文件夹
    if not os.path.isdir("db"):
        os.mkdir("db")
    if not os.path.isdir("pwb"):
        os.mkdir("pwb")
    # GUI
    print (
"欢迎使用纯纯写作助手。\n\
====================\n\
0:打开配置\n\
1:拉取备份\n\
2:解压pwb\n\
3:打开书架")

def setting():
    os.startfile("config.ini")
def download():
    # 读取配置
    conf = configparser.ConfigParser()
    conf.readfp(open('config.ini',encoding="utf-8"))
    address = conf.get("webdav","address")
    username = conf.get("webdav","username")
    password = conf.get("webdav","password")
    # 拉取备份
    print("请输入需要拉取的备份名：\n（形如PureWriterBackup-*-*-0502132757-v15.2.9.pwb）")
    pwb_name = input()
    os.system("WinSCP.com /command \"open dav://"+username+":"+password+"@"+address+"\" \"get PureWriter/Backups/"+pwb_name+" pwb\\"+pwb_name+"\" \"exit\"")

def unzip():
    pwb_newest = findnewestfile("pwb")
    os.system("7z.exe x -odb pwb/"+pwb_newest+" -x!*.xml -x!MD5")

def book():
    os.system("cls")
    db_name = "db\\"+findnewestfile("db")
    #连接数据库
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    #获取书籍ID
    book = cur.execute("select name from Folder")
    print("书架上有以下书籍：")
    for i in book:
        print(str(i)[2:-3]) 
    print("====================\n请输入需要导出的书名：")
    book_name = input()
    book2 = cur.execute("select * from Folder")
    for j in book2:
        if j[1] == book_name:
            folder_id = j[0]
            break
    #创建文件夹
    if os.path.isdir("output/"+book_name):
        shutil.rmtree("output/"+book_name)
    os.makedirs("output/"+book_name)
    #获取文章内容
    articles = cur.execute("select * from Article where folderId=\'"+folder_id+"\'")
    for n in articles:
        with open("output/"+book_name + "/" + n[1] + ".txt", "w", encoding="utf-8") as f:
            f.write(n[2])
    cur.close()
    print("全书默认导出至output目录下。")

# def zip():

def ctrl():
    print("====================")
    num = int (input())
    if num == 0:
        setting()
    elif num == 1:
        download()
    elif num == 2:
        unzip()
    elif num == 3:
        book()
    else:
        exit()
    ctrl()

if __name__ == "__main__":
    init()
    ctrl()