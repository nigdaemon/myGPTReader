
fork 工程：https://github.com/madawei2699/myGPTReader

用chatGPT查看了每一个文件的作用，了解了是用fly部署的

通过查看大伟老师的视频，了解了工程的运作模式和逻辑

通过GPT的询问，知道了如何部署。

### 准备

1、新建一个slack频道，并在slack服务中新建应用，获取两个token

2、在openai注册一个新账号，获取api token

3、注册fly.io账号，绑定信用卡

4、fork myGPTReader，并clone到本地

5、修改必要的配置文件
	- fly.toml
	- .env
	- vip_whitelist.txt 增加自己的userid

### 部署

安装flyctl：
```
brew install flyctl
```

fly launch配置文件
```
fly launch
```

一步一步配置后，配置文件与fork有了区别，我又把配置覆盖回去了

设置远程环境变量
```
flyctl secrets set OPENAI_API_KEY=...
```

部署程序
```
flyctl deploy
```

data挂载点配置没对，gpt提醒后更改了fly.toml配置，重新执行depoly

部署成功
```
Machine **39080553cd7087 [app]** update finished: success

Finished deploying
```


### 设置slack

配置：Event Subscriptions

配置：request URL

在### Subscribe to bot events中，选择 "Add Bot User Event"，把需要监控的事件添加好

通过向GPT询问，获知监听的端点地址：https://mychatreader.fly.dev/slack/events

填写到slack后，判断为无响应

查看服务器状态
```
flyctl status
```

查看机器没有启动，通过询问GPT，获取启动命令：

```
flyctl machine start xxx

```

通过查看日志，并将日志内容给GPT，知道了是procfile中配置错误：
```
flyctl logs -a appname
```


修改procfile文件，该错误是在初始化时，程序自动生成的，缺少了路径：
```
web: gunicorn app.server:app
```

修改配置后，重新部署 deploy

重新部署后报错，发现时/data目录权限不对，暂时修改为tmp目录，并重新部署

此次部署后，运行成功，在event中也可以verified

在slack中尝试不行，之后通过GPT提示，卸载了应用重新安装，成功了

![DlUVAx](https://raw.githubusercontent.com/nigdaemon/oss/master/uPic/DlUVAx.png)

感谢大伟老师：https://twitter.com/madawei2699