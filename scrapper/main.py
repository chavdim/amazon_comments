#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import io

print("please input URL")
my_urls = input()


urls = []

current_url = my_urls
req = requests.get(current_url,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36'})
html = req.text


for n in range(24):
    ind = html.index("a-section a-spacing-none a-inline-block s-position-relative")
    ind2 = html.index("s-access-image cfMarker")
    html2 = html[ind:ind2]
    html = html[ind2+20:]
    ind = html2.index("href=")
    ind = ind + 6
    ind2 = html2.index("><img")
    ind2 = ind2 -1
    html2 = html2[ind:ind2]
    urls.append(html2)
    


for current_url in urls:
    req = requests.get(current_url,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36'})
    html = req.text
    if "a-link-emphasis a-nowrap" not in html :
        continue
    ind = html.index("a-link-emphasis a-nowrap")
    if "すべてのカスタマーレビューを見る" not in html :
        continue
    ind2 = html.index("すべてのカスタマーレビューを見る")
    ind2 = ind2 - 2
    html = html[ind:ind2]
    ind = html.index("https")
    a_r_url = html[ind:]

    current_url = a_r_url
    req = requests.get(current_url,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36'})
    html = req.text
    if "a-last" not in html :
        continue
    ind = html.index("a-last")
    ind2 = ind -24
    sub_num = html[ind2:ind]
    ind = sub_num.index("</a>")
    ind2 = sub_num.index(">") + 1
    max_num = sub_num[ind2:ind]

    html_file = open("url.csv",'a',encoding='utf8')
    html_file.write(current_url)
    html_file.write("&pageNumber=1,")
    html_file.write(max_num)
    html_file.write("\n")
    html_file.close()



import getCommentsHtml
import get_comments
