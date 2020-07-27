import easyimap
import pyprowl
import random
import re
import requests
import time


class Bot:
    login = 'your@email.com'
    password = 'yourpassword'
    host = 'yourimaphost'
    port = 993
    read_mails = []
    imapper = None
    accept_language = 'de-DE,de;q=0.5'
    prowl_api_key = '' # let empty for no notifications

    def __init__(self):
        self.s = requests.session()
        self.connect()
        print("[*] Add all emails to read Array")
        for mail_id in self.imapper.listids(limit=100):
            self.read_mails.append(mail_id)
        self.read_emails()

    def connect(self):
        print("[+] (Re-)Connecting to IMAP Server")
        self.imapper = easyimap.connect(self.host, self.login, self.password, "Inbox", True, self.port)

    def read_emails(self):
        print("[*] Reading Emails")
        qassaCnt = euroClixCnt = dondinoCnt = bonusBunnyCnt = questlerCnt = 0
        prowlMsg = ""
        for mail_id in self.imapper.listids(limit=100):
            if mail_id in self.read_mails:
                continue
            self.read_mails.append(mail_id)
            mail = self.imapper.mail(mail_id, include_raw=True)
            if "Qassa" in mail.from_addr:
                print("[+] Found new Mail from Qassa")
                try:
                    url = re.search("(?P<url>https?://www.qassa.de/redirect[^\s]+)", mail.body).group("url")
                    get_real_link_r = self.s.get(url, allow_redirects=True)
                    real_url = re.search("(?P<url>https?://www.qassa.de//mailing[^\s]+)", get_real_link_r.content).group("url")
                    get_coins = self.s.get(real_url, allow_redirects=True)
                    print("[+] Visited Url")
                    qassaCnt += 1
                except:
                    print("[-] No Url found")
            if "EuroClix" in mail.from_addr:
                print("[+] Found new Mail from EuroClix")
                try:
                    url = re.search("(?P<url>https://www.euroclix.de/reference[^\s]+)", mail.body).group("url")
                    visit_link = self.s.get(url, allow_redirects=True)
                    print("[+] Visited link")
                    euroClixCnt += 1
                except:
                    print("[-] No Url found]")
            if "dondino" in mail.from_addr.lower():
                print("[+] Found new Mail from DonDino")
                try:
                    url = re.search("(?P<url>http://www.dondino.de/[^\s]+)", mail.body).group("url")
                    visit_link = self.s.get(url, allow_redirects=True)
                    print("[+] Visited link")
                    dondinoCnt += 1
                except:
                    print("[-] No Url found]")
            if "Bonus Bunny" in mail.from_addr:
                print("[+] Found new Mail from Bonus Bunny")
                try:
                    url = re.search("(?P<url>https://www.bonus-bunny.de/pmail.php[^\s]+)", mail.raw).group("url")
                    url = url.replace("\"", "")
                    visit_link = self.s.get(url, allow_redirects=True)
                    print("[+] Visited link")
                    bonusBunnyCnt += 1
                except:
                    print("[-] No Url found]")
            if "Questler.de" in mail.from_addr:
                print("[+] Found new Mail from Questler")
                try:
                    url = re.search("(?P<url>https://www.questler.de/earn/best.php[^\s]+)", mail.body).group("url")
                    visit_link = self.s.get(url, allow_redirects=True)
                    print("[+] Visited link")
                    questlerCnt += 1
                except:
                    print("[-] No Url found]")
        if (qassaCnt > 0):
            prowlMsg += str(qassaCnt) + " qassa|"
        if (euroClixCnt > 0):
            prowlMsg += str(euroClixCnt) + " EuroClix|"
        if (dondinoCnt > 0):
            prowlMsg += str(dondinoCnt) + " dondino|"
        if (bonusBunnyCnt > 0):
            prowlMsg += str(bonusBunnyCnt) + " Bonus Bunny|"
        if (questlerCnt > 0):
            prowlMsg += str(questlerCnt) + " Questler.de|"

        if (len(prowlMsg) > 0):
            print("[+] Confirmed mails: " + prowlMsg[:-1])
            if (len(self.prowl_api_key) > 0):
                try:
                    p = pyprowl.Prowl(self.prowl_api_key)
                    p.notify(event='Confirmed mails', description=prowlMsg[:-1], priority=0, appName='PaidMailBot')
                    print("[+] Notification successfully sent to Prowl!")
                except Exception as e:
                    print("[-] Error sending notification to Prowl: {}".format(e))
            else:
                print("[*] Skip prowl notification")
        else:
            print("[*] No links were confirmed")
        
        sleep = random.randint(0,3600) + 3600
        print("[*] Sleeping " + time.strftime('%H:%M', time.gmtime(sleep)) + " Hour")
        time.sleep(sleep)
        self.connect()
        self.read_emails()


if __name__ == '__main__':
    bot = Bot()

