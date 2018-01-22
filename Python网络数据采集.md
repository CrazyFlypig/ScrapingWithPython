# Python 爬虫

## 一、初见网络爬虫

### 1. 简单网络连接

```python
from urllib.request import urlopen
#urlopen用来打来并读取一个从网络获取的远程对象，是一个通用库
if __name__ == '__main__':
    html = urlopen("http://www.baidu.com")
    print(html.read())
```

urllib是Python的标准库，包含了从网络请求数据，处理cookie，甚至改变请求头和用户代理这些元数据的函数。

*   点击阅读[urllib库的Python文档](https://docs.python.org/3/library/urllib.html)

### 2.BeautifulSoup简介

它通过定位HTML标签来格式化和组织复杂的网络信息，用简单易用的Python对象为我们展现XML结构信息。

#### 1.2.1 安装BeautifulSoup

1.  安装pip。
2.  `>pip install beautifulsoup4`

#### 1.2.2 运行BeautifulSoup

```python
from urllib.request import urlopen
from bs4 import BeautifulSoup
if __name__ == '__main__':
    html = urlopen("https://docs.python.org/3/library/urllib.html")
    bsObj = BeautifulSoup(html.read())
    print(bsObj.h3)
```

把HTML内容传到BeautifulSoup对象，转换成下面的结构：

![TIM图片20180116151451](https://github.com/CrazyFlypig/ScrapingWithPython/blob/master/resource/image/TIM%E5%9B%BE%E7%89%8720180116151451.png)

*   任何HTML（或XML）文件的任意节点信息都可以被提取出来，只要目标信息在旁边或附近有标记就行。

#### 1.2.3 可靠的网络连接

`html = urlopen("https://docs.python.org/3/library/urllib.html")`

这行代码可能会出现两种异常：

*   网页也服务器上不存在（或者获取页面时出错）
*   服务器不存在

第一种情况发生时，程序会返回HTTP错误。urlopen函数会抛出“URLError”异常。我们可以用下面这种方式处理：

```python
try:
        html = urlopen("http://localhost:8080")
    except URLError as e:
        print(e)
        #返回空值，中断程序，或者执行另一个方案
    else:
        #程序继续。注意，如果已经在上面进行异常捕获，那么将不执行else语句
```

第二种情况是，urlopen会返回一个None对象，我们可以增加一个判断语句检测返回的html对象是不是None。

但将网页从服务器那里成功获取后，如果网页上的内容并非我们的期望，依然会出现异常。当调用BeautifulSoup对象里的一个标签时，如果这个标签不存在，就会发生AttributeError错误。需要对这种情形进行检查。

加上异常检查后的爬虫代码，也是爬虫的另一种写法：

```python
from urllib.error import  URLError
from urllib.request import urlopen
from bs4 import BeautifulSoup
def getTitle(url):
    try:
        html = urlopen(url)
    except URLError as e:
        return None
    try:
        bsObj = BeautifulSoup(html.read())
        title = bsObj.body.h1
    except AttributeError as e:
        return None
    return title;
if __name__ == '__main__':
    title = getTitle("https://www.baidu.com")
    if title == None:
        print("Title could not be found")
    else:
        print(title)
```

在写爬虫时，思考代码的总体格局，让代码即可以捕获异常又可以容易阅读。尽可能重用代码，例如：getSiteHTML和getTitle这样通用的函数。

## 二、复杂HTML解析

### 1.再端一碗BeautifulSoup

基本每个网站都会有层叠样式表（Cascading Style Sheet，CSS），CSS可以使HTML元素呈现差异化，使那些具有完全相同修饰的元素呈现出不同样式。

```python
from urllib.error import  URLError
from urllib.request import urlopen
from bs4 import BeautifulSoup
def getTitle(url):
    try:
        html = urlopen(url)
    except URLError as e:
        return None
    try:
        bsObj = BeautifulSoup(html)
        #用findAll函数抽取只包含在<span class="green"></span>标签里的文字
        namelist = bsObj.findAll("span", {"class":"green"})
    except AttributeError as e:
        return None
    return namelist;
if __name__ == '__main__':
    namelist = getTitle("http://www.pythonscraping.com/pages/warandpeace.html")
    if namelist == None:
        print("Title could not be found")
    else:
        for name in namelist:
            print(name.get_text())
```

通过BeautifulSoup对象，我们可以用findAll函数抽取只包含在\<span class="green">\</span>标签里的文字。

#####get_text()的使用和标签的保留

>   .get_text()会把你正在处理的HTML文档中的所有标签清除，然后只返回一个只包含文字的字符串。对于带有超链接、段落、和标签的大段源码，`.get_text()`会把这些超链接、段落和标签都清除掉，只剩下一串不带标签的文字。

用BeautifulSoup对象查找到你要的信息后，通常在准备打印、存储和操作数据时，最后使用`.get_text()`。一般情况下，尽可能地保留HTMl文档的标签结构。

#### 2.1.1 BeautifulSoup的find()和findAll()

BeautifulSoup文档里两个方法的定义：

```python
findAll(tag, attributes, recursive, text, limit, keywords)
find(tag, attributes, recursive, text, keywords)
```

*   标签参数tag，可以传一个标签名称或多个标签名称组成的Python列表做标签参数。
*   属性参数attributes，是一个Python字典封装一个标签的若干属性和对应的属性值。例如，下面这个函数会返回HTML文档里红色和绿色两种颜色的span标签：`.findAll("span", {"class":{"green", "red"}})`


*   递归参数recursive是一个布尔变量。若设置为True，findAll就会查找标签参数的所有子标签，以及子标签的子标签。若设置为False，findAll就只查找文档的一级标签。默认值是True。
*   文本参数text，用标签的文本内容去匹配，而不是用标签属性。假如我们想要查找前面网页中包含“the prince”内容的标签数量，我们可以使用如下代码：

```python
nameList = bsObj.findAll(text="the prince")
print(len(nameList))
```

*   范围限制参数limit，只适用于findAll方法。find等价于findAll的limit等于1时的情形。
*   关键词参数keyword，可以让你选择那些具有指定属性的标签。例如：

```python
allText = bsObj.findAll(id="text")
print(allText[0].get_text())
```

通过标签参数tag把标签列表传到`.findAll()`里获取一系列标签，其实就是一个“或”关系的过滤器，而关键字参数keyword可以让你增加一个“与”关系的过滤器来简化工作。

#### 2.1.2其它BeautifulSoup对象

*   BeautifulSoup对象

*   标签Tag对象

*   NavigableString对象

    用来表示标签里的文字

*   Comment对象

    用来查找HTML文档的注释标签，\<!--像这样的-->

#### 2.1.3 导航树

导航树的作用：通过标签在文档里的位置来查找标签。

##### 1.处理子标签和其它后代标签

子标签是一个父标签的下一级，而后代标签是指一个父标签下面所有级别的标签。

如果你只想找出子标签，可以用`.children`标签：

```python
from urllib.request import urlopen
from bs4 import BeautifulSoup
if __name__ == '__main__':
    html = urlopen("http://www.pythonscraping.com/pages/page3.html")
    bsObj = BeautifulSoup(html)
    for child in bsObj.find("table",{"id":"giftList"}).children:
        print(child)
```

`descendants()`函数是找出后代标签。

##### 2. 处理兄弟标签

BeautifulSoup的`next_siblings()`函数可以让收集表格数据变得简单，尤其是代表提行的表格：

```python
from urllib.request import urlopen
from bs4 import BeautifulSoup
if __name__ == '__main__':
    html = urlopen("http://www.pythonscraping.com/pages/page3.html")
    bsObj = BeautifulSoup(html)
    for sibling in bsObj.find("table", {"id":"giftList"}).tr.next_siblings:
        print(sibling)
```

标题行不会被打印，有两个理由：

1.  对象不能把自己作为兄弟标签。
2.  这个对象只能调用后面的兄弟标签。

##### 让标签的选择更具体

>   只使用标签也可以实现功能，但只用标签很容易丢失细节。另外，页面布局总是在不断变化的，如果显然爬虫更稳定，最好还是让标签的选择更加具体。如果有属性，就利用属性值。

`previous_siblings()`函数查找某个标签之前的一组标签。`next_sibling()`和`previous_sibling()`上面的函数作用类似，返回的是单个标签，而不是一组标签。

##### 3. 父标签处理

BeautifulSoup的父标签查找函数，parent和parents。

```python
from urllib.request import urlopen
from bs4 import BeautifulSoup
if __name__ == '__main__':
    html = urlopen("http://www.pythonscraping.com/pages/page3.html")
    bsObj = BeautifulSoup(html)
    print(bsObj.find("img", {"src":"../img/gifts/img1.jpg"}).parent.previous_sibling.get_text())
```

这段代码会打印`../gifts/img1.jpg`这个图片对应的商品价格。

实现方式：

![](https://github.com/CrazyFlypig/ScrapingWithPython/blob/master/resource/image/2.2.PNG)

1.  选择图片标签`src=../img/gifts/img1.jpg`;
2.  选择图片标签的父标签（在示例是\<td>标签）；
3.  选择\<td>标签的前一个兄弟标签previous_sibling（在示例中是包含美元价格的\<td>标签）；
4.  选择标签中文字。

### 2.正则表达式

略

### 3. 正则表达式和BeautifulSoup

解决诸如网页结构变化导致爬虫出现问题的方法，就是直接定位那些标签来查找信息。在本例中，我们直接通过商品图片路径来查找：

```python
from urllib.request import urlopen
import re
from bs4 import BeautifulSoup
if __name__ == '__main__':
    html = urlopen("http://www.pythonscraping.com/pages/page3.html")
    bsObj = BeautifulSoup(html)
    imgaes = bsObj.findAll("img", {"src" : re.compile("\.\.\/img\/gifts\/img.*\.jpg")})
    for image in imgaes :
        print(image)
```

正则表达式可以作为BeautifulSoup语句的任意一个参数，让你的目标元素查找工作极具灵活性。

### 4. 获取属性

对于一个标签对象，可以用下面代码获取它的全部属性：`myTag.attrs`。代码返回的是一个Python字典，可以获取和操作这些属性。如获取图片的资源位置src，可以用如下代码：`myImgTag.attrs["src"]`

### 5. Lambda表达式

Lambda表达式本质上就是一个函数，可以作为其它函数的变量使用。

BeautifulSoup允许我们把特定的函数当作findAll函数的参数。唯一的限制条件是这些函数必须把一个标签作为参数且返回结果是布尔类型。	BeautifulSoup用这个函数来评估它遇到的每个标签对象，最后把评估结果为“真”的标签保留，把其它标签剔除。

例如，下面代码就是获取有两个属性的标签：`soup.findAll(lambda tag : len(tag.attrs) == 2)`

在BeautifulSoup里用Lambda表达式选择标签，将是正则表达式的完美替代方案。

### 6. 超越BeautifulSoup

*   [lxml](http://lxml.de/)，可以用来解析HTML和XML文档，以非常底层处理而著名，处理速度快。
*   [HTML parser](https://docs.python.org/3/library/html.parser.html)，Python自带解析库

## 三、开始采集

**网络爬虫(Web crawler)**，即沿着网络爬行，本质是一种递归方式。

谨慎地考虑消耗的网络流量和使采集的目标服务器负载更低一些。

### 3.1 遍历单个域名

```python
from urllib.request import urlopen
import re
from bs4 import BeautifulSoup
##爬取周杰伦百度百科上明星关系包含的明星
if __name__ == '__main__':
    html = urlopen("https://baike.baidu.com/item/%E5%91%A8%E6%9D%B0%E4%BC%A6/129156?fr=aladdin")
    bsObj = BeautifulSoup(html)
    links = bsObj.find("div", {"id":"slider_relations"}).findAll("a", href=re.compile("^http://baike.baidu\.com/subview(/[\\d]+)+\.htm"))
    for link in links:
        div = link.find("div", {"class":"name"})
        if "title" in div.attrs:
            print(div.attrs["title"])
```

这个静态爬取的百度百科词条相关信息的程序很有趣，却没什么实际用处。需要让程序更像下面的形式：

*   一个函数`getLinks()`，可以某个百度百科的URL链接作为参数，然后返回一个列表，里面包含了其它词条的URL链接。
*   一个主函数，以某个起始词条作为参数调用`getLinks()`，再从返回的URL列表里随机选择一个词条链接，再调用`getLinks()`，直到我们主动停止，或者在新的界面上没有了词条链接了，程序才停止。

改进后的代码：

```python
import random
from urllib.request import urlopen
import re
import datetime
from bs4 import BeautifulSoup
def getLinks(url):
    html = urlopen(url)
    bsObj = BeautifulSoup(html)
    #读取明星关系标签组
    labels = bsObj.find("div", {"id":"slider_relations"}).findAll("a", href=re.compile("^http://baike.baidu\.com/subview(/[\\d]+)+\.htm"))
    links = []
    #获取明星关系中的链接
    for label in labels:
        links.append(label.attrs['href'])
    return links
if __name__ == "__main__":
    #获得随机数种子
    random.seed(datetime.datetime.now())
    links = getLinks("http://baike.baidu.com/subview/2632/19244814.htm")
    for i in range(1,6):
        if len(links) > 0:
            newURL = links[random.randint(0, len(links)-1)]
            print(newURL)
            links = getLinks(newURL)

```

利用系统当前时间生成一个随机数生成器，保证程序运行时，选择一个全新的路径。

##### 伪随机数和随机数种子

>   随机数算法在初始阶段都需要提供随机数“种子”（random seed），而完全相同的种子每次将产生同样的“随机”数序列，因此程序选择系统时间作为随机数序列生成的起点，程序运行时更具随机性。
>
>   Python的伪随机数（pseudorandom number）生成器是[梅森旋转算法](https://en.wikipedia.org/wiki/Mersenne_Twister)，它产生的随机数很难预测且呈均匀					分布，缺点是耗费CPU资源。

##### 异常处理

>   代码需要增加异常处理以提升脚本运行的稳固性。

### 3.2采集整个网络

##### 深网和暗网

>   浅网是互联网上搜索引擎可以抓到的那部分网络。	
>
>   深网与浅网对立，诸如提交表单、未链接到顶层域名、有robot.txt禁止而不能查看网站			
>
>   暗网，dark Internet，建立在已有网络之上，使用Tor客户端，带有运行在HTTP之上的新协议，提供了一个信息交换的安全隧道。			

遍历整个网站的网络数据采集有什么作用：	

*   生成网站地图
*   收集数据

一个常用的费时的网站采集方法就是从顶级界面开始（如主页），然后搜索页面上所有链接，形成列表。再去采集这些链接的每一个页面，然后在把每个页面上找到的链接形成新的列表，重复执行下一轮采集。

假设每个页面有10个链接，网站上有5个页面深度，那么采集整个网站就需要采集$$10^{5}$$个页面。虽然“5个页面深度，每页10个链接“是网站的主流配置	，但一般网站很少有那么多页面，大部分内链是重复的。

为避免一个页面被重复采集多次，链接去重是非常重要的。把已发现的所有链接放到一起，并保存在方便查询的列表里。只有新的链接才会被采集，之后再从其页面中搜索其它链接：

```python
from urllib.error import URLError
from urllib.request import urlopen
import re
from bs4 import BeautifulSoup
def getLinks(url):
    global pages
    html = urlopen(url)
    bsObj = BeautifulSoup(html)
    try:
        labels = bsObj.find("div", {"id":"slider_relations"}).findAll("a", href=re.compile("^http://baike.baidu\.com/subview(/[\\d]+)+\.htm"))
        for label in labels:
            if  label.attrs['href'] not in pages:
                newPage = label.attrs['href']
                namePage = label.find("div", {"class":"name"}).attrs['title']
                print(namePage + ":" + newPage)
                pages.add(newPage)
                getLinks(newPage)
    except URLError as e:
        print(e)
    except AttributeError as e :
        print(e)
if __name__ == '__main__':
    pages = set()
    try:
        getLinks("http://baike.baidu.com/subview/2632/19244814.htm")
    except TimeoutError as e :
        print(e)
```

这段代码实现了，以百度百科里面的明星关系为依据，以周杰伦的百度百科作为起始页面，依次爬取其相应的人物百科界面，将其打印在控制台。

##### 关于递归的警告

>   Python默认的递归限制是1000次。设置一个较大的递归计数器，或者其它手段不让其停止。

### 收集整个网站数据

第一步就是先观察网站上的一些页面，然后拟定一个采集模式。

自己后面找个网站，当作小项目来写写

##### 不同的模式应对不同的需求

>   在一个异常处理语句中执行多条语句是不明智的。首先，你无法确定异常被哪行代码抛出。其次，异常会影响网页后面的信息获取。
>
>   通常按照网站上信息出现的可能性高低进行排序是可行，但偶尔会丢失数据，只要作好详细日志的保存就好了。

### 3.3 通过互联网采集

在写爬虫随意跟随外链跳转之前，问自己几个问题：

*   我要手机哪些数据？这些数据可以通过采集几个已经确定的网站完成吗？或者我的爬虫需要发现哪些我可能不知道的网站吗？
*   但我的爬虫到了某个网站，它是立即顺着下一个出站链接跳到一个新网站，还是在网站上待一会，深入采集网站内容？
*   有没有我不想采集的一类网站？
*   如果我的网络爬虫引起了某个网站网管的怀疑，我如何避免法律责任？


    ​		