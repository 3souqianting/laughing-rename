# **批量重命名与恢复**</br>
###### 拿来练手的</br>
#### 说明
 对文件名字中的非基本拉丁字母（包括符号，就是除了unicode编码的\u0000-\u007E这些之外）进行重命名，非基本拉丁字母部分前后会有标志（前zhf，后zhd），而且为了节省长度把重复出现的\u去掉了，有标志在，恢复的时候按间隔加回去就行。重命名的时候包括文件拓展名（就是后缀，如果有的话），不会用os.path.splitext来分离文件拓展名，试过，识别错了，有的文件名中会含有“.”，他就认为那里就是文件拓展名</br>
 ###### 举个栗子：dsfs嘎d1地方放大fg.txt </br>
######  &#8194;&#8194;&#8194;&#8194;&#8194;&#8194;&#8194;&#8194;&#8194;&#8194;dsfszhf560ezhdd1zhf573065b9653e5927zhdfg.txt
### 为什么会做这个？
在ubuntu使用davfs2挂载网盘的时候发现，含有中文名字的都没有被挂载，升级了最新版也不行，其他的非英语的估计大概率也会</br>
索性靠着百度自己开始在win下写了个py，因为在win下有官方程序能挂载在本地（202204）</br>
详细<a href="https://github.com/3souqianting/laughing-rename/blob/main/doc/%E6%B5%81%E7%A8%8B%E5%9B%BE.svg" target="_blank">流程图</a>在doc内，网页点raw看原图就清晰了</br>
