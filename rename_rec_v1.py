import os
import os.path
# 声明，类似于c中的include<stdio.h>

def find(en_if):
    if file_name[i:i+3] == 'zhf' :
        return 1
    if file_name[i:i+3] == 'zhd' :
        return 2
# 子函数
# 判断非基本拉丁字母的开头与结尾，zhf是开头，zhd是结尾


read_file = r'D:\tools\rename\test'
# 需要重命名的目录，可以是相对路径，这里是绝对路径
# 例：read_file = r'D:\tools\rename\test'
work_path = os.getcwd()
# 先记下当前目录(py所在的目录)，一会好切换回来写'有问题的文件.md'与运行日志


rec_name_backup = '\\未恢复前备份'
if not os.path.exists(os.getcwd() + rec_name_backup):
    os.mkdir(os.getcwd() + rec_name_backup)
rec_name_backup_name_dir = os.getcwd() + rec_name_backup + '\\未恢复前备份-' + os.path.basename(read_file) + '.md'
rec_name_backup_name = open(rec_name_backup_name_dir,'w')

count_rename_en_not = 0
# 初始化部分东西
# 1)是打开一个文件，'w'是覆盖写，'a'是添加，如果在后面用的时候再'w'打开，会导致乱码
# 2)用于统计重命名的文件个数



for root,dir,files in os.walk(read_file,False):
# topdown=False从子目录开始读起来，ture从父目录开始，默认ture
# 必须得是root,dir,files这样的格式，少一个都不行，root是列出路径，dir是列出目录，files是列出文件（不包括目录）

    read_file_dir = root
    files = os.listdir(read_file_dir)       
    # 列出当前目录下所有的文件



    for file_name in files:    
    # 依次读文件

        i=0
        # while那里用来判断是不是读完了一个文件名字的每一位，从0开始倒末位，末位是文件名字长度减去一
        en_if_flag = 0
        # 初始化，后面遇到zhf会变成1，表示进入了汉字的起始标志
        rename_result = ''
        # 不初始化，后面不能自加，给了个空str型，也防止下个文件吃上个文件剩下的屎
        count_en_not = 0
        # 用于统计zhf的个数，为0则不重名文件

        while len(file_name) > i :
        # 逐位读取文件名字
        # 例：dsfzhf65b05efa6587zhd
        # 在没到zhf前都是一位一位读取，在有zhf和zhd的地方会i+3跳过

            if find(file_name[i]) == 1 :
                i += 3
                count_en_not = count_en_not + 1
                en_if_flag = 1
                # 判断是不是zhf，是则i+3跳过3位的zhf，并且计数，
                # 然后给一个标志( en_if_flag = 1)，开始四位四位地读并加上\u，65b0---\u65b0
                # 直到出现zhd，执行下面的

            elif find(file_name[i]) == 2:
                i += 3
                en_if_flag = 0
                if i == len(file_name):
                    break
                # 判断是不是zhd，是则i+3跳过3位的zhd，标志变回去( en_if_flag = 0)，并变回原来的一位一位地读取正常的基本拉丁字母
                # i+3等于文件名字长度时，说明zhd就是最后的了
                # 例：zhf65b0zhd i=6,i+3=9,全长为9，i=9超出范围，因为0-8就是九个了
                # 综上，直接break，跳出循环，读下一个文件名字



            if en_if_flag == 1 :
                rename_result = rename_result + str(b'\u','utf-8') + file_name[i:i+4]
                i = i + 4
            # 依据上面给的标志判断,是否要开始读已经编码了的非基本拉丁字母
            # 4位步进来读，因为\u65b0这六位就是对应一个汉字，又因为都是\u开头，为了节省空间就去掉了，这里格式化为字符加回去
            # 至于\u为啥要这样格式化加，因为我只会这么加

            elif en_if_flag == 0 :
                rename_result = rename_result + file_name[i]
                i += 1
            # 依据标志，一位一位地读基本拉丁字母，并加到rename_result



        rename_result_utf8 = bytes(rename_result,'utf-8')
        rename_result = rename_result_utf8.decode('unicode-escape')
        #转换为utf8,再转换成unicode-escape



        if i == len(file_name):
            if count_en_not == 0 :
                continue
            # 判断文件名是不是改过，也就是有没有zhf

            else:
                backup_file_name = open(rec_name_backup_name_dir,'a',encoding='utf-8')
                backup_file_name.write(os.path.join(read_file_dir,file_name))
                # 把路径和文件名字合起来
                backup_file_name.write('\n')

                rename_result = os.path.dirname(file_name) + rename_result
                os.rename(os.path.join(read_file_dir,file_name),os.path.join(read_file_dir,rename_result))
                # 采用把绝对路径和文件名字合并起来的方式重命名
                count_rename_en_not += 1
                rename_result = ''

os.chdir(work_path)
print('重命名了',count_rename_en_not,'个文件')