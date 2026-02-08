# FbCreator_Unblock.py
# 100% Unblock + High Success
# প্রক্সি + ডিলে + রিয়েল UA

import requests, random, json, time, re
from faker import Faker
fake = Faker()

print("\nFbCreator 2025 - UNBLOCK MODE\n")

# ========== প্রক্সি লোড কর (ফ্রি) ==========
def load_free_proxies():
    try:
        url = "https://api.proxyscrape.com/v2/?request=get&protocol=http&timeout=10000&country=all&ssl=yes&anonymity=elite"
        proxies = requests.get(url, timeout=15).text.strip().split("\n")
        random.shuffle(proxies)
        return [p for p in proxies if ":" in p][:20]
    except:
        print("[-] Proxy API down!")
        return []

proxies = load_free_proxies()
if not proxies:
    print("[-] No proxy! Using delay...")
    proxies = [None]  # fallback

def get_real_ua():
    uas = [
        "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
    ]
    return random.choice(uas)

def get_temp_mail():
    try:
        domains = requests.get("https://api.mail.tm/domains", timeout=10).json()['hydra:member']
        domain = random.choice(domains)['domain']
        username = fake.user_name()[:8] + str(random.randint(100,999))
        email = f"{username}@{domain}"
        password = fake.password(12)
        requests.post("https://api.mail.tm/accounts", json={"address": email, "password": password}, timeout=10)
        print(f"[+] Email: {email}")
        return email, password
    except:
        print("[-] Mail.tm down!")
        return None, None

def register_with_proxy(email, password, first_name, last_name, birthday, proxy=None):
    session = requests.Session()
    if proxy:
        session.proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    
    headers = {
        "User-Agent": get_real_ua(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    session.headers.update(headers)
    
    try:
        r = session.get("https://m.facebook.com/reg/", timeout=15)
        if "name=\"lsd\"" not in r.text:
            return False
        
        lsd = re.search('name="lsd" value="([^"]+)"', r.text).group(1)
        jazoest = re.search('name="jazoest" value="([^"]+)"', r.text).group(1)
        
        day, month, year = birthday.day, birthday.month, birthday.year
        
        data = {
            "lsd": lsd,
            "jazoest": jazoest,
            "firstname": first_name,
            "lastname": last_name,
            "reg_email__": email,
            "reg_passwd__": password,
            "birthday_day": str(day),
            "birthday_month": str(month),
            "birthday_year": str(year),
            "sex": "2",
            "submit": "Sign Up"
        }
        
        r2 = session.post("https://m.facebook.com/reg/", data=data, allow_redirects=False, timeout=15)
        
        if r2.status_code in [301, 302]:
            loc = r2.headers.get("Location", "")
            if "confirmemail" in loc or "checkpoint" in loc:
                info = {
                    "email": email, "mail_password": mail_pass, "fb_password": password,
                    "name": f"{first_name} {last_name}", "birthday": f"{year}-{month:02d}-{day:02d}",
                    "proxy_used": proxy or "None"
                }
                with open("account_info.txt", "w") as f:
                    json.dump(info, f, indent=2)
                print(f"\nACCOUNT CREATED! Proxy: {proxy or 'Local'}")
                print(f"Check: https://mail.tm")
                return True
        return False
    except:
        return False

# ============= MAIN =============
email, mail_pass = get_temp_mail()
if not email:
    exit()

first_name = fake.first_name()
last_name = fake.last_name()
password = ''.join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=12))
birthday = fake.date_between(start_date='-35y', end_date='-21y')

print(f"[+] Name: {first_name} {last_name}")
print(f"[+] DOB: {birthday.strftime('%Y-%m-%d')}")
print(f"[+] Password: {password}")

# Try with each proxy
for proxy in proxies:
    print(f"\n[Try] Proxy: {proxy or 'Local IP'}")
    if register_with_proxy(email, password, first_name, last_name, birthday, proxy):
        print("\nMANUALLY VERIFY EMAIL NOW!")
        break
    else:
        print("Failed... trying next proxy...")
        time.sleep(random.randint(15, 30))
else:
    print("\nAll failed. Try 4G or later.")
