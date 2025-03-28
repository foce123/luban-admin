FROM python:3.7
WORKDIR /app
COPY . /app
EXPOSE 8085

#  安装依赖
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
RUN python -m pip install --upgrade pip
RUN python -m pip install gunicorn
RUN python -m pip install greenlet
RUN python -m pip install eventlet
RUN python -m pip install gevent
RUN python -m pip install -r requirements.txt

#  创建数据
RUN python createDatabase.py
RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python initDatabase.py

# 修改时区
RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

# gunicorn部署 需要部署nginx 存在跨域问题， 配置文件
CMD ["gunicorn" ,"application.wsgi", "-c", "gunicorn.conf.py"]

# CMD ["python" ,"manage.py", "runserver", "0.0.0.0:8085"]
