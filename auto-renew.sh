#!/usr/bin/env bash


# https://certbot.eff.org/docs/using.html#manual

# --pre-hook and --post-hook hooks run before and after every renewal attempt.
# If you want your hook to run only after a successful renewal,
# use --deploy-hook in a command like this.

#certbot renew --deploy-hook /path/to/deploy-hook-script


path=$(cd `dirname $0`; pwd)
cd ${path}
# 自动定制执行
echo ------------------
pwd
date
# 自动续期更新所有证书，离过期时间太远就不会去续期，一般离过期时间 还有一个月内 就会续期
./certbot-auto renew  --manual --preferred-challenges dns --manual-auth-hook ${path}/auth.sh --deploy-hook "/usr/bin/systemctl restart nginx"


# 测试更新,
# ./certbot-auto renew  --manual --preferred-challenges dns  --manual-auth-hook /opt/svr/certbot-auth-alidns/auth.sh --deploy-hook "/usr/bin/systemctl restart nginx" --dry-run

# 强制更新
# ./certbot-auto renew  --manual --preferred-challenges dns  --manual-auth-hook /opt/svr/certbot-auth-alidns/auth.sh --deploy-hook "/usr/bin/systemctl restart nginx" --force-renewal


# cron 每天2点执行
# 0 2 * * * /opt/svr/certbot-auth-alidns/auto-renew.sh
