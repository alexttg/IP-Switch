# 本地连接池

利用clash配置，实现自动切换并更新ip

ip池站点
https://sch.shanchendaili.com/



## 框架要求

- python >= 3.10
- clash  >= 1.96


## 安装

```bash
pip install -r requirements.txt
```

## 配置

1. 创建配置文件：

```shell
git clone https://github.com/alexttg/IP-Switch.git

```

2. 创建环境变量

```shell
python -m venv venv
source venv/bin/activate

```


3. 安装相关包

```shell
pip install -r requirements.txt

```

## 使用

修改`env.yaml` 设置 需要抓取的站点和ip供应商相关key，运行
    
```shell
python app.py

```

将生成` ${server-name}.yaml`  放入clash 对应的配置文件夹中并在客户端选择



## License

MIT