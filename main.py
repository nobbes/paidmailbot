import easyimap
import re
import requests
import time


class Bot:
    login = 'your@email.com'
    password = 'yourpassword'
    read_mails = []
    imapper = None
    accept_language = 'de-DE,de;q=0.5'

    def __init__(self):
        self.s = requests.session()
        self.connect()
        print("[*]Add all emails to read Array")
        for mail_id in self.imapper.listids(limit=100):
            self.read_mails.append(mail_id)
        self.read_emails()

    def connect(self):
        print("[+](Re-)Connecting to IMAP Server")
        self.imapper = easyimap.connect('mail.yourmailserver.com', self.login, self.password)

    def read_emails(self):
        print("[*]Reading Emails")
        for mail_id in self.imapper.listids(limit=100):
            if mail_id in self.read_mails:
                continue
            self.read_mails.append(mail_id)
            mail = self.imapper.mail(mail_id, include_raw=True)
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
            if "dondino" in mail.from_addr.lower():
                print("[+]Found new Mail from DonDino")
                try:
                    url = re.search("(?P<url>http://www.dondino.de/[^\s]+)", mail.body).group("url")
                    visit_link = self.s.get(url, allow_redirects=True)
                    print("[+]Visited link")
                except:
                    print("[-]No Url found]")
            if "Bonus Bunny" in mail.from_addr:
                print("[+]Found new Mail from Bonus Bunny")
                try:
                    url = re.search("(?P<url>https://www.bonus-bunny.de/pmail.php[^\s]+)", mail.raw).group("url")
                    url = url.replace("\"", "")
                    visit_link = self.s.get(url, allow_redirects=True)
                    print("[+]Visited link")
                except:
                    print("[-]No Url found]")
            if "Questler.de" in mail.from_addr:
                print("[+]Found new Mail from Questler")
                try:
                    url = re.search("(?P<url>https://www.questler.de/earn/best.php[^\s]+)", mail.body).group("url")
                    visit_link = self.s.get(url, allow_redirects=True)
                    print("[+]Visited link")
                except:
                    print("[-]No Url found]")
        print("[*]Sleeping 1 Hour")
        time.sleep(3600)
        self.connect()
        self.read_emails()


if __name__ == '__main__':
    bot = Bot()

