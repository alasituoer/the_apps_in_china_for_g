#coding:utf-8
import scrapy 

class AppPurchaseSpider(scrapy.Spider):
    name = 'app_purchase_spider'
    allowed_domains = ['apple.com']
    start_urls = ['https://www.apple.com/itunes/']


    working_space = '/Users/Alas/Documents/TD/Top_Apps_in_China_For_Google/in_purchase_apps_in_itunes/'


    # 待爬取apple_appid文件路径
    path_to_be_crawled = working_space + 'to_be_crawled_apple_appid.txt'
    # 已爬取apple_appid的文件路径
    path_crawled = working_space + 'crawled_apple_appid.txt'
    # 已爬取的内购数据
    path_to_write = working_space + 'result_in_purchase_info.txt'

    def parse(self, response):
        # 打开待爬取列表
        with open(self.path_to_be_crawled, 'r') as f1:
            # 打开已爬取列表
            with open(self.path_crawled, 'r') as f2:
                list_crawled_apple_appid = []
                for i in f2.readlines():
                    list_crawled_apple_appid.append(i.strip())

                for line in f1.readlines():
                    apple_appid = str(int(line))
                    # 针对爬取过一遍后的apple appid, 检查下是否在已爬取列表, 如果在则跳过
                    if apple_appid in list_crawled_apple_appid:
                        continue
                    url = 'https://itunes.apple.com/cn/app/id' + apple_appid
                    yield scrapy.Request(url, meta={'appid': apple_appid,}, callback=self.GetPurchaseInfo)

    def GetPurchaseInfo(self, response):
        if response.status == 200:
            # apple appid 对应的中文名
            for sel1 in response.xpath("//div[@id='title']/div[@class='left']/h1"):
                app_name = sel1.xpath('text()').extract()[0]
                app_name.replace(',', '').replace('，', '')

            # apple appid 对应的类别
            for sel1 in response.xpath("//div[@id='left-stack']/div[@class='lockup product application'\
                    ]/ul[@class='list']/li[@class='genre']"):
                category = sel1.xpath("a/span/text()").extract()[0]
                #print response.meta['appid'], category

            # apple appid 的内购数据(若有)
            # 内购数据的物品名与价格的文字中不能有',' '，'逗号, 方便之后导入Excel或是作为CSV格式提数计算
            for sel1 in response.xpath("//div[@class='extra-list in-app-purchases']/ol/li"):
                in_app_title = sel1.xpath("span[1]/text()").extract()[0]
                in_app_price = sel1.xpath("span[2]/text()").extract()[0]
                in_app_title.replace(',', '').replace('，', '')
                in_app_price.replace(',', '').replace('，', '')
                #print response.meta['appid'], app_name, in_app_title, in_app_price

                # 追加写入已爬取到的内购数据
                to_write_strings = response.meta['appid'] + ',' + category + ',' + app_name + ',' +\
                        in_app_title + ',' + in_app_price + '\n'
                with open(self.path_to_write, 'ab') as f3:
                    f3.write(to_write_strings)

                # 记录已爬取的apple appid, 供检查爬漏的
            with open(self.path_crawled, 'ab') as f4:
                f4.write(response.meta['appid'] + '\n')


