import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Gmail:
    GMAIL_SMTP = "smtp.gmail.com"
    GMAIL_IMAP = "imap.gmail.com"

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def send_message(self, *recipients, **kwargs):
        msg = MIMEMultipart()
        msg['From'] = self.login
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = kwargs.get('subject', '')
        msg.attach(MIMEText(kwargs.get('message', '')))
        ms = smtplib.SMTP(GmailEmails.GMAIL_SMTP, 587)
        ms.ehlo()
        ms.starttls()
        ms.ehlo()
        ms.login(self.login, self.password)
        ms.sendmail(self.login, ms, msg.as_string())
        ms.quit()

    def receive(self, header):
        mail = imaplib.IMAP4_SSL(GmailEmails.GMAIL_SMTP)
        mail.login(self.login, self.password)
        mail.list()
        mail.select("inbox")
        criterion = f'(HEADER Subject "{header if header else "ALL"}")'
        result, data = mail.uid('search', None, criterion)
        assert data[0], 'There are no letters with current header'
        latest_email_uid = data[0].split()[-1]
        result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_string(raw_email)
        mail.logout()
        return email_message


if __name__ == '__main__':
    email = Gmail('login@gmail.com', 'qwerty')
    email.send_message('vasya@email.com', 'petya@email.com', message='Message', subject='Subject')
    response = email.receive(None)