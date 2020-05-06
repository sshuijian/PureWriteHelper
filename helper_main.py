# python3
import os
import sqlite3
import shutil
import helper_webdav
   
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
# 主界面
def gui_main():
    os.system("cls")
    print ("欢迎使用纯纯写作助手。\n====================\n0:进入云存储\n1:解压备份\n2:打开书架")
    ctrl()
# 解压缩
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

def ctrl():
    print("====================")
    num = int(input())
    if num == 0:
        helper_webdav.gui()   
    elif num == 1:
        unzip()
    elif num == 2:
        book()
    else:
        exit()
    ctrl()

if __name__ == "__main__":
    # 创建文件夹
    if not os.path.isdir("db"):
        os.mkdir("db")
    if not os.path.isdir("pwb"):
        os.mkdir("pwb")
    # 主界面
    gui_main()