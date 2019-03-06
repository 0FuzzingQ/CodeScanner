from __future__ import absolute_import

from celery import task
from celery import shared_task
from .models import Task,Result
import subprocess
import rarfile
import zipfile
from xml.dom.minidom import parse

#gitlab token 

#调用fortify扫描任务
@shared_task
def add(filepath,taskid):
    
    #按照后缀解压缩代码文件

    #rar
    if filepath.split('.')[-1] == 'rar':
    	rf = rarfile.RarFile(filepath)
    	newpath = filepath[0:-4]
    	rf.extractall(newpath)

    #zip
    if filepath.split('.')[-1] == 'zip':
        af = zipfile.ZipFile(filepath)
        newpath = filepath[0:-4]
        af.extractall(newpath)

    #tar.gz
    if filepath.split('.')[-1] == 'gz' and filepath.split('.')[-2] == 'tar':
        downcmd = "wget -O upload\\ " + taskid + ".zip" + " " + filepath
        down = subprocess.check_call(downcmd,shell=True)
        af = zipfile.ZipFile(taskid + ".zip")
        newpath = taskid
        af.extractall(newpath)
        

    #fortify 命令行接口拼接
    cmd = "D:\\HPE_Sec\\Fortify_SCA_and_Apps_16.20\\bin\\sourceanalyzer.exe " + newpath + " -scan -f " + taskid + ".fpr"
    cmd2 = "D:\\HPE_Sec\\Fortify_SCA_and_Apps_16.20\\bin\\ReportGenerator.bat -format xml -f " +  taskid + ".xml -source " + taskid + ".fpr" 
    
    
    #子进程调用
    print("[*]start scan")
    res1 = subprocess.check_call(cmd, shell=True)
    print("[*]start report")
    res2 = subprocess.check_call(cmd2, shell=True)
    print("[*]report success")
    #anaylsis xml
    xmlfile = taskid + ".xml"
    parsefile = parse(xmlfile)
    root = parsefile.documentElement
    body = root.getElementsByTagName("ReportSection")[2]
    sections = body.getElementsByTagName("GroupingSection")

    #解析fortify xml结果，入库

    for section in sections:
        result = Result()
        result.taskid = taskid
        result.issue = section.getElementsByTagName("Issue")
        result.title = section.getElementsByTagName("groupTitle")[0].childNodes[0].nodeValue
        result.level = section.getElementsByTagName("Folder")[0].childNodes[0].nodeValue
        result.desc = section.getElementsByTagName("Abstract")[0].childNodes[0].nodeValue
        result.filepath = section.getElementsByTagName("FilePath")[0].childNodes[0].nodeValue
        result.line = section.getElementsByTagName("LineStart")[0].childNodes[0].nodeValue
        result.content = section.getElementsByTagName("Snippet")[0].childNodes[0].nodeValue
        result.save()
        del result


    return "ok"


