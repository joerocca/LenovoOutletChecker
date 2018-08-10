#!/usr/bin/env python

import requests, bs4, smtplib

def fetch_webpage(url):
    headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36"}
    resp = requests.get(url, headers=headers, timeout=5)
    resp.raise_for_status()
    return resp.text

def search_for_laptops(html, laptop_name):
    in_stock_laptops = []
    soup = bs4.BeautifulSoup(html, "html.parser")
    laptop_stock = soup.find_all("div", {"class": "facetedResults-item"})
    
    for laptop in laptop_stock:
        laptop_title = laptop.h3.text.strip()
        if laptop_name in laptop_title:
            stock = laptop.select("span.rci-msg")[0].text.strip().lower()
            if stock != "out of stock":
                buy_link = "https://www.lenovo.com" + laptop.select("a.button-called-out")[0]["href"]
                in_stock_laptops.append(buy_link)
    return in_stock_laptops

def send_email(body):
    from_email = "REPLACE_WITH_EMAIL"
    from_email_pwd = "REPLACE_WITH_PASSWORD"
    to_emails = ["REPLACE_WITH_TO_EMAIL"]
    for to_email in to_emails:
        message = "\r\n".join([f"From: {from_email}", f"To: {to_email}", "Subject: Alert!", "", f"\n{body}"])
        message = message.encode("utf-8")
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.ehlo()
        s.starttls()
        s.login(from_email, from_email_pwd)
        s.sendmail(from_email, to_email, message)
        s.quit()

if __name__ == '__main__':
    laptop_name = "ThinkPad"
    url = "https://www.lenovo.com/us/en/outletus/laptops/c/LAPTOPS?q=%3Aprice-asc%3AfacetSys-Memory%3A16+GB%3AfacetSys-HardDrive%3A512+GB+Solid+State%3AfacetSys-ScreenSize%3A14+in%3AfacetSys-Processor%3AIntel%C2%AE+Core%E2%84%A2+i7%3AfacetSys-Price%3A%24500-%24999.99&uq=&text=#"
    
    html = fetch_webpage(url)
    in_stock_laptops = search_for_laptops(html, laptop_name)
    if len(in_stock_laptops) > 0:
        in_stock_laptop_string = " \n ".join(in_stock_laptops)
        email_body = f"{laptop_name} in stock! \n {in_stock_laptop_string}"
        send_email(email_body)
