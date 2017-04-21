#-*- coding:UTF-8 -*-

import os
import json
import shutil
import requests

ssr_dir = os.path.join('D:', os.sep, 'Program', 'ShadowsocksR')
ssr_config_file = os.path.join(ssr_dir, 'gui-config.json')
ssr_config_backup = os.path.join(ssr_dir, 'gui-config.json_bak')

token = '[Input the token from Arukas -> API Keys]'
secret = '[Input the secret from Arukas -> API Keys]'
ss_id = '[Id of Arukas apps which use image: lowid/ss-with-net-speeder]'
ssr_id = '[Id of Arukas apps which use image: malaohu/ssr-with-net-speeder]'

url_prefix = 'https://app.arukas.io/api/'
header = {'content-type': 'application/vnd.api+json'}

arukas_server = []
arukas_port = []


def get_containers(id):
    r = requests.get(url=url_prefix+'containers/'+id, auth=(token,secret), headers=header)
    return r.content


def check_containers(id):
    result = get_containers(id)
    status = json.loads(result)["data"]["attributes"]["is_running"]
    return status


def start_containers(id):
    requests.post(url=url_prefix + 'containers/' + id + '/power', auth=(token, secret), headers=header)


def update_arukas_info(id):
    if check_containers(id):
        origin_info = get_containers(id)
        port_mapping = json.loads(origin_info)["data"]["attributes"]["port_mappings"]
        for i in port_mapping:
            arukas_server.append(i[0]['host'].split('.')[0].replace('seaof-', '').replace('-', '.'))
            arukas_port.append(i[0]['service_port'])
    else:
        start_containers(id)


# 获取最新列表
update_arukas_info(ss_id)
update_arukas_info(ssr_id)


if os.path.exists(ssr_config_file):
    # 备份
    # shutil.copyfile(file, file_bak)

    with open(ssr_config_file,'r') as f:
        j = json.load(f)

    for i in range(len(j['configs'])):
        j['configs'][i]['server'] = arukas_server[i]
        j['configs'][i]['server_port'] = arukas_port[i]

    with open(ssr_config_file, 'w') as f:
        json.dump(j, f, indent=4)
else:
    print "原始文件不存在，请检查。"
