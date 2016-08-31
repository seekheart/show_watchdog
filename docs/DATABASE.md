MySQL Support
===
The app uses mysql as database solution, used sql library is flask_sqlalchemy.

To use SQLAlchemy with mysql, you will need to install a mysql driver.

Driver used in this project is Connector/Python by Oracle

Connector/Python Setup
===

Windows
---
Download the zip file from [here](http://dev.mysql.com/downloads/connector/python/) (its "Platform Independent" in dropdown menu), unzip it, then run this on an elevated cmd window:

```
setup.py install
```

Unix
---

Tarball can be found [here](http://dev.mysql.com/downloads/connector/python/)
```
sudo wget http://cdn.mysql.com//Downloads/Connector-Python/mysql-connector-python-2.1.3.tar.gz
tar -zxvf mysql-connector-python-2.1.3.tar
cd mysql-connector-python-2.1.3
sudo python3 setup.py install
```