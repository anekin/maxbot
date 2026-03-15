# yeah.net 邮箱配置完成指南

## 📧 当前配置

| 项目 | 值 |
|------|-----|
| **邮箱地址** | maxbot@yeah.net |
| **SMTP服务器** | smtp.yeah.net |
| **SMTP端口(SSL)** | 465 |
| **SMTP端口(普通)** | 25 |
| **POP服务器** | pop.yeah.net |
| **IMAP服务器** | imap.yeah.net |

---

## ⚠️ 重要：必须使用授权码

网易邮箱（yeah.net）为了安全，要求使用**授权码**而非邮箱密码登录第三方客户端。

### 什么是授权码？
- 授权码是16位字符串
- 用于代替邮箱密码登录邮件客户端
- 可以随时重置

---

## 🔧 获取授权码步骤

### 步骤1: 登录邮箱
1. 访问 https://mail.yeah.net
2. 使用 maxbot@yeah.net 登录

### 步骤2: 进入设置
1. 点击页面顶部的 **设置** 按钮
2. 选择 **POP3/SMTP/IMAP**

### 步骤3: 开启服务
1. 找到 **SMTP服务** 选项
2. 勾选 **开启**
3. 系统会要求验证身份（发送短信验证码）
4. 验证通过后，会显示 **授权码**

### 步骤4: 保存授权码
授权码格式类似：`ABCD1234EFGH5678`

**⚠️ 注意**: 授权码只显示一次，请务必保存好！

---

## 📝 更新服务器配置

获取授权码后，告诉我，我会更新服务器配置：

```bash
# 我会执行这个命令更新授权码
echo "你的授权码" > /home/ubuntu/.openclaw/secrets/email_password.txt
```

---

## ✅ 验证配置

更新授权码后，测试邮件功能：

```bash
# 诊断邮件配置
python3 scripts/send-email.py diagnose

# 发送测试邮件
python3 scripts/send-email.py test "maxbot@yeah.net"
```

---

## 🚀 邮件功能

配置成功后，我可以：

### 1. 每日收盘报告
每天15:00自动发送持仓分析报告

### 2. BS点实时提醒
出现买卖信号时即时邮件通知

### 3. 市场异动预警
大盘异常波动时发送预警

### 4. 周报/月报
定期发送投资组合表现总结

---

## 📊 邮件脚本命令

```bash
# 诊断配置
python3 scripts/send-email.py diagnose

# 发送测试邮件
python3 scripts/send-email.py test "收件人邮箱"

# 发送持仓报告
python3 scripts/send-email.py report "收件人邮箱" "报告文件.md"

# 发送BS点提醒
python3 scripts/send-email.py alert "收件人邮箱" "股票名" "B/S" "价格"

# 检查收件箱
python3 scripts/send-email.py check
```

---

## 🔐 安全说明

- 授权码存储在 `/home/ubuntu/.openclaw/secrets/email_password.txt`
- 文件权限 600（仅所有者可读写）
- 不会记录在日志中
- 仅用于你授权的任务

---

## ❓ 常见问题

### Q: 为什么不能用邮箱密码？
A: 网易邮箱为了安全，第三方客户端必须使用授权码。

### Q: 授权码忘记了怎么办？
A: 登录邮箱网页版，重新生成新的授权码。

### Q: 可以发送到其他邮箱吗？
A: 可以，脚本支持发送到任意邮箱地址。

### Q: 发送失败怎么办？
A: 运行 `python3 scripts/send-email.py diagnose` 查看详细错误信息。

---

## 📞 需要帮助？

如果配置过程中遇到问题，告诉我具体的错误信息，我会帮你解决。

---

*文档由 AnalyzeMaster 创建*  
*最后更新: 2026-03-15*
