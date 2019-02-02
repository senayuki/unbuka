# 布卡漫画离线文件转换  

感谢[贴吧hucsmn大佬](https://tieba.baidu.com/p/3264037584)提供的.buka文件格式说明  
用Python写了几个类，实现了.buka文件、章节文件夹、chaporder.dat解析  
  
# 类与方法的相关说明
__为使用统一，所有信息，包括编号，统一是str类型，不是num__  
  
__buka_convert.py__ 当作一个示例，实现了将一个漫画文件夹转换  

__BukaFile__ 类用于解析和拆解.buka文件  
__BupFloder__ 类用于解析章节文件夹中的文件  
以上两个类都直接将文件或路径作为参数构造即可  
以上类都有以下方法  
export_buka_to_Dict：解压文件到字典file_Dict{文件名:数据}  
export_buka_to_File：解压文件到指定目录  
convert_to_WebP：拆解出WebP文件  

__BukaFile__ 类有getInfo_buka方法，用于解析.buka文件的基本信息到字典bukaInfo  

__BukaJSONReader__ 类用于解析chaporder.dat文件  
漫画相关信息存入各成员变量  
chap_Dict为章节对照表，cid为键，章节信息的字典为值 {cid:{title,idx,type}}  
由于布卡临时工的疏忽（大概），有些title为空，利用type和idx进行了补全  
  
# .buka文件格式说明  
字符串以UTF-8编码，以\0结尾；数字是unsigned的4字节整数，小端存储  
缓存到的文件夹中，所有文件均没有去除64字节的头  
  
* 魔数 4字节字符串：buka  
* 未知作用的数字1 4字节整数  
* 未知作用的数字1 4字节整数  
* 漫画编号 4字节整数  
* 章节编号 4字节整数  
* 漫画名称 字符串  
* 文件信息表  
  * 文件信息表大小（含自身4字节） 4字节整数  
  * 文件信息（根据文件信息表多次读取）  
    * 偏移量  
    * 文件大小  
    * 文件名  
* 文件数据（根据信息表多次读取）  
  * 数据头 __64字节__  
  * 元数据（图片为WebP，dat的作用没搞懂）  