import os

class FormatError(Exception):
    """
    格式错误异常
    """
    pass

class BupFloder:
    def exportFile_buka_to_Dict(self):
        """
        分割文件,返回字典，{文件名:WebP}
        """
        self.file_Dict={}
        for file in self.files:#得到字典
            with open(self.dir+"\\"+file,"rb") as f:
                f.read(64)#读掉谜之数据头
                self.file_Dict[file]=f.read()
        return

    def exportFile_buka_to_File(self,dir=os.getcwd()):
        """
        将文件存储到工作目录\\cid下
        """
        self.exportFile_buka_to_Dict()
        dir+="\\"+str(self.dir_name)
        if not os.path.exists(dir):
            os.mkdir(dir)
        for file_name in self.file_Dict.keys():
            with open(dir+"\\"+file_name,"wb") as f:
                f.write(self.file_Dict[file_name])

    def __init__(self,dir):
        self.dir=dir
        if os.path.isfile(dir):#检查是否是目录
            raise FormatError("It's a file,you should use BukaFile")
        self.dir_name=dir.split("\\")[-1]
        self.files=os.listdir(dir)
        self.file_Dict={}
