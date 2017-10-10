#coding:utf-8
import sys
import scrapy

# 从服务器下载的近三个月的畅销榜应用只有 苹果应用ID -> 当天每个小时的排名值
# 需要再由苹果应用ID到ASO100上得到对应的包名, 还有中文名

class UpdateVersionAso100Spider(scrapy.Spider):
    name = 'get_pkname_with_appid_from_aso100'
    allowed_domains = ['aso100.com']
    start_urls = ['https://aso100.com']
    working_space = '/Users/Alas/Documents/TD/Top_Apps_in_China_For_Google/in_purchase_apps_in_itunes/lookup_table_pkname_with_appid_from_aso100/'

    # 待爬取apps_apple_appid文件
    path_to_be_crawled_apps_apple_appid = working_space +\
            'apple_appid_given_apps/apple_appid_given_apps_p4.txt'
    # 已爬取apps_apple_appid文件
    path_crawled_apps_apple_appid = working_space +\
            'apple_appid_given_apps/apple_appid_crawled_apps.txt'
    # 存放爬取到的文件
    path_crawled_results = working_space + 'crawled_results/'

    def parse(self, response):
        # 打开待爬取的apps_apple_appid文件
        with open(self.path_to_be_crawled_apps_apple_appid, 'r') as f1:
            # 再打开已爬取的apps_apple_appid文件
            with open(self.path_crawled_apps_apple_appid, 'r') as f2:
                # 将已爬取的苹果应用id放入一个列表中
                list_apps_apple_appid_crawled = []
                for info in f2.readlines():
                    list_apps_apple_appid_crawled.append(info.split('\t')[0].strip())
                #print list_apps_apple_appid_crawled

                #if 'li' in 'limingzhi':
                #    line = f1.readline()
                # 从待爬取文件中挨个读入苹果应用id来构造爬取网址
                for line in f1.readlines():
                    app_apple_appid, app_name = [i.strip() for i in line.split('\t')]
                    #print [app_apple_appid, app_name]

                    # 如果该ID在已爬取文件中, 则跳过此次爬取行为(或称循环)
                    if app_apple_appid in list_apps_apple_appid_crawled:
                        continue

                    # 根据 apple appid 构造网址
                    url = 'https://aso100.com/app/rank/appid/' + app_apple_appid
                    meta_source = {'app_apple_appid': app_apple_appid, 'app_name': app_name,}
                    yield scrapy.Request(url, callback=self.GetPkname, meta=meta_source,)


    def GetPkname(self, response):
        #print response.url
        if response.status == 200:
            for sel in response.xpath("//ul[@class='nav nav-tabs']/li[2]"):
                url =  'https://aso100.com' + sel.xpath("a/@href").extract()[0]
                meta_source = {'app_apple_appid': response.meta['app_apple_appid'],
                        'app_name': response.meta['app_name'],}
                yield scrapy.Request(url, callback=self.ToWriteCSV, meta=meta_source,)

    def ToWriteCSV(self, response):
        #print response.body
        if response.status == 200:
            list_appinfo = [response.meta['app_apple_appid'], response.meta['app_name'],]
            for sel in response.xpath("//p[@class='content text']"):
                try:
                    list_appinfo.append(sel.xpath("text()").extract()[0])
                except:
                    list_appinfo.append('')
#            print list_appinfo


            with open(self.path_crawled_results + 'crawled_result.txt', 'ab') as f1:
                to_write_strings = ''
                for i in list_appinfo:
                    to_write_strings += str(i)
                    to_write_strings += '\t'
                to_write_strings = to_write_strings[:-1]
                to_write_strings += '\n'
                f1.write(to_write_strings)

            # 将成功爬取数据的apps_apple_appid存放于一个单独文件
            to_write_crawled_apple_appid = response.meta['app_apple_appid'] + '\t' +\
                    response.meta['app_name'] + '\n'
            with open(self.path_crawled_apps_apple_appid, 'ab') as f1:
                f1.write(to_write_crawled_apple_appid)


