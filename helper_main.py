# python3
import os
import helper_webdav
import helper_book
import helper_pak
   
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
    print ("欢迎使用纯纯写作助手。\n====================\n0:进入云存储\n1:解压备份\n2:打开书架\n3:打包文件夹为备份")
    ctrl()
# 解压缩
def unzip():
    pwb_newest = findnewestfile("pwb")
    os.system("7z.exe x -odb pwb/"+pwb_newest+" -x!*.xml -x!MD5")

def ctrl():
    print("====================")
    num = int(input())
    if num == 0:
        helper_webdav.gui()   
    elif num == 1:
        unzip()
    elif num == 2:
        helper_book.gui()
    elif num == 3:
        helper_pak.gui()
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