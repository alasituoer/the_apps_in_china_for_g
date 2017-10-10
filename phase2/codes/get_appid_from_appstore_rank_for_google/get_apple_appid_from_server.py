#coding:utf-8
import pandas as pd
import MySQLdb
import sys

# 从60.205.163.159服务器的AppStore_Rank数据库中下载指定日期的畅销榜排名
# 包含所有字段, 存入文件 apple_appid_from_server.txt 中

# 每期开始时, 需要修改phase2为phase3或phase4
# 还有第30行左右的MySQL查询语句中 对于时间的限定条件(目前是查询2017年7月和8月的所有应用)
working_space = '/Users/Alas/Documents/TD_handover/the_apps_in_china_for_google/phase2/'
path_to_write = working_space + 'in_purchase_and_revenue/apple_appid_from_server/'
name_to_write = 'apple_appid_from_server.txt'

try:
    conn = MySQLdb.connect(
        host = ‘*’,
        port = 3306,
        user = ‘*’,
        passwd = ‘*’,
        db = ‘*’,
        charset = 'utf8')
except Exception, e:
    print e
    sys.exit()

cursor = conn.cursor()

# 在此处更改查询语句的时间来限定范围
mysql = """select * from app_history
        where cat=36 and tab=2 and 
        (day like '2017-07-%' or day like '2017-08-%')"""
try:
    df_selected_data = pd.read_sql(mysql, conn)
except Exception, e:
    print e

df_selected_data.to_csv(path_to_write + name_to_write, index=False)

conn.close()




