# Scrapy-浅涉

## 一、初窥Scrapy

Scrapy是用于爬取网站和提取结构化数据的应用程序框架，可用于各种有用的应用程序，如数据挖掘、信息处理或历史归档。

网站地址：[Scrapy教程](https://oner-wv.gitbooks.io/scrapy_zh/content/%E7%AC%AC%E4%B8%80%E6%AD%A5/%E5%88%9D%E7%AA%A5scrapy.html)

以一个简单的爬虫例子，来了解Scrapy。

```python
import scrapy
class QuotesSprider(scrapy.Spider):
    name = "quotes"
    start_urls = ['http://quotes.toscrape.com/tag/humor/', ]
    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.xpath('span/small/text()').extract_first(),
            }
        next_page = response.css('li.next a::attr("href")').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
```

使用`scrapy runspider xxx.py -o quotes.json`命令可运行该程序，并将结果输出至当前目录下。

当执行命令时，Scrapy会在其中寻找一个Spider的定义，并通过框架的爬虫引擎执行它。

抓取开始时从`start_urls` 属性中定义的URLs发出请求，并调用默认的回调（callback）方法`parse`，将`response`对象作为参数传递。在`parse`中，我们使用CSS选择器来遍历 quote 元素，`yield`一个带有提取的text和author的Python dict，查找下一个链接，使用相同的`parse`方法作为回调来调度另一个请求。

Scrapy的一个主要优点：请求是被[异步调度和处理](https://docs.scrapy.org/en/latest/topics/architecture.html#topics-architecture)的。

Scrapy的其它优点：

-   内置支持使用扩展的CSS选择器和XPath表达式从HTML / XML源 [选择和提取](https://oner-wv.gitbooks.io/scrapy_zh/content/%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/%E9%80%89%E6%8B%A9%E5%99%A8.html#topics-selectors) 数据，以及使用正则表达式提取的帮助方法。
-   一个 [交互式shell控制台](https://oner-wv.gitbooks.io/scrapy_zh/content/%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/scrapy%E7%BB%88%E7%AB%AF.html#topics-shell) （IPython感知），用于尝试CSS和XPath表达式来抓取数据，在写或调试爬虫时非常有用。
-   内置支持以多种格式（JSON，CSV，XML）生成 [Feed导出](https://oner-wv.gitbooks.io/scrapy_zh/content/%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/feed%E5%AF%BC%E5%87%BA.html#topics-feed-exports) 并将它们存储在多个后端（FTP，S3，本地文件系统）
-   对于处理非英语，非标准的和错误的编码声明，提供了强大支持和自动检测。
-   强大的可扩展性支持，允许您使用 [信号(signals)](https://oner-wv.gitbooks.io/scrapy_zh/content/%E6%89%A9%E5%B1%95Scrapy/%E4%BF%A1%E5%8F%B7.html#topics-signals) 和定义明确的API（中间件，[扩展](https://oner-wv.gitbooks.io/scrapy_zh/content/%E6%89%A9%E5%B1%95Scrapy/%E6%89%A9%E5%B1%95.html#topics-extensions) 和 [管道](https://oner-wv.gitbooks.io/scrapy_zh/content/%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/item%E7%AE%A1%E9%81%93.html#topics-item-pipeline) ）插入自己的功能。
-   广泛的内置扩展和中间件处理：
-   cookies and session 处理
-   HTTP功能，如压缩，认证，缓存
-   user-agent模拟
-   robots.txt
-   爬取深度限制
-   更多
-   内置 [Telnet终端](https://oner-wv.gitbooks.io/scrapy_zh/content/%E5%86%85%E7%BD%AE%E6%9C%8D%E5%8A%A1/telnet%E7%BB%88%E7%AB%AF.html#topics-telnetconsole) ，通过在Scrapy进程中钩入Python终端，使您可以查看并且调试爬虫
-   此外，其他好东西，如可重复使用的 spiders ，从 [Sitemap](http://www.sitemaps.org/) 和XML / CSV 资讯提供中抓取网站，一个media pipeline ，用于 [自动下载与抓取](https://oner-wv.gitbooks.io/scrapy_zh/content/%E8%A7%A3%E5%86%B3%E7%89%B9%E5%AE%9A%E9%97%AE%E9%A2%98/%E4%B8%8B%E8%BD%BD%E5%B9%B6%E5%A4%84%E7%90%86%E6%96%87%E4%BB%B6%E5%92%8C%E5%9B%BE%E5%83%8F.md#topics-media-pipeline) 与项目相关联的图片（或任何其他media），缓存DNS解析程序，以及更多！


## 二、Scrapy入门教程

实现的任务：

1.  创建一个新的 Scrapy 项目
2.  编写爬虫以抓取网站并提取数据
3.  使用命令行导出已爬取的数据
4.  将爬虫更改为递归跟进链接
5.  使用爬虫参数

测试网站：[http://quotes.toscrape.com](http://quotes.toscrape.com)

### 1. 创建项目

创建命令：`scrapy startproject {projectName}`。

将创建一个具有一下内容的项目目录：

```python
{projectName}/
	scrapy.cfg		#部署配置文件
	{projectName}/		#项目的 Python 模块，从这里加入代码
		__init__.py
		items.py		#项目的 item 定义文件
		pipelines.py	#项目的 pipelines 文件
		setting.py		#项目的 setting 文件
		spiders/		#放置spider代码的目录
			__init__.py
```

### 2. 第一个爬虫

爬虫类为自定义，Scrapy用它从网站中抓取信息。它们必须子类化`scrapy.Spider`并定义初始请求，可选地如何跟踪页面中的链接，以及如何解析下载的页面内容以提取数据。

将下面代码保存到项目中`{projectName}/spiders`目录，名为`quotes_spider.py`：

```python
import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.spilt("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, "wb") as f:
            f.write(response.body)
        self.log('Saved file as %s' % filename)
```

如代码，我们的 Spider 继承了`scrapy.Spider`并定义了一些属性和方法：

*   `name`: 标识爬虫。它在项目中必须是唯一的，即，不能为不同的 Spider 设置相同的名称。
*   `start_requents()`:必须返回一个可迭代的 Requests（也可以返回一个request列表或写一个生成器函数），Spider将开始抓取。后续请求从这些初始请求中连续生成。
*   `parse()`:被调来处理 response 方法，response由每个 request 下载生成。response 参数是一个`TextResponse`的实例，它保存页面内容，并具有更多有用的方法来处理它。


`parse()`方法通常解析 response，将抓取的数据提取为 dicts，并查找要跟进的新 URL 并从中创建请求（`Request`）。

### 3. 运行爬虫

进入根目录，并执行如下命令：`scrapy crawl quotes`。

由此命令运行将我们刚才添加名为`quotes`的爬虫，并发送一些请求到`quotes.toscrape.com`域。

现在，检查当前目录中的文件。已经创建了两个文件：quotes-1.html和quotes-2.html，内容分别对应各自的 URL，作为我们的`parse`方法指示。

#### 具体过程

Scrapy 调度由 Spider 的`start_requests()`方法返回的`scrapy.Request`对象。在接收到每个 response 时，它实例化`Response`对象并调用与 request 相关联的回调方法（`parse()`方法）将 response 作为参数传递。

#### start_request 的快捷方式

可以使用一个 URL 列表来定义一个`start_urls`类属性，来代替实现一个从 URLs 生成`scrapy.Request`对象的`start_requests()`方法，此列表将由默认实现的`start_requests()`用于爬虫创建初始请求：

```python
import scrapy

class QuotesSpider(scrapy, Spider):
    name = 'quotes'
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]
    
    def parse(self, response):
        page = response.url.spilt("/")[-2]
        filename = 'quotes-%s.thml' % page
        with open(filename, "wb") as f:
            f.write(response.body)
```

将调用`parse()`方法来处理对这些 URL 的每个请求，即使我们没有明确告诉 Scrapy 这样做。因为`parse()`是 Scrapy 的默认回调方法，当请求没有显式分配回调时的请求调用。

#### 提取数据

起初尝试使用 Scrapy 终端(Scrapy Shell)选择器(selector)。运行：

```
scrapy shell 'http://quotes.toscrape.com/page/1/
```

使用shell，可以使用带有 response 对象的 CSS 选择元素：

```shell
>>> response.css('title')
[<Selector xpath='descendant-or-self::title' data='<title>Quotes to Scrape</title>'>]
```

运行`response.css('title')`结果是一个名为`SelectorList`的类似列表对象，它表示包含 XML/HTML元素的`Selector`对象列表，可以进一步精密的选择查询或提取数据。

从上面的标题中提取文本，可以：

```shell
>>> response.css("title::text").extract()
[u'Quotes to Scrape']
```

注意：

1.  在 CSS 查询中添加了`::text`，意味着选择直接`<title></title>`元素中选择文本元素。若不指定`::text`，则获取完整的 title 元素，包括其标签：`[u'<title>Quotes to Scrape</title>']`。
2.  调用`.extract()`的结果是得到一个列表，因为处理的是`SelectorList`的一个实例。当只想得到第一个结果，可以使用`extract_first()`方法。此外还可以`>>> response.css('title::text')[0].extract()`。不同的是，使用`.extract_first()`会避免`IndexError`，并且在找不到与选择匹配的元素时返回`None`。

除了`extract()`方法外，还可以使用`re`方法，使用正则表达式进行提取：

```shell
>>> response.css("title::text").re(r"Quotes.*")
[u'Quotes to Scrape']
>>> response.css("title::text").re(r"Q\w+")
[u'Quotes']
>>> response.css("title::text").re(r"(\w+) to (\w+)")
[u'Quotes', u'Scrape']
```

#### Xpath简介

Scrapy 选择器还支持使用XPath表达式：

XPath 表达式非常强大，是 Scrapy 选择器的基础。事实上，CSS 选择器转换为 XPath 。（待续）

#### 提取 quotes 和 authors

将第一个选择器分配给一个变量：`quote = response.css("div.quote")[0]`。

从得到的	`quote`对象中提取`title`，`author`和`tags`，标签是字符串列表，我们可以使用 `.extract()` 方法来获取所有的：

```shell
>>> title = quote.css("span.text::text").extract_first()
>>> title
u'\u201cThe world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.\u201d'
>>> author = quote.css("small.author::text").extract_first()
>>> author
u'Albert Einstein'
>>> tags = quote.css("div.tags a.tag::text").extract()
>>> tags
[u'change', u'deep-thoughts', u'thinking', u'world']
```

遍历所有选择器元素，并将它们放在一起，成为一个Python字典：

```shell
>>> for quote in response.css("div.quote"):
...     text = quote.css("span.text::text").extract_first()
...     author = quote.css("small.author::text").extract_first()
...     tags = quote.css("div.tags a.tag::text").extract()
...     print(dict(text=text,author=author,tags=tags))
...
{'text': u'\u201cThe world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.\u201d', 'tags': [u'change', u'deep-thoughts', u'thinking', u'world'], 'author': u'Albert Einstein'}
{'text': u'\u201cIt is our choices, Harry, that show what we truly are, far more than our abilities.\u201d', 'tags': [u'abilities', u'choices'], 'author': u'J.K. Rowling'}
{'text': u'\u201cThere are only two ways to live your life. One is as though nothing is a miracle. The other is as though everything is a miracle.\u201d', 'tags': [u'inspirational', u'life', u'live', u'miracle', u'miracles'], 'author': u'Albert Einstein'}
...
```

### 4. 在爬虫中提取数据

目前为止，爬虫只会将整个HTML页面保存到本地文件，下面将数据提取的逻辑集成到爬虫中。

Scrapy爬虫通常会生成许多包含从页面中提取的数据的字典。因此，在回调中使用 Python 的`yield`关键字：

```python
import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('span small::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            }
```

提取出的数据将在日志内输出

### 5. 存储爬虫数据

存储爬取数据最简单的方法是使用[Feed 导出(Feed exports)]()，使用以下命令：

```shell
scrapy crawl quotes -o quotes.json
```

将产生一个`quotes.json`文件，包含被抓取的项目，以 [JSON](https://zh.wikipedia.org/wiki/JSON) 序列化。

>   Scrapy 输出文件不会覆盖原内容，而是附加至给定文件，若一个文件保存数据两次，则这个 JSON 文件将不合法。

也可使用其它格式，如 [JSON Lines](http://jsonlines.org/)：`scrapy crawl quotes -o quotes.jl`

[JSON Lines](http://jsonlines.org/) 格式是流式的，可以轻松地添加新的记录。当你运行两次它没有相同的 JSON 问题。此外，由于每条记录都是单独的行，因此可以处理大文件，而无需将所有内容都放在内存中，有像 [JQ](https://stedolan.github.io/jq/) (数据格式转换工具)这样的工具可以帮助这样做。

如果要对已抓取的 Item 执行更复杂的操作，则可以编写 [Item Pipeline]() 。在创建项目时，已经在 `tutorial / pipelines.py` 中为您创建了 Item Pipeline 的占位符文件。

