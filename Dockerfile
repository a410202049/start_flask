FROM python:2.7

# set timezone
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY . ./
RUN pip install -i https://pypi.douban.com/simple/ -r requirements.txt
RUN mkdir -p /var/log/gunicorn
#CMD ["gunicorn", "app:app", "-c", "gunicorn.conf.py"]