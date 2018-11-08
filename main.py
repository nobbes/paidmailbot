import easyimap
import re
import requests
from fake_useragent import UserAgent
import time


class Bot:
    login = 'your_email@provider.com'
    password = 'your_password'
    read_mails = []
    imapper = None
    user_agent = "" ""
    accept_language = 'de-DE,de;q=0.5'

    def __init__(self):
        fake_ua = UserAgent()
        self.user_agent = str(fake_ua.random)
        self.s = requests.session()
        self.connect()
        print("[*]Add all emails to read Array")
        for mail_id in self.imapper.listids(limit=100):
            self.read_mails.append(mail_id)
        self.read_emails()

    def connect(self):
        print("[+](Re-)Connecting to IMAP Server")
        self.imapper = easyimap.connect('imap.your_server.com', self.login, self.password)

    def read_emails(self):
        print("[*]Reading Emails")
        for mail_id in self.imapper.listids(limit=100):
            if mail_id in self.read_mails:
                continue
            self.read_mails.append(mail_id)
            mail = self.imapper.mail(mail_id)
            if "Qassa" in mail.from_addr:
                print("[+]Found new Mail from Qassa")
                try:
                    url = re.search("(?P<url>https?://www.qassa.de/redirect[^\s]+)", mail.body).group("url")
                    get_real_link_r = self.s.get(url, allow_redirects=True)
                    real_url = re.search("(?P<url>https?://www.qassa.de//mailing[^\s]+)", get_real_link_r.content).group("url")
                    get_coins = self.s.get(real_url, allow_redirects=True)
                    print("[+]Visited Url")
                except:
                    print("[-]No Url found")
            if "EuroClix" in mail.from_addr:
                print("[+]Found new Mail from EuroClix")
                try:
                    url = re.search("(?P<url>https://www.euroclix.de/reference[^\s]+)", mail.body).group("url")
                    visit_link = self.s.get(url, allow_redirects=True)
                    print("[+]Visited link")
                except:
                    print("[-]No Url found]")
        print("[*]Sleeping 1 Hour")
        time.sleep(3600)
        self.connect()
        self.read_emails()


def main():
    bot = Bot()


if __name__ == '__main__':
    main()
