import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

def send_email(subject, message, my_user):
    try:
        my_sender = 'whxlz2020@163.com'
        my_pass = 'cs18031804'
        msg = MIMEText(message, 'plain', 'utf-8')
        msg['From'] = formataddr(["From Server", my_sender])
        msg['To'] = formataddr(["Client", my_user])
        msg['Subject'] = subject

        server = smtplib.SMTP_SSL("smtp.163.com", 465)
        server.login(my_sender, my_pass)
        server.sendmail(my_sender, [my_user, ], msg.as_string())
        server.quit()
        print("---邮件发送成功---")
        return 0, ""
    except Exception as e:
        print(e, "---邮件发送失败---")
        return 1, str(e)