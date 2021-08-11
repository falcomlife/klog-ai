FROM swr.cn-north-4.myhuaweicloud.com/cotte-bigdata/python-base:3.8.5
ARG CONTAINERNAME

WORKDIR /opt
RUN mkdir -p /opt/analy/src
#copy config to container
#COPY ./dist/analy-0.0.1-py3-none-any.whl /opt/analy/
COPY ./src /opt/analy/src

#RUN python3 -m pip install ./analy/analy-0.0.1-py3-none-any.whl
WORKDIR /opt/analy/src/core/
# modify timezone
COPY ./Shanghai /etc/localtime
RUN echo "Asia/Shanghai" > /etc/timezone
RUN chmod 755 -R /opt/analy/src/
#modify Character set
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
ENV LC_ALL en_US.UTF-8