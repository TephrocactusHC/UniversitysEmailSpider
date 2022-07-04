# NKUSpider
**南开大学各学院教师邮箱的爬虫练习.**<br>

每个学院上传的文件包括程序(.py)和爬取结果(.txt/.csv/...)两项内容。

主要受到前人启发，[这是前人的连接](https://github.com/lvwuwei/NKU-spider)，打算自己也爬一下教师邮箱练练手。正好各学院主页基本上都更新了，为了防止爬虫基本都采用了动态渲染的方式，
学长写的程序也基本上都不能运行了，因此更新一下。

2022.6.28<br>
首次更新了马克斯学院的代码和爬取结果。

2022.6.29<br>
更新了计网、外院、哲学院的代码和爬取结果。
其中哲学院由于官网没有变化，故直接用的前人成果，只对编码添加了两个语句。计网的官网一样，故只爬取了计院的官网。外院的动态渲染也较为简单，并不复杂。


2022.7.2<br>
新增法学、文学、医学、药学、历史、数学、化学学院的成果。大多数不难，直接套用前人成果，稍微分析一下网页即可。

2022.7.3<br>
新增电光、软件学院、汉语言文学、旅游、环境科学、商学院、材料科学学院、经济学院的成果。除了商学院都是在分析网页的基础上，套用前人成果。
商学院的网页比较特殊，大部分网页重定向到旧版商学院官网，旧版商学院官网是内网，所以会有反爬机制，如果用requests会发生重定向错误，用selenium完美解决问题。
以材料和商院为代表的前端定向的很乱，所以加了判定。<br>
新增人工智能学院，这学院为了反爬也是把前端写的很烂很碎，所以很难进行准确的、完整的爬虫。AI.py程序95%的邮箱都是对的，但还是有几个老师的界面爬下来的有问题。不过反正是玩具程序，就不改了。<br>

增加统计学院。这个学院从培养计划到科研方向到任课教师到官网主页，我都特别喜欢，真是好地方。<br>

增加周政学院。在周政匹配邮箱的过程中，发现前人写的正则表达式有个问题，(AT)无法成功替换成@，暂时不知道为什么。那在周政之前的邮箱爬取可能都是不完全的，但是无伤大雅，把我在周政里改的语句加上即可。网上有一个流传很广的正则表达式，理论上可以匹配任何格式的邮箱，但是考虑到有的学院前端写的很混乱，可能并不适用。有兴趣的可以去网上查查那种万能的正则。<br>

能套用到基本上都在这里了，之前人写的那个程序的主体框架还是不错的，很适合套用在类似场合。过几天不忙了主要解决生科院为代表的界面，需要用到js逆向的方法。

2022.7.4<br>
新增物理学院，生命科学学院。物理学院的爬取应该是和生科院类似的，较为简单的办法是通过selenium模拟浏览器然后获取链接再进去爬取。
当然，物理学院有好多老师的信息不全，所以结果并不完整。<br>
生命科学学院我也采取了selenium的方法，JS逆向的方法以后可能会考虑更新，不过在小样本量爬取的情况下，selenium已经足够强大了。<br>

最后更新一波金融学院。由于是表格，故直接爬取，难度很低。<br>

#### 至此，NKU的已经完结了。<br>

**后续可能会更新TJU或者其他学校的，看情况。**
