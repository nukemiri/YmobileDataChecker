#! /usr/bin/env python
# -*- coding: utf-8 -*-


import requests
from bs4 import BeautifulSoup
import pickle
import cgi
import cgitb
# cgitb.enable()
import os


def main():

    form = cgi.FieldStorage()
    if "telnum"in form:
        telnum = form["telnum"].value

    if "varinum" in form:
        varinum = form["varinum"].value
        with open(f'../dump/{telnum}_session.dump', 'rb') as f:
            s = pickle.load(f)

        os.remove(f'../dump/{telnum}_session.dump')
        soup = BeautifulSoup(r.text, 'html.parser')
        
        ticket = soup.find('input', attrs={'name': 'ticket', 'type': 'hidden'})["value"]
        params={
            "tel":str(telnum),
            "password":varinum,
            "ticket":ticket
        }
        r = s.post("https://id.my.ymobile.jp/sbid_auth/type1/2.0/r_login_otp.php",data=params)

    else:
        s = requests.Session()

        # クッキーのロード
        try:
            with open(f'../dump/{telnum}_cookie.dump', 'rb') as f:
                c = pickle.load(f)
                s.cookies.update(c)
        except:
            pass

        r = s.get("https://my.ymobile.jp/muc/d/top?s=4e2mV")
        soup = BeautifulSoup(r.text, 'html.parser')

        if soup.find("title").text=="ログイン | ワイモバイル":
            if "password" in form:
                password = form["password"].value
            ticket = soup.find('input', attrs={'name': 'ticket', 'type': 'hidden'})["value"]
            params = {
                'ticket': ticket,
                "telnum": telnum,
                "password":password}
            r = s.post("https://id.my.ymobile.jp/sbid_auth/type1/2.0/login.php",data=params)
            soup = BeautifulSoup(r.text, 'html.parser')

        if soup.find("title").text=="本人確認 | My SoftBank | ソフトバンク":
            print ('Content-type: text/html; charset=UTF-8')
            print ("\r\n\r\n")
            print(f"""
                <html>
        <head><meta charset="utf-8" /></head>
            <form action="" method="POST">
                <input type="hidden" name="telnum" value="{telnum}" />
                {telnum}に届いた確認番号を入力
                <input type="text" name="varinum">
                <input type="submit" name="submit" value="送信">
            </form>
        </body>
        </html>
            """)
            with open(f'../dump/{telnum}_session.dump', 'wb') as f:
                pickle.dump(s, f)
            return
    # クッキーのセーブ
    with open(f'../dump/{telnum}_cookie.dump', 'wb') as f:
        pickle.dump(s.cookies, f)
    
    soup = BeautifulSoup(r.text, 'html.parser')
    data=soup.find("span", attrs={'class': 'fs-28'})
    print ('Content-type: text/html; charset=UTF-8')
    print ("\r\n\r\n")
    print(f"{data.text}GB")
    return data.text

main()
