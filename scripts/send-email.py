#!/bin/bash
# 邮件发送脚本 - 使用Python实现
# 使用 yeah.net 邮箱

import smtplib
import ssl
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

# 读取邮箱配置
with open('/home/ubuntu/.openclaw/secrets/email_address.txt', 'r') as f:
    EMAIL = f.read().strip()

with open('/home/ubuntu/.openclaw/secrets/email_password.txt', 'r') as f:
    PASSWORD = f.read().strip()

# yeah.net SMTP配置
SMTP_SERVER = "smtp.yeah.net"
SMTP_PORT = 465  # SSL端口

def send_email(to_email, subject, body, attachment=None):
    """发送邮件"""
    try:
        # 创建邮件
        msg = MIMEMultipart()
        msg['From'] = EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # 添加正文
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        # 添加附件
        if attachment and os.path.exists(attachment):
            with open(attachment, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {os.path.basename(attachment)}'
                )
                msg.attach(part)
        
        # 连接SMTP服务器并发送
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, to_email, msg.as_string())
        
        print(f"✅ 邮件发送成功: {to_email}")
        return True
        
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
        return False

def send_test_email(to_email):
    """发送测试邮件"""
    subject = "🧪 邮件功能测试"
    body = f"""这是一封测试邮件。

如果您收到这封邮件，说明邮件功能配置成功！

发送时间: {os.popen('date').read().strip()}
发送账号: {EMAIL}

--
AnalyzeMaster
"""
    return send_email(to_email, subject, body)

def send_portfolio_report(to_email, report_file):
    """发送持仓日报"""
    from datetime import datetime
    date = datetime.now().strftime('%Y-%m-%d')
    
    subject = f"📊 持仓日报 - {date}"
    body = f"""您好！

附件是今日持仓分析报告，请查收。

报告时间: {date}
发送时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

--
AnalyzeMaster
"""
    return send_email(to_email, subject, body, report_file)

def send_bs_alert(to_email, stock_name, signal, price):
    """发送BS点提醒"""
    if signal == "B":
        emoji = "🟢"
        action = "买入信号"
    elif signal == "S":
        emoji = "🔴"
        action = "卖出信号"
    else:
        emoji = "🟡"
        action = "观望"
    
    subject = f"{emoji} BS点提醒 - {stock_name}"
    body = f"""检测到 {stock_name} 出现{action}

当前价格: {price}
信号类型: {signal}
提醒时间: {os.popen('date').read().strip()}

请登录查看详细分析:
https://github.com/anekin/maxbot

--
AnalyzeMaster
"""
    return send_email(to_email, subject, body)

# 主程序
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 send-email.py <命令> [参数]")
        print("")
        print("命令:")
        print("  test <邮箱>              - 发送测试邮件")
        print("  report <邮箱> <报告文件> - 发送持仓报告")
        print("  alert <邮箱> <股票> <信号> <价格> - 发送BS点提醒")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "test":
        if len(sys.argv) < 3:
            print("请提供收件人邮箱")
            sys.exit(1)
        send_test_email(sys.argv[2])
    
    elif command == "report":
        if len(sys.argv) < 4:
            print("请提供收件人邮箱和报告文件路径")
            sys.exit(1)
        send_portfolio_report(sys.argv[2], sys.argv[3])
    
    elif command == "alert":
        if len(sys.argv) < 6:
            print("请提供: 邮箱 股票名 信号 价格")
            sys.exit(1)
        send_bs_alert(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    
    else:
        print(f"未知命令: {command}")
        sys.exit(1)
