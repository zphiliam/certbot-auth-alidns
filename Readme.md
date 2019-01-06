- 以下假设 clone 路径是在 /opt/svr/下，
即本项目的实际路径是：
```bash
/opt/svr/certbot-auth-alidns/
```
- 本项目 适用 linux 系统
# 执行初始化文件
帮你安装一些依赖库，和初始化本项目的配置文件
```bash
cd certbot-auth-alidns
./init.sh
```

# 配置阿里云 accessKeyId 和 accessSecret
修改 `config.py` 里面对应的值（阿里云控制台中生成的，一定要是拥有这个域名的阿里云）
```python
ACCESS_KEY_ID = 'your accessKeyId'
ACCESS_KEY_SECRET = 'your accessSecret'
```

# 初次申请证书
- 已经申请了的跳过， 直接看更新
- -d 后面参数是 具体的域名，可以是泛域名（通配符），也可以是某个具体域名，
- 如果有多个域名或泛域名。就用多个 -d 参数 -d *.a.com -d *.b.com
- 支持多级域名如 -d *.x.iot-c.top -d *.iot-c.top 

> 以下命令中的 `/opt/svr/certbot-auth-alidns/auth.sh` 为验证服务脚本的实际全路径，你可能要根据你的clone实际路径修改

### 测试申请
- --dry-run 测试的
- 不会真的申请，但会去DNS添加TXT 记录
```bash
./certbot-auto certonly  -d *.iot-c.top  --manual --preferred-challenges dns  --manual-auth-hook /opt/svr/certbot-auth-alidns/auth.sh --dry-run

```

### 实际申请
```bash
./certbot-auto certonly -d *.iot-c.top --manual --preferred-challenges dns  --manual-auth-hook /opt/svr/certbot-auth-alidns/auth.sh
```

# 自动更新
如果要定时执行更新检测，本项目已经提供了执行文件文件 `auto-renew.sh` ,
把他加入到linux 的cron 定时任务中

```bash
crontab -e
```
里面添加一行：
```cron
0 2 * * * /opt/svr/certbot-auth-alidns/auto-renew.sh
```


# 手动更新
- `--manual-auth-hook` 动态验证DNS的脚本服务
- `--deploy-hook` 后面的参数是证书更新成功之后，要指定执行的命令，这里是重启 nginx, 因为nginx不会自动重新加载证书，reload也不会
- 关于生成好的证书如何在 nginx 等容器中的配置，自行百度

### 正常更新
```bash
./certbot-auto renew  --manual --preferred-challenges dns  --manual-auth-hook /opt/svr/certbot-auth-alidns/auth.sh --deploy-hook "/usr/bin/systemctl restart nginx"
```

### 测试更新
--dry-run 是测试执行，不会生成实际证书，也不会执行 --deploy-hook 内容
```bash
./certbot-auto renew  --manual --preferred-challenges dns  --manual-auth-hook /opt/svr/certbot-auth-alidns/auth.sh --deploy-hook "/usr/bin/systemctl restart nginx" --dry-run
```

### 强制更新
```bash
./certbot-auto renew  --manual --preferred-challenges dns  --manual-auth-hook /opt/svr/certbot-auth-alidns/auth.sh --deploy-hook "/usr/bin/systemctl restart nginx" --force-renewal
```



