#!/usr/bin/env python3
# 邮件发送脚本 - 使用 yeah.net 邮箱
# 支持 POP3/IMAP/SMTP

import smtplib
import imaplib
import poplib
import ssl
import sys
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

# 读取邮箱配置
with open('/home/ubuntu/.openclaw/secrets/email_address.txt', 'r') as f:
    EMAIL = f.read().strip()

with open('/home/ubuntu/.openclaw/secrets/email_password.txt', 'r') as f:
    PASSWORD = f.read().strip()

# yeah.net 服务器配置
SMTP_SERVER = "smtp.yeah.net"
SMTP_PORT = 25  # 尝试25端口（非SSL）
SMTP_PORT_SSL = 465  # SSL端口

POP_SERVER = "pop.yeah.net"
POP_PORT = 110
POP_PORT_SSL = 995

IMAP_SERVER = "imap.yeah.net"
IMAP_PORT = 143
IMAP_PORT_SSL = 993

def test_smtp_connection():
    """测试SMTP连接"""
    print("测试SMTP连接...")
    try:
        # 尝试SSL连接
        print(f"  尝试 {SMTP_SERVER}:{SMTP_PORT_SSL} (SSL)...")
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT_SSL, context=context, timeout=10) as server:
            server.login(EMAIL, PASSWORD)
            print("  ✅ SSL连接成功")
            return "SSL"
    except Exception as e:
        print(f"  ❌ SSL连接失败: {e}")
    
    try:
        # 尝试STARTTLS连接
        print(f"  尝试 {SMTP_SERVER}:{SMTP_PORT} (STARTTLS)...")
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            print("  ✅ STARTTLS连接成功")
            return "STARTTLS"
    except Exception as e:
        print(f"  ❌ STARTTLS连接失败: {e}")
    
    try:
        # 尝试普通连接
        print(f"  尝试 {SMTP_SERVER}:{SMTP_PORT} (普通)...")
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
            server.login(EMAIL, PASSWORD)
            print("  ✅ 普通连接成功")
            return "PLAIN"
    except Exception as e:
        print(f"  ❌ 普通连接失败: {e}")
    
    return None

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
        
        # 尝试多种方式发送
        sent = False
        
        # 方式1: SSL
        if not sent:
            try:
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT_SSL, context=context, timeout=30) as server:
                    server.login(EMAIL, PASSWORD)
                    server.sendmail(EMAIL, to_email, msg.as_string())
                    sent = True
                    print("  使用SSL发送")
            except Exception as e:
                print(f"  SSL发送失败: {e}")
        
        # 方式2: STARTTLS
        if not sent:
            try:
                with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30) as server:
                    server.starttls()
                    server.login(EMAIL, PASSWORD)
                    server.sendmail(EMAIL, to_email, msg.as_string())
                    sent = True
                    print("  使用STARTTLS发送")
            except Exception as e:
                print(f"  STARTTLS发送失败: {e}")
        
        if sent:
            print(f"✅ 邮件发送成功: {to_email}")
            return True
        else:
            print("❌ 所有发送方式都失败")
            return False
        
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
        return False

def send_test_email(to_email):
    """发送测试邮件"""
    subject = "🧪 邮件功能测试"
    body = f"""这是一封测试邮件。

如果您收到这封邮件，说明邮件功能配置成功！

发送时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
发送账号: {EMAIL}

--
AnalyzeMaster
"""
    return send_email(to_email, subject, body)

def send_portfolio_report(to_email, report_file):
    """发送持仓日报"""
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
提醒时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

请登录查看详细分析:
https://github.com/anekin/maxbot

--
AnalyzeMaster
"""
    return send_email(to_email, subject, body)

def check_inbox():
    """检查收件箱"""
    try:
        print("检查收件箱...")
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT_SSL)
        mail.login(EMAIL, PASSWORD)
        mail.select('inbox')
        
        # 搜索未读邮件
        _, search_data = mail.search(None, 'UNSEEN')
        unread_count = len(search_data[0].split())
        
        print(f"  未读邮件: {unread_count} 封")
        
        mail.logout()
        return unread_count
        
    except Exception as e:
        print(f"  检查收件箱失败: {e}")
        return -1

# 主程序
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 send-email.py <命令> [参数]")
        print("")
        print("命令:")
        print("  test <邮箱>              - 发送测试邮件")
        print("  report <邮箱> <报告文件> - 发送持仓报告")
        print("  alert <邮箱> <股票> <信号> <价格> - 发送BS点提醒")
        print("  check                    - 检查收件箱")
        print("  diagnose                 - 诊断邮件配置")
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
    
    elif command == "check":
        check_inbox()
    
    elif command == "diagnose":
        print("=" * 50)
        print("邮件系统诊断")
        print("=" * 50)
        print(f"邮箱地址: {EMAIL}")
        print(f"SMTP服务器: {SMTP_SERVER}")
        print(f"POP服务器: {POP_SERVER}")
        print(f"IMAP服务器: {IMAP_SERVER}")
        print("-" * 50)
        test_smtp_connection()
        print("-" * 50)
        check_inbox()
        print("=" * 50)
    
    else:
        print(f"未知命令: {command}")
        sys.exit(1)
