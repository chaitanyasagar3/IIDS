# python script to send email
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib
from os.path import basename

def emailsend(email, subject, mes, fi):
    from_email = "sagarchinu123@gmail.com"
    from_password = "Anjana#1998"
    to_email = email

    subject = subject
    message = mes

    msg = MIMEMultipart()

    msg['Subject'] = subject
    msg['To'] = to_email
    msg['From'] = from_email
    msg.attach(MIMEText(message,'html'))
    if fi != "no":
        with open(fi,'rb') as fil:
            part = MIMEApplication(fil.read(),Name=basename(fi))
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(fi)
            msg.attach(part)

    gmail = smtplib.SMTP('smtp.gmail.com',587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)
    gmail.send_message(msg)
