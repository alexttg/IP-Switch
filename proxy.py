import requests
import yaml
import subprocess
import random
import json
import re

with open("env.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)


# https://clash.gitbook.io/doc/restful-api/proxies
# https://github.com/MetaCubeX/mihomo/blob/Alpha/docs/config.yaml

def nslookup(domain):
    try:
        result = subprocess.run(["nslookup", domain], capture_output=True, text=True)
        ips = re.findall(r'Address:\s+([\d\.]+)', result.stdout)
        return ips
    except Exception as e:
        print(f"DNS error: {e}")
        return []


def generate_rules(domain):
    rules = [f"DOMAIN-SUFFIX,{domain},{config['server-name']}"]
    ips = nslookup(domain)
    if ips:
        for ip in ips:
            rules.append(f"IP-CIDR,{ip}/32,{config['server-name']}")

    return rules


def get_ip():
    ip_url = f"{config['ip-pool']['host']}?action=get_ip&key={config['ip-pool']['key']}&time={config['ip-pool']['time']}" \
             f"&count={config['ip-pool']['count']}&type=json&only=0"
    response = requests.get(ip_url)
    data = response.json()
    print(data.get("expire"))
    proxy_list = data.get("list", [])
    print(f"ip到期时间：{data.get('expire')}")
    return proxy_list


def proxy_pool(proxy_list):
    proxies = []
    for i, proxy in enumerate(proxy_list, start=1):
        proxies.append({
            "name": f"Socks5-{proxy.get('sever')}",
            "type": "socks5",
            "server": proxy.get("sever"),
            "port": proxy.get("port"),
            "username": config['ip-pool']['username'],
            "password": config['ip-pool']['password']
        })
    return proxies


def proxy_pool_restock():
    proxy_list = get_ip()
    proxies = proxy_pool(proxy_list)
    return {"proxies": proxies}


def start_run(test_data):
    print("生成clash配置文件")
    clash = config["clash-config"]
    clash["rules"] = generate_rules(config["web-site"])

    proxy_group(clash)

    with open(config["output_path"], "w", encoding="utf-8") as f:
        yaml.dump(clash, f, default_flow_style=False, allow_unicode=True)


def proxy_group(clash):
    clash["proxy-providers"]["dynamic-provider"]["interval"] = config['ip-pool']['time'] * 60
    clash["proxy-groups"][0]["interval"] = config["gap"]
    clash["proxy-groups"][0]["name"] = config["server-name"]


def create_proxy(clash, proxies):
    clash["proxies"] = proxies
    for group in clash["proxy-groups"]:
        group["interval"] = config["gap"]
        group["name"] = config["server-name"]
        group["proxies"] = [p["name"] for p in proxies]


def test_start():
    str_data = "[{'sever': '117.68.38.187', 'port': 32359, 'net_type': 3}, {'sever': '49.84.34.202', 'port': 20614, 'net_type': 2}, {'sever': '58.217.72.237', 'port': 29428, 'net_type': 2}]"
    str_data = str_data.replace("'", '"')
    proxy_list = json.loads(str_data)
    start_run(proxy_list)
