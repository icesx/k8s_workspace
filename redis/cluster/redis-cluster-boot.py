# coding:utf-8
# Copyright (C)
# Author: I
# Contact: 12157724@qq.com
import os
from time import sleep

replicas = 3
node_file = "/data/nodes.conf"
data_redis = "/data/redis"
node_ok = "/data/node_ok"


def code(host):
    ip = ""
    while True:
        p = os.popen("nslookup " + host + " 10.96.0.10 |grep Address|grep -v '#53'|awk '{print$2}'")
        result = p.readlines()
        if len(result) == 0:
            print("cannot detect IP for host %s" % host)
            sleep(5)
            continue
        else:
            ip = result[0].replace("\n", "")
            print("detect IP %s,for host %s" % (ip, host))
            break
    return ip


def hosts():
    host_temp = "redis-stateful-{}.redis-stateful-headless"
    __list = range(0, replicas)
    return list(map(lambda i: host_temp.format(i), __list))


def node_hash(host):
    __hash = ""
    while True:
        result = list(os.popen("redis-cli -h " + host + " cluster nodes|grep myself|awk '{print$1}'"))
        if len(result) == 0:
            print("cannot get hash for host", host)
            sleep(5)
            continue
        else:
            __hash = result[0].replace("\n","")
            break
    print("node_hash for host %s is %s" % (host, __hash))
    return __hash


def mk_data_redis():
    if os.path.exists(data_redis) is not True:
        os.mkdir(data_redis)
        print("make dir ", data_redis)


def doit():
    mk_data_redis()
    for host in hosts():
        hash = node_hash(host)
        ip = code(host)
        i = os.system(
            "sed -i -e \"/" + hash + "/ s/[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}/" + ip + "/\" " + node_file)
        print("change nodes.conf result is ", i)
    if os.path.exists(node_ok) is not True:
        open(node_ok,"w")
        print("create node_ok file")
    else:
        print("node_ok is exists")



if __name__ == '__main__':
    doit()
