#!/usr/bin/env bash
# clone 本项目后首次执行 此文件

#安装依赖的aliyun python sdk：
pip install aliyun-python-sdk-core

# 安装 certbot-auto 入口文件，如果之前在其他某个位置
# 安装过 certbot-auto ，并不会冲突，
# 启动后会检查依赖库已安装就不会重新安装，放心执行
cd certbot-auth-alidns
wget https://dl.eff.org/certbot-auto
chmod a+x certbot-auto
./certbot-auto --help


# 初始化配置文件

# -f 参数判断 $file 是否存在
# config.py 文件不存在就初始化一个
if [ ! -f "./config.py" ]; then
    cp ./_config.py ./config.py
fi
