#coding:utf-8
import pandas as pd

working_space = '/Users/Alas/Documents/TD/Top_Apps_in_China_For_Google/in_purchase_apps_in_itunes/'
path_apple_appid_from_server = working_space + 'apple_appid_from_server.txt'
path_to_write = working_space + 'to_be_crawled_apple_appid.txt'

df_to_be_crawled_apple_appid = pd.read_csv(path_apple_appid_from_server)
#print df_to_be_crawled_apple_appid.head()
#print df_to_be_crawled_apple_appid['day'].unique()

with open(path_to_write, 'wb') as f1:
    for appid in df_to_be_crawled_apple_appid['appid'].unique():
        f1.write(str(appid) + '\n')




