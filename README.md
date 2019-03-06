# CodeScanner
A code security platform based on fortify sca windows

## 功能

后端基于fortify sca的一款自动化代码审计管理平台

可以在CI流程中嵌入，可自动化拉取gitlab代码仓库或手动上传代码包进行代码审计

本系统包含基本功能，可以使用Celery轻易扩展其他功能

基于python3 + celery +redis + sqlite3开发，适用Windows

## 依赖

python3 redis celery djcelery

## 使用

### 1 安装代码

<pre>
  git clone https://github.com/0FuzzingQ/CodeScanner.git
  cd mysite
  </pre>
  
### 2 同步数据库

<pre>
  python3 manage.py makemigrations
  python3 manage.py migrate
  </pre>
  
### 3 开启celery队列 + web

<pre>
  celery worker -A mysite -l debug -P eventlet
  python manage.py runserver
  </pre>
  
## demo

[a](c:\\users\\aldin\\desktop\\cs.JPG)
