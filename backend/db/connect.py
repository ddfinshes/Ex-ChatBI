import psycopg2 ##导入

## 通过connect方法，创建连接对象 conn
## 这里连接的是本地的数据库
conn = psycopg2.connect(database="chatbi", user="postgres", password="123456", host="127.0.0.1", port="5432")

## 执行之后不报错，就表示连接成功了！
print('postgreSQL数据库“db_test”连接成功!')