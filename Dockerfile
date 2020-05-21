FROM python:3.7.5
RUN echo 'Asia/Shanghai' > /etc/timezone
RUN mkdir /midplatform
COPY run.sh /midplatform
COPY requirements.txt  /midplatform
WORKDIR /midplatform/
RUN chmod 777 run.sh
RUN  pip install -r /midplatform/requirements.txt -i  http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
RUN rm -rf /usr/local/lib/python3.7/site-packages/django/contrib/admin/widgets.py
ADD widgets.py /usr/local/lib/python3.7/site-packages/django/contrib/admin/widgets.py
EXPOSE 8989
CMD ["/bin/sh","run.sh"]