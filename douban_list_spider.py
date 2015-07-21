#!/usr/bin/env python
# encoding: utf-8

# --------------------------------------------
# Author: CuiBinghua <i_chips@qq.com>
# Date: 2015-07-20 20:05:00
# --------------------------------------------

"""douban_list_spider.py是一个简单的爬虫，可以根据关键字抓取豆瓣电影、豆瓣读书或者豆瓣音乐的条目信息.
"""


# 把str编码由ascii改为utf8（或gb18030）
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import time
import re
import requests
from bs4 import BeautifulSoup


# ==================== 可配置参数 start ====================

object = 'movie' # 抓取对象
tag_list = ['动作','科幻','惊悚'] # 感兴趣的任意关键字
page_num = 2 # 每个标签抓取的页数, 必须为正整数

# object = 'book' # 抓取对象
# tag_list = ['经济学','中国历史','科普'] # 感兴趣的任意关键字
# page_num = 1 # 每个标签抓取的页数, 必须为正整数

# object = 'music' # 抓取对象
# tag_list = ['莫扎特','贝多芬'] # 感兴趣的任意关键字
# page_num = 2 # 每个标签抓取的页数, 必须为正整数

# ==================== 可配置参数 end ====================


file_content = '抓取时间：' + time.asctime() + '\n' # 最终要写到文件里的内容
file_partial_name = '_list.txt'


def print_encode(s):
    print s
    # print s.encode("gb18030")


def get_rating(rating):
    if (rating is not None):
        return rating.string.strip()
    else:
        return '未知'


def check_if_year_or_not(string):
    year = re.findall("\d{4}$", string)
    if 0 == len(year):
        return False
    else:
        return True


def movie_spider(soup, item_num):
    global file_content

    list_soup = soup.find('div', {'class': 'mod movie-list'})
    for douban_info in list_soup.findAll('dd'):
        title = douban_info.find('a', {
            'class':'title'}).string.strip()
        desc = douban_info.find('div', {'class':'desc'}).string.strip()
        desc_list = desc.split('/')
        country_info =  '制片国家/地区：' + desc_list[0]
        type_info =     '类型：        ' + '/'.join(desc_list[1:-5])
        time_info =     '上映时间：    ' + desc_list[-5]
        director_info = '导演：        ' + desc_list[-4]
        actor_info =    '主演：        ' + '/'.join(desc_list[-3:])
        rating = douban_info.find('span', {
            'class':'rating_nums'})
        rating = get_rating(rating)
        file_content += "*%d\t《%s》\t评分：%s\n\t%s\n\t%s\n\t%s\n\t%s\n\t%s\n\n" % (
            item_num, title, rating, country_info, type_info, time_info, director_info, actor_info)
        item_num += 1


def book_spider(soup, item_num):
    global file_content

    list_soup = soup.find('div', {'class': 'mod book-list'})
    for douban_info in list_soup.findAll('dd'):
        title = douban_info.find('a', {
            'class':'title'}).string.strip()
        desc = douban_info.find('div', {'class':'desc'}).string.strip()
        desc_list = desc.split('/')
        # 一般情况下, 出版时间会被拆分到desc_list[-2]
        # 但是如果出版时间是2008/6这种格式, 2008会被拆分到desc_list[-3], 6会被拆分到desc_list[-2], 就需要特殊处理
        if (check_if_year_or_not(desc_list[-3])):
            split_pos = -4
        else:
            split_pos = -3
        author_info = '作者/译者：' + '/'.join(desc_list[0:split_pos])
        pub_info =    '出版信息：' + '/'.join(desc_list[split_pos:])
        rating = douban_info.find('span', {
            'class':'rating_nums'})
        rating = get_rating(rating)
        file_content += "*%d\t《%s》\t评分：%s\n\t%s\n\t%s\n\n" % (
                item_num, title, rating, author_info, pub_info)
        item_num += 1


def music_spider(soup, item_num):
    global file_content

    list_soup = soup.find('div', {'class': 'mod music-list'})
    for douban_info in list_soup.findAll('dd'):
        title = douban_info.find('a', {
            'class':'title'}).string.strip()
        desc = douban_info.find('div', {'class':'desc'}).string.strip()
        desc_info = '音乐信息：' + desc
        rating = douban_info.find('span', {
            'class':'rating_nums'})
        rating = get_rating(rating)
        file_content += "*%d\t《%s》\t评分：%s\n\t%s\n\n" % (
                item_num, title, rating, desc_info)
        item_num += 1


def each_page_spider(douban_tag, page):
    global file_content

    item_num = page * 15 # 每页有15个条目
    url = "http://www.douban.com/tag/%s/%s?start=%d" % (douban_tag, object, item_num)
    item_num += 1
    source_code = requests.get(url)
    # just get the code, no headers or anything
    plain_text = source_code.text
    # BeautifulSoup objects can be sorted through easy
    soup = BeautifulSoup(plain_text, "lxml")

    print_encode('正在抓取%s的第%d页信息...' % (douban_tag, page + 1))
    if (object == 'movie'):
        movie_spider(soup, item_num)
    elif (object == 'book'):
        book_spider(soup, item_num)
    elif (object == 'music'):
        music_spider(soup, item_num)


def douban_spider(douban_tag):
    global file_content

    title_divide = '\n' + '--' * 30 + '\n' + '--' * 30 + '\n'
    file_content += title_divide + '\t' * 4 + \
            douban_tag + '：' + title_divide

    for page in range(0, page_num):
        each_page_spider(douban_tag, page)


def do_spider():
    print_encode('准备开始抓取...')
    for douban_tag in tag_list:
        douban_spider(douban_tag)


def do_write():
    """将最终结果写入文件"""
    file_name = object + file_partial_name
    print_encode('正在将抓取信息写入到文件%s中...' % file_name)
    f = open(file_name, 'w')
    f.write(file_content)
    f.close()
    print_encode('抓取完毕，请到文件%s中查看抓取信息...' % file_name)


def main():
    if object not in ['movie','book','music']:
        print_encode('抓取对象的取值%s无效! 请为object设置movie, book或music中的任一值...' % object)
        return

    if (type(page_num) != type(1)) or (page_num <= 0):
        print_encode('抓取页数的取值%s无效! 请为page_num设置一个正整数...' % page_num)
        return

    do_spider()
    do_write()


main()