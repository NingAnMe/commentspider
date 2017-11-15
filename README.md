# commentspider

评论爬虫，抓取各网站的评论，用来进行情感分析

目前支持：
微博评论（m.weibo.cn）：9W条/小时
豆瓣电影评论（movie.douban.com）：6W条/小时


# 开发环境

系统：Ubuntu 16.04

数据库： MongoDB 3.2.17

Python版本： Python2


# 使用

```
$ git clone git@github.com:NingAnMe/renrenspider.git

$ cd renrenspider

$ pip install -r requirements.txt

# 获取网站cookies
$ python getcookies.py

# 配置 settings.py 文件的数据库信息

# 修改爬虫内的开始链接，运行对应的爬虫，'weibo'，'douban'
$ scrapy crawl weibo

```

# 安装

### 安装MongoDB

```
$ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
$ echo "deb http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list
$ sudo apt-get update
$ sudo apt-get install -y mongodb-org
```

# TO-DO

- 完成获取cookies功能 [√]

- 完成微博评论的采集功能 [√]

- 完成豆瓣电影评论的采集功能 [√]
