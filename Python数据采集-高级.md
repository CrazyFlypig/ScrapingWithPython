# Python数据采集-高级

## 四、使用API

引用编程接口（Application Programming Interface，API）用处：为不同的应用提供方便友好的接口。

一般情况下，程序员可以用HTTP协议向API发出请求以获取某种信息，API会用 XML（可标记扩展语言）或 JSON（JavaScript Object Notation）格式返回服务器响应的信息。

### 4.1 API概述

### 4.2 API通用规则

#### 4.2.1 方法

利用 HTTP 从网络服务获取信息有四种方式：

*   GET
*   POST
*   PUT
*   DELETE

PUT请求用来更新一个对象或信息。

DELETE用于删除一个对象。

#### 4.2.2 验证

通常 API 验证的方法都是用类似于令牌（token）的方式调用，每次 API 调用都会把令牌传递到服务器上。

令牌除了在URL链接中传递，还会通过请求头里的 cookie 把用户信息传递给服务器。

### 4.3 服务器响应

#### API调用

当使用 GET 请求获取数据时，用 URL 路径描述你要获取的数据范围，查询参数可以作为过滤器或附加请求使用。

### 4.4 Google API

