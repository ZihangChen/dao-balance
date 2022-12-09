from web3 import Web3
import toml

import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr


def get_config(config_file):
    return toml.load(config_file)


def check_wallet_balance(web3, wallets, threshold):
    sufficient_amount = True
    balances = []
    for wallet in wallets:
        balance = web3.eth.getBalance(wallets[wallet])*1e-18
        if balance < threshold:
            sufficient_amount = False
            balances.append((wallets[wallet], balance))
    return sufficient_amount, balances


def notification_email(mail_info, receiver, msg):
    message = MIMEText(msg, 'plain', 'utf-8')
    message['From'] = formataddr(('Friendly DAO Wallet Balance Reminder', mail_info['account']))
    message['To'] = mail_info['account']
    message['Subject'] = Header('DAO signature wallet balance insufficient!!!!', 'utf-8')
    with smtplib.SMTP(mail_info['host'], mail_info['port']) as server:
        server.starttls()
        server.ehlo()
        server.login(mail_info['account'], mail_info['password'])
        server.sendmail(mail_info['account'], list(receiver.values()), message.as_string())
    return 'email sent'


def run_scan():
    conf = get_config('config.toml')
    web3 = Web3(Web3.HTTPProvider(conf['rpc_endpoint']))

    if not web3.isConnected():
        notification_email(conf['email'], 'rpc connection failed!')
        return 'RPC connection error'
    
    message = ''
    sufficient, balances = check_wallet_balance(web3, conf['signature'], conf['threshold'])
    if sufficient:
        return 'All wallet balance a sufficient'
    for info in balances:
        message += 'Wallet {} has insufficient balance, remaining balance: {}. \n'.format(info[0], info[1])
    notification_email(conf['email'], conf['email_receiver'], message)
    return 'error: \n' + message
    
    