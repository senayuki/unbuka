import os
import json

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
        self.bukaInfo["bid"]=str(self.__read_number())#漫画编号
        self.bukaInfo["cid"]=str(self.__read_number())#章节编号
        self.bukaInfo["name"]=self.__read_string()#漫画名
        #读取文件分割表
        self.bukaInfo["list_length"]=self.__read_number()
        self.bukaInfo["list"]=self.__read_list()
        return

    def export_buka_to_Dict(self):
        """
        分割文件,返回字典，{文件名:WebP}
        """
        #如果info是空的，那么先获取信息
        if self.bukaInfo=={}:
            self.getInfo_buka()
        #遍历list，解出文件
        self.file_Dict={}
        for file in self.bukaInfo["list"]:
            self.f.read(64)#读掉谜之数据头
            self.file_Dict[file["file_name"]]=self.f.read(file["size"]-64)
        return

    def export_buka_to_File(self,dir=os.getcwd()):
        """
        将解压的所有文件存储到目录下，默认为工作目录
        """
        self.export_buka_to_Dict()
        if not os.path.exists(dir):
            os.makedirs(dir)
        for file_name in self.file_Dict.keys():
            with open(dir+"\\"+file_name,"wb") as f:
                f.write(self.file_Dict[file_name])

    def convert_to_WebP(self,dir=os.getcwd()):
        """
        将WebP文件存储到目录下，默认为工作目录
        """
        self.export_buka_to_Dict()
        if not os.path.exists(dir):
            os.makedirs(dir)
        for file_name in self.file_Dict.keys():
            if file_name=="index2.dat":
                continue
            name=file_name.split(".")[0].split("_")[1]
            with open(dir+"\\"+name+".webp","wb") as f:
                f.write(self.file_Dict[file_name])

    def __init__(self,file):
        self.bukaInfo={}#存放章节相关信息
        self.file_Dict={}#存放文件字典
        if os.path.isdir(file):#检查是否是文件
            raise FormatError("It's a floder,you should use BupFloder")
        self.type=file.split(".")[1]#获得输入文件扩展名
        self.dir=os.path.split(file)[0]#获得目录
        self.file=file#存储完整的文件路径

class BupFloder:
    def export_buka_to_Dict(self):
        """
        分割文件,返回字典，{文件名:WebP}
        """
        self.file_Dict={}
        for file in self.files:#得到字典
            with open(self.dir+"\\"+file,"rb") as f:
                f.read(64)#读掉谜之数据头
                self.file_Dict[file]=f.read()
        return

    def export_buka_to_File(self,dir=os.getcwd()):
        """
        将解压的文件存储到目录下，默认为工作目录
        """
        self.export_buka_to_Dict()
        if not os.path.exists(dir):
            os.mkdir(dir)
        for file_name in self.file_Dict.keys():
            with open(dir+"\\"+file_name,"wb") as f:
                f.write(self.file_Dict[file_name])

    def convert_to_WebP(self,dir=os.getcwd()):
        """
        将WebP文件存储到目录下，默认为工作目录
        """
        self.export_buka_to_Dict()
        if not os.path.exists(dir):
            os.makedirs(dir)
        for file_name in self.file_Dict.keys():
            if file_name=="index2.dat":
                continue
            name=file_name.split(".")[0].split("_")[1]
            with open(dir+"\\"+name+".webp","wb") as f:
                f.write(self.file_Dict[file_name])
                
    def __init__(self,dir):
        self.dir=dir
        if os.path.isfile(dir):#检查是否是目录
            raise FormatError("It's a file,you should use BukaFile")
        self.dir_name=dir.split("\\")[-1]
        self.files=os.listdir(dir)
        self.file_Dict={}
        
class BukaJSONReader:
    """
        解析chaporder.dat，得到漫画信息字典info_Dict和章节字典chap_dict{cid: {title, idx, type}}，所有数据类型均为str，不是num
    """
    def __init__(self,JSON):
        with open(JSON,"r",encoding="utf-8") as f:
            self.json_dict=json.loads(f.read())

        self.chap_Dict={}
        for chap in self.json_dict["links"]:
            chap_cid=chap["cid"]
            chap_type=chap["type"]
            chap_title=chap["title"]
            chap_idx=chap["idx"]
            if (chap_type=="0" and chap_title==""):#如果是正篇且title=""，则title=idx
                chap_title=chap_idx
            if (chap_type=="2" and chap_title==""):#如果是番外且title=""，则title="番外"+idx
                chap_title="番外"+chap_idx
            dict={"title":chap_title,"idx":chap_idx,"type":chap_type}
            self.chap_Dict[chap_cid]=dict

        self.name=self.json_dict["name"]
        self.comicid=self.json_dict["detail_shareurl"].split("/")[4]
        self.logo=self.json_dict["logo"]
        self.author=self.json_dict["author"]
        self.intro=self.json_dict["intro"]
        self.lastup=self.json_dict["lastup"]
        self.lastuptimeex=self.json_dict["lastuptimeex"]
        self.populars=self.json_dict["populars"]
        self.detail_shareurl=self.json_dict["detail_shareurl"]
        del self.json_dict


