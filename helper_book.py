import helper_main
import os
import sqlite3
import shutil

def between(lst, target):
    for i in range(len(lst)-1):
        if target >= lst[i] and target < lst[i+1]:
            return i

def gui():
    os.system("cls")
    # 连接数据库
    db_name = "db\\"+helper_main.findnewestfile("db")
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    # 读取书籍
    book = cur.execute("select name from Folder")
    print("书架上有以下书籍：")
    book_ser = 0
    for i in book:
        print(str(book_ser)+":"+str(i)[2:-3]) 
        book_ser += 1

    cur.close()
    print("====================\n0:返回\n1:分章导出\n2:合并导出")
    ctrl()

def ctrl():
    print("====================")
    book_num = int(input())
    if book_num == 0:       
        helper_main.gui_main()
    elif book_num == 1:
        make()
    elif book_num == 2:
        make_one()
    else:
        exit()

    ctrl()

def make():
    db_name = "db\\"+helper_main.findnewestfile("db")
    # 连接数据库
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    # 读取书籍
    book = cur.execute("select name from Folder")
    print("====================\n请输入分章导出的书籍编号：")
    book_id = int(input())
    tmp = 0
    for i in book:
        if tmp == book_id:
            book_name = str(i)[2:-3]
            break
        tmp += 1

    folder = cur.execute("select * from Folder")
    for i in folder:
        if i[1] == book_name:
            folder_id = i[0]
            break
    # 读取分卷
    categories = cur.execute("select * from Category order by rank")
    category_selected_name = []
    category_selected_rank = []
    for i in categories:
        if i[1] == folder_id:
            category_selected_name.append(i[2])
            category_selected_rank.append(i[5])

    # 创建文件夹
    if os.path.isdir("output/"+book_name):
        shutil.rmtree("output/"+book_name)
    os.makedirs("output/"+book_name)
    for i in category_selected_name:
        if not os.path.isdir("output/"+book_name+"/"+i):
            os.makedirs("output/"+book_name+"/"+i)

    # 写入文章内容
    articles = cur.execute("select * from Article where folderId=\'"+folder_id+"\' order by rank asc")
    for i in articles:
        if i[9] == 0:
            with open("output/"+book_name+"/"+i[1]+"."+i[3],"w",encoding="utf-8") as f:
                f.write(i[2])
        index = between(category_selected_rank, i[9])
        if index == None:
            folder = category_selected_name[len(category_selected_rank)-1]
        else:
            folder = category_selected_name[index]
        with open("output/"+book_name+"/"+folder+"/"+i[1]+"."+i[3],"w",encoding="utf-8") as f:
            f.write(i[2])

    cur.close()
    print("默认导出至output目录下。")

def make_one():
    db_name = "db\\"+helper_main.findnewestfile("db")
    # 连接数据库
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    # 读取书籍
    book = cur.execute("select name from Folder")
    print("====================\n请输入合并导出的书籍编号：")
    book_id = int(input())
    tmp = 0
    for i in book:
        if tmp == book_id:
            book_name = str(i)[2:-3]
            break
        tmp += 1

    folder = cur.execute("select * from Folder")
    for i in folder:
        if i[1] == book_name:
            folder_id = i[0]
            break
    # 读取分卷
    categories = cur.execute("select * from Category order by rank")
    category_selected_name = []
    category_selected_rank = []
    for i in categories:
        if i[1] == folder_id:
            category_selected_name.append(i[2])
            category_selected_rank.append(i[5])
    # 创建文件夹
    if not os.path.isdir("output"):
        os.makedirs("output")
    # 写入文章内容
    articles = cur.execute("select * from Article where folderId=\'"+folder_id+"\' order by rank asc")
    all_articles = ""
    for i in articles:
        all_articles += "\n====================\n"+i[1]+"\n====================\n"+i[2]+"\n"

    with open("output/"+book_name+".txt","w",encoding="utf-8") as f:
        f.write(all_articles)
        
    cur.close()
    print("默认导出至output目录下。")    

if __name__ == "__main__":
    gui()