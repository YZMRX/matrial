import pymysql
from dbutils.pooled_db import PooledDB


class pysql:
    def __init__(self):
        # self.db = pymysql.connect(
        #     host="127.0.0.1",
        #     user="root",
        #     password='942021',
        #     database='massage',
        #     port=3306,
        #     cursorclass=pymysql.cursors.DictCursor
        # )
        db_config = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'passwd': '942021',
            'db': 'material',
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor,
            'maxconnections': 0,  # 连接池允许的最大连接数
            'mincached': 4,  # 初始化时连接池中至少创建的空闲的连接，0表示不创建
            'maxcached': 0,  # 连接池中最多闲置的连接，0表示不限制，连接使用完成后的空闲连接保留数。
            'maxusage': 5,  # 每个连接最多被重复使用的次数，None表示不限制
            'blocking': True  # 连接池中如果没有可用连接后是否阻塞等待，
            # True 等待，让用户等待，尽可能的成功； False 不等待然后报错，尽快告诉用户错误，例如抢购，不成功就提示。

        }
        self.spool = PooledDB(pymysql, **db_config)
        self.db = self.spool.connection()
        self.cursor = self.db.cursor()

    # 查
    # 单个数据
    def check(self, sql, params):
        self.db = self.spool.connection()
        self.cursor = self.db.cursor()
        try:
            self.cursor.execute('select * from data where id = %s', params)
            result = self.cursor.fetchone()
            return result
        except:
            print("查询异常")
            return False

        # 全部数据

    def checkAll(self):
        self.db = self.spool.connection()
        self.cursor = self.db.cursor()
        try:
            self.cursor.execute("select * from data")
            results = self.cursor.fetchall()
            for i in range(len(results)):
                results[i]['time'] = results[i]['time'].strftime('%Y-%m-%d %H:%M:%S')
            return results
        except:
            print("查询异常")

    # 增
    def AddData(self, sql, params):
        self.db = self.spool.connection()
        self.cursor = self.db.cursor()
        try:
            self.cursor.execute(
                'insert into material.data (material, material_use, minTemperature, maxTemperature, CurrentTemperature, minHumidity, maxHumidity, CurrentHumidity, minForce, maxForce, CurrentForce, amplitude, time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW())',
                params)
            self.db.commit()
            return True
        except:
            print("插入失败")
            self.db.rollback()
            return False

    # 删
    def deleteData(self, sql, params):
        self.db = self.spool.connection()
        self.cursor = self.db.cursor()
        try:
            self.cursor.execute('delete from data where id=%s', params)
            self.db.commit()
            return True
        except:
            print("删除失败")
            self.db.rollback()
            return False

    # 改
    def updata(self, sql, params):
        self.db = self.spool.connection()
        self.cursor = self.db.cursor()
        try:
            self.cursor.execute(sql, params)
            self.db.commit()
            return True
        except:
            print("修改失败")
            self.db.rollback()
            return False

    # 搜索数据
    def search(self, param):
        self.db = self.spool.connection()
        self.cursor = self.db.cursor()
        try:
            self.cursor.execute("select * from data where material=%s ", param)
            results = self.cursor.fetchall()
            return results
        except:
            print("查询异常")
        return None

    # 查询损耗比
    def look_rate(self, param):
        self.db = self.spool.connection()
        self.cursor = self.db.cursor()
        try:
            self.cursor.execute("select * from rate where id=%s ", param)
            results = self.cursor.fetchone()
            return results
        except:
            print("查询异常")

    def update_rate(self, params):
        self.db = self.spool.connection()
        self.cursor = self.db.cursor()
        try:
            self.cursor.execute("update rate set t_rate=%s,h_rate=%s,f_rate=%s where id=%s", params)
            print(200)
            self.db.commit()
        except:
            print("插入异常")
            self.db.rollback()


