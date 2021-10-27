## GameOfGO
### 概要

 基于《深度学习与围棋》一书，记录学习历程（初衷）

目前用于大四计算机系统课程设计，项目所需环境参考requirements.txt

### 启动

**在main中启动**

安装好所需要的配置之后直接运行以下文件即可启动

end_to_end.py实现了基于深度学习的围棋AI，在本地127.0.0.1:5000/static/play_predict_19.html实现对局；

bot_v_bot.py实现了命令行的机器对机器；

human_v_bot.py实现了命令行的人机对战；

human_v_betago.py部署了一个成熟的围棋AI betago，在本地127.0.0.1:5000/static/play_predict_19.html实现对局

human_v_human.py是基于tkinter的客户端人人对战

### 训练

**网络调整**

通过修改networks文件夹中的large.py即可修改神经网络

**特征参数调整**

通过修改end_to_end.py第23行的num_samples参数大小即可修改加载特征的数量，通过processor.py第117行的chunksize即可修改生成特征的基础要求数量

**别的调整**

同理，processor.py的采样器也可以进行修改；可以参考原书稍作修改写一个并行的processor等等

**学习方法**

后续可以加入强化学习和对抗学习，具体如何实现参照原书

### 使用的黑盒代码

按照文件夹依次说明

```python
agents
	betago.hdf5 # 训练好的机器人
dlgo
	data
    	index_processor.py # u-go网站爬虫代码
        sampling.py # 特征采样器代码
    encoders
    	betago.py # betago的特征提取器
    gosgf全部 # 爬虫爬取的sgf文件转换器
    httpfrontend
    	server.py # flask前端启动器
        static中的前端代码 # flask围棋前端
```

### 其他

有问题请联系我mail： yxhop666@gmail.com
