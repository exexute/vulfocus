FROM python:3
LABEL maintainer="owef <owefsad@gmail.com>" version="0.3.2.1" description="Vulfocus for k8s"
EXPOSE 80
RUN mkdir /vulfocus-api/
WORKDIR /vulfocus-api/

ADD vulfocus-api/requirements.txt /vulfocus-api/requirements.txt
ADD /vulfocus-api/sources.list /etc/apt/sources.list
ADD /vulfocus-api/nginx.conf /etc/nginx/nginx.conf
ADD /vulfocus-api/default /etc/nginx/sites-available/default
ADD /vulfocus-api/default /etc/nginx/sites-enabled/default

ENV DOCKER_URL="unix://var/run/docker.sock"
RUN apt update && \
    apt upgrade -y && \
    apt install redis-server -y && \
    apt install nginx -y && \
    rm -rf /var/www/html/* && \
    apt install -y openjdk-8-jre-headless
RUN python3 -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple some-package -r requirements.txt &&

COPY vulfocus-api /vulfocus-api/
RUN chmod u+x /vulfocus-api/run.sh
ADD autobuild/app.jar /vulfocus-api/
ADD vulfocus-frontend/dist/ /var/www/html/

CMD ["sh", "run.sh"]