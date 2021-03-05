#  encoding: utf-8
from bs4 import BeautifulSoup
import requests

def get_all():
    kuaidi_all = "https://www.kuaidi100.com/all/"

    html = requests.get(kuaidi_all)
    html.encoding = "utf-8"
    text = html.text


    soup = BeautifulSoup(text, "lxml")
    # print(soup)
    dl = soup.find("dl",{"class": "stocklist"}).find_all("img")
    for dd in dl:
        name = dd.attrs["alt"].replace("查询", "").replace("单号","")
        k = dd.attrs["src"].split("_")[0].split("/")[-1]
        print("%s -- %s" % (name, k))



def get_k():
    url = "http://www.kuaidi100.com/query?type=huitongkuaidi&postid=71303608207839"
    html = requests.get(url)
    print(html.json())

if __name__ == '__main__':
    get_k()
