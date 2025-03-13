# 本地连接池

利用clash配置，实现自动切换并更新ip

ip池站点
https://sch.shanchendaili.com/

## 实现思路
### 拦截流量

方法 1：使用 macOS SystemConfiguration API 修改系统代理（适用于 HTTP 代理）
方法 2：创建 TUN 设备，拦截所有 TCP/UDP 流量（适用于全局代理）
解析 & 处理流量

### 解析 DNS 以确定目标 IP
读取规则（如 GFWList、白名单等）
决定流量是否 直连 还是 走代理
转发流量

### 直连流量直接回放
代理流量通过 SOCKS5 / HTTP 代理服务器转发

## 框架要求

- python >= 3.10
- clash  >= 1.96


## 安装

```bash
pip install -r requirements.txt
```

## 配置

1. 下载：

```shell
git clone https://github.com/alexttg/IP-Switch.git

```

2. 创建运行环境

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
