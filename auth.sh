#!/usr/bin/env bash

path=$(cd `dirname $0`; pwd)

# 调用 python 脚本，自动设置 DNS TXT 记录。
# 第一个参数：需要为那个域名设置 DNS 记录
# 第二个参数：需要为具体那个 RR 设置
# 第三个参数: letsencrypt 动态传递的 value 值

echo $CERTBOT_DOMAIN "_acme-challenge" $CERTBOT_VALIDATION

python  $path"/alidns.py"  $CERTBOT_DOMAIN "_acme-challenge"  $CERTBOT_VALIDATION

# DNS TXT 记录刷新时间
/bin/sleep 5

echo "auth.sh end"
