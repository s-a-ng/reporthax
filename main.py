import sys
import requests, re, time
import threading

action_id = sys.argv[1]
tunnel = sys.argv[2]


def threaded(func):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

def log(message):
    requests.post(tunnel + "/log", {
        "id": action_id,
        "message": message
    })

def start_report(cookie, id):
    url = f'https://www.roblox.com/abusereport/asset?id={id}&redirecturl=%2fcatalog%2f{id}%2funnamed'
    session = requests.Session()
    session.cookies.update({'.ROBLOSECURITY': cookie})
    request_verification_token = re.search('<input name="__RequestVerificationToken" type="hidden" value="(.+)"', session.get(url).text).group(1)
    session.headers.update({
        'Origin': 'https://www.roblox.com',
        'Referer': url,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    })
    while True:
        reason = requests.get(tunnel + "/get_reason").text.decode('ascii')
        report = session.post(url, data={
            '__RequestVerificationToken': request_verification_token,
            'ReportCategory': 9,
            'Comment': reason,
            'Id': id,
            'RedirectUrl': f'https://www.roblox.com/catalog/{id}/unnamed',
            'PartyGuid': '',
            'ConversationGuid': ''
        })
        if report.status_code == 429:
            break
        else:
            print("Reported")
            log("Reported item successfully")
        time.sleep(0.5) 

@threaded
def pinger():
    while True:
        requests.post(tunnel + "/ping", {
            id : action_id
        })
        time.sleep(3)

pinger()
log("connected")
id = 18102169073
ACCOUNTS_TO_USE = 3


for i in range(ACCOUNTS_TO_USE):
    cookie = requests.get(tunnel + "/get_cookie").text.decode('ascii')
    print("got cookie")
    start_report(cookie, id)

requests.post(tunnel + "/done", {
    id : action_id
})
