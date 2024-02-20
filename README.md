# RUC Select

## Installation

需要自行安装依赖`pyppeteer`和`ddddocr`，第一次运行时还会安装一个Chrome，但Chrome的依赖项在某些系统下不会自动安装

## Usage

```
python3 ruc_select.py 学号 一级菜单编号 [二级菜单编号] [学院] --monitor [空格分隔的监控列表]
```

- 双选：`python3 ruc_select.py 20xxxxxx 6 1 应用经济学院 --monitor 8`
- 体育课：`python3 ruc_select.py 20xxxxxxxx 11 --monitor 8 9 10`（省略二级菜单编号和学院）

执行命令后输入微人大密码，自动开始抢课，直到抢课成功一直重试刷新和重新登录。抢课按照monitor先后顺序进行，监控列表为课程最前面的行号（注意获取行号的时候不要筛选课程）。[bark（仅支持iOS）](https://apps.apple.com/us/app/bark-customed-notifications/id1403753865)作为消息推送通道，在bark app中创建一个key填入即可

<img width="1040" alt="image" src="https://github.com/huyiwen/RUCSelect/assets/5737212/251c3250-2eb4-441c-b6fb-6e09f35cbc9e">

## Buy me a coffee

<img width="300" alt="image" src=https://github.com/huyiwen/RUCSelect/assets/5737212/cc48ba3d-a386-45a8-8c5a-9aae96a9b198>
