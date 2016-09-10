FROM ubuntu:16.04
MAINTAINER Mike Tung

#install the py ppa
RUN echo "deb http://ppa.launchpad.net/fkrull/deadsnakes/ubuntu xenial main" > /etc/apt/sources.list.d/deadsnakes.list \
    && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys DB82666C

#install ubuntu packages
RUN DEBIAN_FRONTEND=noninteractive apt-get update --fix-missing && apt-get install -y \
    build-essential \
    autoconf \
    libtool \
    pkg-config \
    python3 \
    python3-dev \
    python3-setuptools \
    python3-pip \
    cython \
    wget \
&& apt-get clean \
&& apt-get autoremove \
&& rm -rf /var/lib/apt/lists/*

#Pip install app packages
COPY ./requirements.txt /Watchdog/requirements.txt
RUN pip3 install -r /Watchdog/requirements.txt

#install mysql-connector for python
COPY ./setupMySQLConnector.bash /Watchdog/connector.bash
RUN bash /Watchdog/connector.bash

#move project over
COPY ./authentication /Watchdog/authentication
COPY ./data /Watchdog/data
COPY ./data_model /Watchdog/data_model
COPY ./docs /Watchdog/docs
COPY ./static /Watchdog/static
COPY ./templates /Watchdog/templates
COPY ./watchdog /Watchdog/watchdog
COPY ./run_flask_app.py /Watchdog/run_flask_app.py
COPY ./setting.py /Watchdog/setting.py

#set timezone
RUN echo "America/New_York">/etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata

#set WD
WORKDIR /Watchdog