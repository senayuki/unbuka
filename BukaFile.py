#coding=utf-8
import os

class FormatError(Exception):
    '格式错误异常'
    pass

class BukaFile:
    '处理.buka文件'
    def __read_string(self):#读取f里的内容，遇到\0结束，utf-8编码
        stringb=b""
        self.readed_string=0#本次读取的长度，以成员变量存储
        while(1):
            tmp=self.f.read(1)
            self.readed_string+=1
            stringb+=tmp
            if(tmp==b"\0"):
                break
        string=str(stringb,encoding="utf-8")
        return string[0:-1]#去除\0

    def __read_number(self):#读取固定长度的数字，4四字节无符号小端模式
        num = int.from_bytes(self.f.read(4),byteorder="little",signed=False)
        return num

    def __read_list(self):
        len=self.bukaInfo["list_length"]#方便使用变量
        len-=4#减去存储表长自身的4字节
        list=[]#用列表存储字典
        while(len!=0):#直到长度变为0
            dict={}
            dict["offset"]=self.__read_number()
            len-=4
            dict["size"]=self.__read_number()
            len-=4
            dict["file_name"]=self.__read_string()
            len-=self.readed_string
            list.append(dict)
            del dict
        return list

    def getInfo_buka(self):
        """
        读取buka文件中的信息到bukaInfo
        """
        #读取基本信息
        self.f = open(self.file,"rb")#以rb读文件
        self.bukaInfo["magic"]=self.f.read(4).decode("UTF-8")#校验魔数
        if self.bukaInfo["magic"]!="buka":#如果魔数校验错误
            raise FormatError("Not a .buka file")
        self.bukaInfo["unknown1"]=self.__read_number()#未知数字1
        self.bukaInfo["unknown2"]=self.__read_number()#未知数字2
        self.bukaInfo["bid"]=self.__read_number()#漫画编号
        self.bukaInfo["cid"]=self.__read_number()#章节编号
        self.bukaInfo["name"]=self.__read_string()#漫画名
        #读取文件分割表
        self.bukaInfo["list_length"]=self.__read_number()
        self.bukaInfo["list"]=self.__read_list()
        return

    def exportFile_buka_to_Dict(self):
        """
        分割文件,返回字典，{文件名:WebP}
        """
        #如果info是空的，那么先获取信息
        if self.bukaInfo=={}:
            self.getInfo_buka()
        #遍历list，解出文件
        self.file_Dict={}
        for file in self.bukaInfo["list"]:
            print(file["file_name"])
            self.f.read(64)#读掉谜之数据头
            self.file_Dict[file["file_name"]]=self.f.read(file["size"]-64)
        return

    def exportFile_buka_to_File(self,dir=os.getcwd()):
        """
        将文件存储到工作目录\\cid下
        """
        self.exportFile_buka_to_Dict()
        dir+="\\"+str(self.bukaInfo["cid"])
        if not os.path.exists(dir):
            os.mkdir(dir)
        for file_name in self.file_Dict.keys():
            with open(dir+"\\"+file_name,"wb") as f:
                f.write(self.file_Dict[file_name])

    def __init__(self,file):
        self.bukaInfo={}#存放章节相关信息
        self.file_Dict={}#存放文件字典
        if os.path.isdir(file):#检查是否是文件
            raise FormatError("It's a floder,you should use BupFloder")
        self.type=file.split(".")[1]#获得输入文件扩展名
        self.dir=os.path.split(file)[0]#获得目录
        self.file=file#存储完整的文件路径
