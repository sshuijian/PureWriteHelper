import os
import random
import sqlite3
import shutil
import time
import re
import configparser
import helper_main

def file_str(path):
    with open(path,"r",encoding='utf-8') as f:
        file_str = f.read()
    return file_str

# 分割文件名
def sep_str(str1):
    pre = re.findall("(.+?).txt",str1) or re.findall("(.+?).md",str1)
    pre = str(pre)[2:-2]
    suf = str1[len(pre)+1:]
    return pre,suf

# 将目录结构存入数表
def lst_dir(pak_path,new_book_name):
    file_lst = []
    sum_lst = []
    for root, dirs, files in os.walk(pak_path+"/"+new_book_name): 
        tmp_lst = []
        for i in dirs:
            tmp_lst.append(i)
            sum_lst.append(i)
            for root2, dirs2, files2 in os.walk(pak_path+"/"+new_book_name+"/"+i):
                for j in files2:
                    tmp_lst.append(j)
                    sum_lst.append(j)
            file_lst.append(tmp_lst)
            tmp_lst = []
        tmp_lst.append("0")
        sum_lst.append("0")
        for f in files:
            tmp_lst.append(f)
            sum_lst.append(f)
        file_lst.append(tmp_lst)
        break

    return file_lst,sum_lst

# 生成16位16进制id
def gen_16hex():
    r = lambda: random.randint(0,255)
    ran_16hex = "%02x%02x%02x%02x%02x%02x" % (r(),r(),r(),r(),r(),r())
    return ran_16hex

# 插入分卷名
def insert_category(cur,folderId,name,createdTime,rank):    
    cate_id = cur.execute("select id from Category")
    ran_id = gen_16hex()
    id_same = True
    while id_same:
        for i in cate_id:
            if ran_id == str(i)[2:-3]:
                ran_id = gen_16hex()
        id_same = False
    
    cur.execute("insert into Category (id,folderId,name,createdTime,collapsed,rank) values (\""+ran_id+"\",\""+folderId+"\",\""+name+"\","+createdTime+",0,"+rank+")")

# 插入文章
def insert_article(cur,title,content,extension,time,folderId,rank):    
    art_id = cur.execute("select id from Article")
    ran_id = gen_16hex()
    id_same = True
    while id_same:
        for i in art_id:
            if ran_id == str(i)[2:-3]:
                ran_id = gen_16hex()
        id_same = False

    cur.execute("insert into Article (id,title,content,extension,updateTime,createTime,folderId,editorId,rank) values (\""+ran_id+"\",\""+title+"\",\""+content+"\",\""+extension+"\","+time+","+time+",\""+folderId+"\",0,"+rank+")")

# 打包界面
def gui():
    # print("请输入打包文件夹所处目录：\n（例如：E:\Project\Python\PureWriteHelper\output）")
    # pak_path = input()
    pak_path = "output"
    # print("请输入打包文件夹名：\n（例如：我的书籍）")
    # new_book_name = input()
    # new_book_name = "测试"

    conf = configparser.ConfigParser()
    try:
        conf.readfp(open('config.ini',encoding="utf-8"))
    except:
        print("读取配置文件失败！")
        
    new_book_name = conf.get("quick","bookname")
    pwb_input = conf.get("quick","pwbname")

    if (pwb_input == "") or (new_book_name == ""):
        print("请输入打包文件夹名：\n（例如：我的书籍）")
        new_book_name = input()
        print("请输入打包后的备份文件名：\n（例如：0502132757-v15.2.9）")
        pwb_input = input()
    pak_db(pak_path,new_book_name)
    pak_pwb(new_book_name,pwb_input)

# 将数据写入db文件
def pak_db(pak_path,new_book_name):
    now_time = int(time.time()*1000)
    # 遍历文件夹
    file_lst,sum_lst = lst_dir(pak_path,new_book_name)
    # 连接数据库
    # helper_main.unzip()
    db_newest = helper_main.findnewestfile("db")
    try:
        f =open("db/"+new_book_name+".db",'r')
        f.close()
    except IOError:
        os.rename("db/"+db_newest,"db/"+new_book_name+".db")
    db_name = "db/"+new_book_name+".db"
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    # 得到Folder下最大rank值
    book_rank = cur.execute("select rank from Folder order by rank")
    for i in book_rank:
        new_book_rank = str(i[0]+1)
    # 生成16位16进制id
    book_id = cur.execute("select id from Folder")
    ran_folderId = gen_16hex()
    id_same = True
    while id_same:
        for i in book_id:
            if ran_folderId == str(i)[2:-3]:
                ran_folderId = gen_16hex()
        id_same = False
    # 插入书名
    cur.execute("insert into Folder (id,name,createdTime,rank,deleted,deletedTime) values (\""+ran_folderId+"\",\""+new_book_name+"\","+str(now_time)+","+new_book_rank+",0,0)")
    
    rank_num = 0
    sum_num = 0
    cafe_rank = [2] 
    for i in file_lst[:-1]:
        sum_num += len(i)
        cafe_rank.append(2*len(i))
    # 获取分卷rank放入数组
    a = 0 
    b = 0
    for j in cafe_rank:
        if b < len(cafe_rank)-1:
            b += 1
        cafe_rank[b] += cafe_rank[b-1]
    cafe_rank = cafe_rank[:-1]
    # 插入数据
    while(rank_num < 2*(sum_num)+1):
        rank = 0
        if rank_num != 0:
            rank = sum_lst[int(rank_num/2)-1]
        # 插入无分卷的文章
        if rank_num == 0:
            for i in file_lst[len(file_lst)-1]:
                if i != file_lst[len(file_lst)-1][0]:
                    pre,suf = sep_str(i)
                    article_str = file_str(pak_path+"/"+new_book_name+"/"+i)
                    insert_article(cur,pre,article_str,suf,str(now_time),ran_folderId,str(rank_num))
        # 插入分卷
        elif rank_num in cafe_rank:
            insert_category(cur,ran_folderId,rank,str(now_time),str(rank_num))
        # 插入分卷下文章
        else:
            pre,suf = sep_str(rank)
            n = 0 
            for i in reversed(cafe_rank):
                n += 1
                if rank_num > i:
                    for j in file_lst[len(cafe_rank)-n][1:]:
                        article_str = file_str(pak_path+"/"+new_book_name+"/"+file_lst[len(cafe_rank)-n][0]+"/"+j)
                        insert_article(cur,pre,article_str,suf,str(now_time),ran_folderId,str(rank_num))
        rank_num += 2

    conn.commit()
    conn.close()

# 将db文件打包为pwb
def pak_pwb(book_name,pwb_input):
    # 连接数据库
    db_name = "db/"+book_name+".db"
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    # 获取书籍、文章数目
    num_book = ""
    num_article = ""
    book = cur.execute("select count(*) from Folder")
    for i in book:
        num_book = str(i)[1:-2]
    article = cur.execute("select count(*) from Article")
    for i in article:
        num_article = str(i)[1:-2]
    conn.close()
    # 打包为pwb
    if os.path.isdir("tmp"):
        shutil.rmtree("tmp")
    os.makedirs("tmp")
    pwb_name = "PureWriterBackup-"+num_book+"本书-"+num_article+"篇文章-"+pwb_input
    pwb_newest = helper_main.findnewestfile("pwb")
    os.system("7z.exe x pwb/"+pwb_newest+" -y -aos -otmp -x!*.db")
    # os.rename(db_name,"tmp/"+pwb_name+".db")
    os.system("copy .\\db\\"+book_name+".db .\\tmp\\"+pwb_name+".db")
    os.system("7z.exe a -tzip tmp.pwb .\\tmp/*")
    os.rename("tmp.pwb","pwb/"+pwb_name+".pwb")
    os.system("rd/s/q tmp")

if __name__ == "__main__":
    gui()