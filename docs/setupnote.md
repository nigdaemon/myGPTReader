# 部署 myGPTReader 笔记与感想

在 twitter 上看到大伟老师发布的 myGPTReader 应用，第一时间就非常想自己搞一套，这正是我想实现的，但苦于不会编程，没法自己实现。

看过大伟老师的 readme 后，对这个应用充满期待，在 slack 里也体验了一下，感觉非常适合我的需求。于是迫不及待的开始了自己的部署过程。

一般有安装手册的应用，我大多可以按照步骤自己部署好，但这个程序目前还没有部署手册，一开始挺着急，看不懂如何运行的。

后来通过询问 chatGPT，我找到了部署的方法，基本都是通过双向与 GPT 交互实现的。

## 与 chatGPT 的交互过程

我把所有文件内容都发给了 GPT，让它告诉我每个文件的功能和用途。

突破口在 fly.toml 文件，GPT 告诉我它是 fly.io 的配置文件，顺藤摸瓜知道了 fly 应用。

通过 env 里面的环境变量和几个函数，了解到使用了 cloudflare、azure speech、phantomjscloud、fly、slack 等应用。

之后我把每一步的部署都发给 GPT，只要是有日志输出的情况，基本都能通过几次交互找到正确方法。

## 准备工作

1、申请一个新的 openai 账号，获取 OPENAI_API_KEY

2、申请一个新的 slack 频道，创建一个 slack 应用并发布到对应的 slack 频道，获取 SLACK_TOKEN 和 SLACK_SIGNING_SECRET

以上 2 步是最先做了，完成后部署了应用，跑通后再继续完善了后面的服务

3、注册 fly.io 账号，绑定信用卡

4、fork myGPTReader，并 clone 到本地

5、修改必要的配置文件
    -   fly.toml
    -   vip_whitelist.txt 增加自己的 userid
    -   将/data 修改为/tmp ( 主要是因为不知道如何挂在 data )

## 部署过程

### 部署应用 slack

1、安装 flyctl：

2、运行 fly launch，修改配置文件
ps：一步一步配置后，配置文件与 fork 有了区别，我又把配置覆盖回去了

3、flyctl auth login 终端登录到 fly

4、flyctl deploy 部署程序

5、flyctl secrets set OPENAI_API_KEY=...，设置 openai 和 slack 的 3 个 api token

6、flyctl status 查看状态为 started

7、通过 https://fly.io/apps/hostname/monitoring 可以查看后台日志

8、在 fly 的 overview 中，能看到 hostname，这个地址+/slack/events 就是 slack 的服务地址

9、在 slack 中配置上面的服务地址后，再更新下 slack 的 token 的授权范围

10、测试 slack 无响应，在 slack 中尝试不行，之后通过 GPT 提示，卸载了应用重新安装，成功了。即可实现 slack 中@appname 得到回复

到此步，基本验证服务流程跑通。

PS：在测试文章抓取功能时，每次都会报 out of memey，最后把 fly 服务升级了下，提高了运行内存，问题得到解决。

### 其他服务配置

1、语音对话通过 azure speech 实现，需要申请一个账号，并开通 speech 服务，需要绑定银行卡支付，有一年免费

2、页面抓取分两部分，其中 phantomjscloud 比较简单，申请账号后直接获取 token 即可

3、相对有点难度的是 cloudflare 的抓取服务，主要一开始我没找到代码在哪，看大伟老师代码是自己部署的一个服务

4、后来尝试了让 GPT 来反向页面抓取那部分代码，知道了是通过 cloudflare worker 实现的，并让 GPT 给我实现了一个代码

5、实现的代码多次调试后不太理想，最后还是在大伟老师的 github 工程里发现了 web.scraper.workers.dev 工程

6、这个工程有个一键部署，绑定 github 和 cloudflare 可实现自动部署，如果不需要 access 保护，到此就完事了

7、我目前还没把最后的 access 验证做完，主要是域名验证还没完成

## 其他事项

以上应用的的绝大部分应用，除了 github 我都没用过，放到以前让我没有手册情况完成部署，真的难以想象，学习成本巨大。

有了 chatGPT 后，只要知道了具体用的什么服务，通过跟 chatGPT 的交互，完全可以找到正确的部署过程，这个很厉害。

在问 GPT 每一步怎么执行时，我都会问如何验证测试，包括申请到的 api key，都先测试了一下，这样避免后面不好找问题。

而 GPT 真的能很好的给出测试方法，只要丢给他反馈，就算第一次给的方法不对，也能很快纠正。

整个部署过程花了不到 1 天时间，部署了 8 个版本，我自己还是挺兴奋的。以后可以在此基础上持续的完善了。

最后要非常感谢大伟老师：https://twitter.com/madawei2699

![showgif](https://github.com/nigdaemon/myGPTReader/blob/main/docs/myGPTReader.gif)
