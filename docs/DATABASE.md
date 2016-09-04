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

Creating the database
===
You will need to setup a MySQL server which can be downloaded [here](https://dev.mysql.com/downloads/mysql/) if you are new to SQL development, it is recommended to install MySQL Workbench [here](https://dev.mysql.com/downloads/workbench/5.2.html). After setting up your database environment, you will need to create a database and tables in it. Schema info can be found in `schema.txt` in project root.

Populating the database
===
Place the `data.csv` and `show_eps.tsv` files into `C:/ProgramData/MySQL/MySQL Server 5.7/Uploads` for Windows.


imdbInfo
---
```sql
LOAD DATA INFILE "C:/ProgramData/MySQL/MySQL Server 5.7/Uploads/data.csv"
INTO TABLE imdbInfo
COLUMNS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES;
```
episode2show
---
```sql
LOAD DATA INFILE "C:/ProgramData/MySQL/MySQL Server 5.7/Uploads/show_eps.csv"
INTO TABLE episode2show
COLUMNS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES;
```

Setting up the app
===
Currently, variables for MySQL is stored in your variables for security reasons. You will need to set `USER` variable to your preferred MySQL username (typically `root`) and `PW` variable as your password for MySQL user and `DBNAME` as you guessed it, your database name.

For `Windows`, just type path into your search and click first item. Then add the needed variables (you can probably do this in commandline but this is recommended).

For `Linux`:

```bash
export USER=mysql_user
export PW=mysql_password
export DBNAME=mysql_db
```