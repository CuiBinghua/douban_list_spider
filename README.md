# 1. 简介
douban_list_spider.py是一个简单的爬虫，可以根据关键字抓取豆瓣电影、豆瓣读书或者豆瓣音乐的条目信息.

# 2. Python环境
本人的Python版本为：2.6.6
另外还需要安装必要的Python插件：
$ easy_install requests
$ easy_install BeautifulSoup4

# 3. 执行抓取
首先对douban_list_spider.py中的变量object、tag_list和page_num进行配置。
然后执行命令即可：
$ python douban_list_spider.py
最后，就可以在相同目录下查看到输出文件movie_list.txt、book_list.txt或者music_list.txt了。

# 4. 参考资料
http://plough-man.com/?p=379
https://github.com/plough/myCrawler/blob/master/doubanBook/book_list_spider.py