# -*- coding: utf-8 -*-
import smtplib
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
from utils import db_execute
import conf


def prepare_body(accounts_info, sender_name):
    """Returns message body in text and html format.

    Structure of accounts_info
    >>> accounts_info = [{
    >>>     'code': 'OTA.TCH',
    >>>     'remaining_tickets': 985,
    >>>     'remaining_emds': 400,
    >>>     'datetime': '2018-06-23 19:26:16 (MSK)',
    >>>     'alert': False,
    >>> }]

    :param accounts_info: list, accounts info, see above description of element structure.
    :param sender_name: str, name of sender used in signature.
    :return: tuple of two strings, (body_text, body_html)
    :rtype: tuple
    """
    status_msg = ''
    alert_accounts = list()
    for account in accounts_info:
        tickets = '¯\_(ツ)_/¯' if account['remaining_tickets'] is None else account['remaining_tickets']
        emds = '¯\_(ツ)_/¯' if account['remaining_emds'] is None else account['remaining_emds']
        if account['alert']:
            alert_accounts.append(account['code'])
        status_msg += '{account}: {tickets} билетов, {emds} EMD, проверено {dt}\r\n'\
            .format(account=account['code'], tickets=tickets, emds=emds, dt=account['datetime'])
    alert_msg = ''
    if len(alert_accounts):
        alert_msg = 'Срочно запросите квоту для: ' + ', '.join(alert_accounts) + '!\r\n\r\n'
    body_text = (
        'Приветствую\r\n\r\n'
        '{alert}'
        'Состояние стоков:\r\n{status_msg}'
        '\r\n\r\n'
        '--\r\n'
        'Дружески,\r\n'
        '{sender}'
    )
    body_html = (
        '<html>'
        '<head></head>'
        '<body>'
        '<p>Приветствую</p>'
        '{alert}'
        '<p>Состояние стоков<br />{status_msg}</p>'
        '<p>'
        '<br /><br />'
        '--<br />'
        'Дружески,<br />'
        '{sender}'
        '</p>'
        '</body>'
        '</html>'
    )
    return (
        body_text.format(alert=alert_msg, status_msg=status_msg, sender=sender_name),
        body_html.format(alert=alert_msg, status_msg=status_msg.replace('\r\n', '<br />'), sender=sender_name)
    )


def send_mail(sender, recipient, subject, body, smtp_user, smtp_password,
              smtp_gateway='email-smtp.eu-west-1.amazonaws.com', smtp_port=587):
    """Sends mail via SMTP server.

    :param sender: tuple of two strings, ('Sender Name', 'sender@email.com')
    :param recipient: str, recipient email, e.g. 'recipient@email.com'
    :param subject: str, email subject
    :param body: tuple of two strings, (body_text, body_html)
    :param smtp_gateway: str, smtp server endpoint
    :param smtp_port: int, smtp server port
    :param smtp_user: str, login of smtp user
    :param smtp_password: str, password of smtp user
    """
    # At AWS side Verification Check is case-sensitive - WTF?!
    recipient = recipient.lower()

    body_text, body_html = body
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = email.utils.formataddr(sender)
    msg['To'] = recipient
    msg.attach(MIMEText(body_text, 'plain'))
    msg.attach(MIMEText(body_html, 'html'))
    server = smtplib.SMTP(smtp_gateway, smtp_port)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(smtp_user, smtp_password)
    server.sendmail(sender[1], recipient, msg.as_string())
    server.close()


if __name__ == '__main__':
    rows = db_execute(
        conf.db_name,
        'SELECT account, remaining_tickets, remaining_emds, created_at'
        ' FROM quota_check'
        ' GROUP BY account HAVING MAX(created_at)'
    )
    info_items = list()
    alert = False
    for row in rows:
        if row[0] not in conf.accounts:
            continue  # unknown account code
        info_items.append({
            'code': row[0],
            'remaining_tickets': row[1],
            'remaining_emds': row[2],
            'datetime': time.strftime('%Y-%m-%d %H:%M:%S (%Z)', time.localtime(row[3])),
            'alert': (row[1] or 0) < conf.accounts[row[0]].get('alert', 0),
        })
        alert = info_items[-1]['alert'] or alert
    message_body = prepare_body(info_items, conf.sender[0])
    send_mail(conf.sender, conf.recipient_info, 'Состояние стоков',
              message_body, conf.smtp_user, conf.smtp_password)
    if alert:
        send_mail(conf.sender, conf.recipient_alert, 'Срочно пополните сток',
                  message_body, conf.smtp_user, conf.smtp_password)
