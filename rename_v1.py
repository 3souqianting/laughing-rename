import os
import os.path
# 声明，类似于c中的include<stdio.h>



def en_if(input):
    if u'\u0000' <= input <= u'\u007E':
        return 0
    else:
        return 1
# 子函数
# 判断是不是基本拉丁字母（包括52个大小字母和43个拉丁符号，其实就是英文符号、英文字母和数字）
# u'\u007E'很明显就是16进制的，大于这个值的包括汉字，阿拉伯文，日文、韩文等等你所能想到的
# 想了解更多百度unicode基本拉丁字母



read_file = r'D:\tools\rename\test'
# 需要重命名的目录，可以是相对路径，这里是绝对路径
# 例：read_file = r'D:\tools\rename\test'
# work_path = os.getcwd()  #因为用了绝对路径，不需要切来切去了   
# 先记下当前目录(py所在的目录)，一会好切换回来写'有问题的文件.md'与运行日志



en_not_backup = '\\有汉字备份'
conflict_backup = '\\冲突备份'
if not os.path.exists(os.getcwd() + en_not_backup):
    os.mkdir(os.getcwd() + en_not_backup)
if not os.path.exists(os.getcwd() + conflict_backup):
    os.mkdir(os.getcwd() + conflict_backup)
# 检测工作目录下（即rename.py的目录下）是否已存在了“有汉字备份”
# 和“冲突备份”这两个文件夹，没有则创建,方便管理

backup_file_name_dir = os.getcwd() + en_not_backup + '\\有汉字的文件名字备份-' + os.path.basename(read_file) + '.md'
trouble_dir = os.getcwd() + conflict_backup  + '\\有问题的文件-' + os.path.basename(read_file) + '.md'
# 接上一步，合成两个文件的绝对路径，并在名字里加入标志（来自需要命名的目录，具体看下面）
# 例：read_file = r'D:\tools\rename\test'   则会分别在对应的目录创建创建“有汉字的文件名字备份-test.md”和“有问题的文件-test.md”
# os.getcwd()为py的工作目录
# os.path.basename(read_file)为需要重名的父目录，上面例子的'\\test'



backup_file_name = open(backup_file_name_dir,'w')
trouble = open(trouble_dir,'w',encoding='utf-8')
count_zh_rename = 0
trouble_count = 0
# 初始化部分东西
# 1)与2)是打开一个文件，'w'是覆盖写，'a'是添加，如果在后面用的时候再'w'打开，会导致乱码
# 3)用于统计重命名的文件和目录个数
# 4)用于统计有问题的文件和目录个数



for root,dir,files in os.walk(read_file,topdown=False):
# topdown=False从子目录开始读起来，ture从父目录开始，默认ture
# 必须得是root,dir,files这样的格式，少一个都不行，root是列出路径，dir是列出目录，files是列出文件（不包括目录）

    read_file_dir = root
    files = os.listdir(read_file_dir)
    count_en_if = 0
    # 1)root是路径
    # 2)os.listdir列出目录下所有的文件
    # 3)用于统计一个文件名字中出现的非基本拉丁字母字符的个数，为0则不更改文件名字



    for file_name in files:
    # 逐个取出目录下的文件名字给file_name

        rename_result = ''
        # 每次读一个文件名字就初始化，防止吃上个文件名字的屎
        for i in range(len(file_name)):
        # 顺序逐位读物文件名字（不包含）

            if i+2 < len(file_name):
            # 先判断文件名字是不是读完了
            # i+2 <     的原因是'zhf'和'zhd'长度是3（假设这俩货在结尾的话）,还可以写成i+3 <=

                if file_name[i:i+3] == 'zhf' or file_name[i:i+3] == 'zhd':
                    trouble = open(trouble_dir,'a')
                    # 打开文件，'w'是覆盖写，'a'是添加，这里用'w'打开，会导致乱码
                    trouble_count += 1
                    print('将会有冲突：',file_name)
                    trouble.write(os.path.join(read_file_dir,file_name))
                    trouble.write('\n')
                    break
                # 判断有没有和标志（zhf zhd）一样的字符，有，并记录，继续下一个文件



            if en_if(file_name[i]) == 0 :
                rename_result = rename_result + file_name[i]
            else:
                encode_unicode = file_name[i].encode('unicode-escape')
                # 文件名字取出的那一位编码为unicode-escape
                encode_unicode_str = str(encode_unicode,'utf8')
                # 再格式化为str型
                count_en_if = count_en_if + 1
                # 统计非基本拉丁字母个数

                if i == 0 or en_if(file_name[i-1]) == 0 :
                    rename_result = rename_result + 'zhf'
                # 最重要，上一级的else就包含有file_name[i]为非基本拉丁字母的条件
                    # 首先，若为第一位就是非基本拉丁字母，因为rename_result已经初始化，rename_result = rename_result + 'zhf'    并不会报错，成功塞入zhf标志
                    # 其次，若不是第一位为非基本拉丁字母，则执行or后面的。i的上一位i-1若为基本拉丁字母，这就是一串非基本拉丁字母开始的地方。也成功塞入zhf标志
                
                if i+1 == len(file_name) or en_if(file_name[i+1]) == 0:
                    rename_result = rename_result + encode_unicode_str[2:6] + 'zhd'
                else:
                    rename_result = rename_result + encode_unicode_str[2:6]
                    
                    


        if i + 1 == len(file_name):
            if count_en_if == 0 :
                continue
            else:
                backup_file_name = open(backup_file_name_dir,'a',encoding='utf-8')
                backup_file_name.write(os.path.join(read_file_dir,file_name))      
                # 把路径和文件名字合起来
                backup_file_name.write('\n')
                # 份有非基本拉丁字母的文件名字（包括路径）



                rename_result = os.path.dirname(file_name) + rename_result
                print('文件名为：',file_name,'编码后为：',rename_result)
                os.rename(os.path.join(read_file_dir,file_name),os.path.join(read_file_dir,rename_result))
                # 采用把绝对路径和文件名字合并起来的方式重命名
                count_zh_rename += 1
                # 统计重命名了几个文件夹


#os.chdir(work_path)
# 回到一开始的工作目录，即rename_v1.py存放的位置
print('重命名了',count_zh_rename,'个文件','   有问题的文件个数：',trouble_count)