import smtplib
import ssl

smtp_server = 'smtp.gmail.com'
port = 587
sender = 'django.gastronom@gmail.com'
password = 'ok2392er'
context = ssl.create_default_context()


def send_email(recipient_email, message):
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls(context=context)

        server.login(sender, password)
        server.sendmail(sender, recipient_email, message)
    except Exception as exep:
        print(exep)
    finally:
        server.quit()
