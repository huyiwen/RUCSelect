# RUC Select

需要自行安装依赖`pyppeteer`和`ddddocr`，第一次运行时还会安装一个Chrome，但Chrome的依赖项在某些系统下不会自动安装

```
python3 ruc_select.py 学号 一级菜单编号 [二级菜单编号] [学院] --monitor [空格分隔的监控列表]
```

双选：python3 ruc_select.py 2021xxxx 6 1 应用经济学院 --monitor 8
体育课：python3 ruc_select.py 2021xxxxxx 11 --monitor 8 9 10

执行命令后输入微人大密码，自动开始抢课，直到抢课成功一直重试刷新和重新登录。抢课按照monitor先后顺序进行，监控列表为课程最前面的行号（注意获取行号的时候不要筛选课程）。bark作为消息推送通道
