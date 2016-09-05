#!/bin/sh
wget http://cdn.mysql.com//Downloads/Connector-Python/mysql-connector-python-2.1.3.tar.gz
tar -xzf mysql-connector-python-2.1.3.tar.gz
cd mysql-connector-python-2.1.3
python3 setup.py install
cd ..
rm -rf mysql-connector-python-2.1.3*