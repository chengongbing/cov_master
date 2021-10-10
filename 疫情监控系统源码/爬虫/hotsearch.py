from selenium.webdriver import Chrome,ChromeOptions
import pymysql
import time as t
import jieba
connect=pymysql.connect(host="####",user="####",password="###",db="###")
cur=connect.cursor()

option =ChromeOptions()
option.add_argument("--headless")
option.add_argument("--no--sandbox")
url='https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_pc_1#tab1'
browser=Chrome(executable_path="/root/chromedriver",options=option)
browser.get(url)
but=browser.find_element_by_css_selector('#ptab-1 > div.Virus_1-1-316_2SKAfr > div.Common_1-1-316_3lDRV2 > span')#('#ptab-1 > div.Virus_1-1-315_2SKAfr > div.Common_1-1-315_3lDRV2 > span')
but.click()
day=browser.find_elements_by_xpath('//*[@id="ptab-1"]/div[3]/div/div[1]/span[1]')
time=browser.find_elements_by_xpath('//*[@id="ptab-1"]/div[3]/div/div[1]/span[2]')
c=browser.find_elements_by_xpath('//*[@id="ptab-1"]/div[3]/div/div[2]/a/div')
l=[]
for i in range(len(c)):
    daytime="2021-{}{}".format(day[i].text,time[i].text)
    daytime=daytime.replace('月','-').replace('日',' ')
    # print(daytime)

    # print(daytime,c[i].text)
    insert_hotcearch = "insert into hotsearch(dt,content) values(%s,%s)"
    cur.execute(insert_hotcearch,(daytime,c[i].text))
    connect.commit()
print(f"{t.asctime()}hotsearch检查更新数据完成")
cur.close()
browser.close()
connect.close()