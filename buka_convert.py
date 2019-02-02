import Buka_Util
import os

dir_save=os.getcwd()#保存到工作目录下，之后新建目录
dir_input=input("请提供漫画目录")
file_list=os.listdir(dir_input)
if "chaporder.dat" in file_list:#先判断是否存在chaporder.dat，用来解析 漫画信息 和 章节-cid对照表
    json_reader=Buka_Util.BukaJSONReader(dir_input+r"\chaporder.dat")
    print("漫画名："+json_reader.name)
    dir_save+="\\"+json_reader.name
    if not os.path.exists(dir_save):
        os.makedirs(dir_save)#新建保存目录
    for file in file_list:
        file_path=dir_input+"\\"+file
        if file=="chaporder.dat":
            continue
        if os.path.isdir(file_path):
            cid=file
            bup_floder=Buka_Util.BupFloder(file_path)
            print("正在输出："+json_reader.chap_Dict[cid]["title"])
            bup_floder.convert_to_WebP(dir_save+"\\"+json_reader.chap_Dict[cid]["title"])
            del bup_floder
        else:
            bukafile=Buka_Util.BukaFile(file_path)
            bukafile.getInfo_buka()
            cid=bukafile.bukaInfo["cid"]
            print("正在输出："+json_reader.chap_Dict[cid]["title"])
            bukafile.convert_to_WebP(dir_save+"\\"+json_reader.chap_Dict[cid]["title"])
            del bukafile
else:
    print("没有找到chaporder.dat！")