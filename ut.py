import requests

headers = {
    "Origin": "https://scan.chainx.org",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
}


def getfree(address):
    url = f"http://localhost:4000/getfree?address={address}"
    z = requests.get(url)
    return z.json()


def check(account):
    headers["Referer"] = f"https://scan.chainx.org/accounts/{account}"
    url1 = f"https://api.chainx.org/account/{account}/balance?native=false"
    url2 = f"https://api.chainx.org/account/{account}/balance?native=true"
    url3 = f"https://api.chainx.org/account/{account}/txs?page=0&page_size=10"
    z1 = requests.get(url1, headers=headers)
    z2 = requests.get(url2, headers=headers)
    for i in z1.json() + z2.json():
        if i["token"] == "PCX":
            if i["Free"] != 0:
                return {"msg": "PCX余额不为空", "status": 0}
        if i["token"] in ["BTC", "SDOT"]:
            if i["Free"] < 10:
                return {"msg": "BTC或者SDOT余额为空", "status": 0}

    z3 = requests.get(url3, headers=headers)
    if z3.json()["total"] != 0:
        return {"msg": "不是新账号", "status": 0}
    return getfree(account)


if __name__ == "__main__":
    a = check("0xe4aa679f0140e935338b147c0685380a8e95689605bb9846e236edaa973d624c")
    print(a)
