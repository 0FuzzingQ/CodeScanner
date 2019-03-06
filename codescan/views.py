# -*- coding:utf-8 -*-
from django.shortcuts import render,HttpResponse
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .forms import AddTask
from .models import Task,Result
from .tasks import add
import datetime
import os
import hashlib
import psutil
import platform
import time
# Create your views here.


#文件代码上传函数
def upload_file(myFile):  
	#myFile =request.FILES.get("file", None)
	print(myFile)    
	if myFile == None: 
		#print("nooooooooo") 
		return False  
	destination = open(os.path.join("upload\\",myFile.name),'wb+')   
	
	#分块上传代码包
	for chunk in myFile.chunks(): 
		destination.write(chunk)  
	destination.close()  
	return  os.path.join("upload\\",myFile.name)

def addtask(request):

	if request.method == 'POST':

		task = Task()
		task.name = request.POST.get('taskname')
		task.method = request.POST.get('method')
		task.java = '1' if request.POST.get('java') else '0'
		task.other = request.POST.get('other')

		#按照gitlAB拉取或前端上传定义不同的文件路径

		task.filepath = upload_file(request.FILES.get("file", None)) if (request.POST.get('method') == 'a') else request.POST.get('address')
		task.datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

		task.taskid = hashlib.md5(task.datetime.encode('utf-8')).hexdigest()
		#保存模型
		task.save()
		#前端上传延时
		time.sleep(5)
		#添加后端celery扫描任务
		res = add.delay(task.filepath,task.taskid)
		return HttpResponse(request.FILES.get("file", None))

	else:

		return render(request, 'form.html')

#任务列表页
def task(request):

	tasklist = Task.objects.all()
	paginator = Paginator(tasklist,10)
	page = request.GET.get('page')
	try :
		tasklist = paginator.page(page)
	except PageNotAnInteger:
		tasklist = paginator.page(1)
	except EmptyPage:
		tasklist = paginator.page(paginator.num_pages)
	
	return render(request,'table-list.html',{'tasklist':tasklist})

#按任务显示漏洞列表页	
def result(request):

	taskid = request.GET.get('taskid')
	resultlist = Result.objects.filter(taskid=taskid)
	paginator = Paginator(resultlist,10)
	page = request.GET.get('page')
	try :
		resultlist = paginator.page(page)
	except PageNotAnInteger:
		resultlist = paginator.page(1)
	except EmptyPage:
		resultlist = paginator.page(paginator.num_pages)
	return render(request,'result.html',{'resultlist':resultlist})


#漏洞详情页
def detail(request):

	vulnid = request.GET.get("id")
	detail = Result.objects.filter(id=vulnid)
	#print(detail)
	detail[0].content.replace('{','{111')
	print(detail[0].content)
	return render(request,'detail.html',{'detail':detail})


#主页
def index(request):

	

	#获取系统版本，系统资源占用
	os_banner = platform.platform()
	mem = psutil.virtual_memory()
	
	mem_per = str(mem.percent) + "%"
	cpu_per = str(psutil.cpu_percent(1)) + "%"
	system_info = [os_banner,mem_per,cpu_per]

	#统计任务，漏洞数量
	taskcount = Task.objects.all().count()
	resultcount = Result.objects.all().count()
	infocount = Result.objects.filter(level = 'Info').count()
	lowcount = Result.objects.filter(level = 'Low').count()
	midcount = Result.objects.filter(level = 'High').count()
	highcount = Result.objects.filter(level = 'Critical').count()

	taskmonthcount = 0
	resultmonthcount = 0
	taskall = Task.objects.all()
	now = str(datetime.datetime.now().month) if len(str(datetime.datetime.now().month)) == 2 else ("0" + str(datetime.datetime.now().month))
	for i in range(0,taskcount):
		if taskall[i].datetime.split('-')[1] == now:
			taskmonthcount = taskmonthcount + 1
			resultmonthcount = resultmonthcount + Result.objects.filter(taskid = taskall[i].taskid).count()
		else:
			pass


	vuln_count = [taskcount,resultcount,infocount,lowcount,midcount,highcount,taskmonthcount,resultmonthcount]
	#月份统计
	month_1 = 0
	month_2 = 0
	month_3 = 0
	month_4 = 0
	for i in range(0,taskcount):
		if int(taskall[i].datetime.split('-')[1]) + 1 == int(now):
			month_1 = month_1 + 1
		if int(taskall[i].datetime.split('-')[1]) + 2 == int(now):
			month_2 = month_2 + 1
		if int(taskall[i].datetime.split('-')[1]) + 3 == int(now):
			month_3 = month_3 + 1
		if int(taskall[i].datetime.split('-')[1]) + 4 == int(now):
			month_4 = month_4 + 1
	month_count = [month_4,month_3,month_2,month_1,taskcount,(int(now)-4)%12,(int(now)-3)%12,(int(now)-2)%12,(int(now)-1)%12,(int(now))%12]
	for i in range(5,10):
		if month_count[i] == 0:
			month_count[i] = 12

	return render(request, 'index.html',{'system_info' : system_info,'vuln_count':vuln_count,'month_count':month_count})