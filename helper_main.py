# python3
import os
import sys
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
    print ("欢迎使用纯纯写作助手。\n====================\n0:打开设置\n1:进入云存储\n2:解压备份\n3:打开书架\n4:打包文件夹为备份\n5:快速上传云备份\n6:刷新屏幕")
    ctrl()
# 解压缩
def unzip():
    pwb_newest = findnewestfile("pwb")
    os.system("7z.exe x -odb pwb/"+pwb_newest+" -x!*.xml -x!MD5")

def ctrl():
    print("====================")
    num = int(input())
    if num == 0:
        try:
            os.startfile("config.ini")
        except:
            print("打开配置文件失败！")
        else:
            print("打开配置文件成功！")
    elif num == 1:
        helper_webdav.gui(0)   
    elif num == 2:
        unzip()
    elif num == 3:
        helper_book.gui()
    elif num == 4:
        helper_pak.gui()
    elif num == 5:
        helper_webdav.gui(1) 
    elif num == 6:
        gui_main()
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