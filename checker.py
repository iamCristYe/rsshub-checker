# https://github.com/RSSNext/rsshub-docs/raw/refs/heads/main/.vitepress/theme/components/InstanceList.vue

import requests

response = requests.get(
    "https://raw.githubusercontent.com/RSSNext/rsshub-docs/main/.vitepress/theme/components/InstanceList.vue"
)
print(response.text)
# The above code fetches the content of the specified URL and prints it to the console.
# You can further process the content as needed.
# This script is intended to be run in an environment where the 'requests' library is available.
# Make sure to install the requests library if you haven't already:
# pip install requests
# The content fetched is the source code of a Vue.js component used in the RSSHub documentation site.

line_count = len(response.text.splitlines())
print(f"The fetched file has {line_count} lines.")

instance_list = []
for line in response.text.splitlines():
    if "url: '" in line:
        instance_list.append(line.replace("url: '", "").replace("',", "").strip())

print(instance_list)


def check_instances(instances):
    results = {}
    for instance in instances:
        try:
            r = requests.get(instance + "/weibo/user/5617891490", timeout=60)
            results[instance] = r.status_code
            if "Location" in r.headers:
                results[instance] = f"Redirected to {r.headers['Location']}"
        except requests.RequestException as e:
            results[instance] = str(e)
    return results


print(check_instances(instance_list))

result_test = {
    "https://rsshub.rssforever.com": 503,
    "https://hub.slarker.me": 503,
    "https://rsshub.pseudoyu.com": 503,
    "https://rsshub.rss.tips": 502,
    "https://rsshub.ktachibana.party": 503,
    "https://rss.owo.nz": 503,
    "https://rss.wudifeixue.com": "HTTPSConnectionPool(host='rss.wudifeixue.com', port=443): Max retries exceeded with url: /weibo/user/5617891490 (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:992)')))",
    "https://rss.littlebaby.life/rsshub": 503,
    "https://rsshub.henry.wang": "HTTPSConnectionPool(host='rsshub.henry.wang', port=443): Max retries exceeded with url: /weibo/user/5617891490 (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x70d952497510>: Failed to establish a new connection: [Errno -5] No address associated with hostname'))",
    "https://holoxx.f5.si/": "HTTPSConnectionPool(host='holoxx.f5.si', port=443): Max retries exceeded with url: //weibo/user/5617891490 (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate (_ssl.c:992)')))",
    "https://rsshub.umzzz.com": 503,
    "https://rsshub.isrss.com": "HTTPSConnectionPool(host='rsshub.isrss.com', port=443): Max retries exceeded with url: /weibo/user/5617891490 (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate (_ssl.c:992)')))",
    "https://rsshub.email-once.com": "HTTPSConnectionPool(host='rsshub.email-once.com', port=443): Max retries exceeded with url: /weibo/user/5617891490 (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x70d952495fd0>: Failed to establish a new connection: [Errno -2] Name or service not known'))",
    "https://rss.datuan.dev": 503,
    "https://rsshub.asailor.org": 500,
    "https://rsshub2.asailor.org": 522,
    "https://rss.4040940.xyz": 200,
    "https://rsshub.cups.moe": 503,
}

import os


def sendTelegramMessage(message: str):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN")
    chat_id = "-1001982849593"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
    }
    requests.post(url, data=payload)


result_text = "RSSHub Instance Check Results:\n"
for instance, status in result_test.items():
    status_sent = "❌" if status != 200 else "✅"
    result_text += f"{status_sent}{instance}\n"

sendTelegramMessage(result_text)
