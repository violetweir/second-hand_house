import pymysql
from dbutils.pooled_db import PooledDB

# 创建连接池对象
pool = PooledDB(creator=pymysql,
    maxconnections=100,
    mincached=10,
    maxcached=20,
    maxshared=10,
    blocking=True,
    maxusage=100,
    setsession=None,
    charset= 'UTF8',
    host='localhost',
    port=3306,
    database='cdhouse',
    user='root',
    password='123456'
)

def getCon():
    # 从连接池中获取数据库连接
    con = pool.connection()
    return con