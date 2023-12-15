import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup


MAX_CONCURRENT_REQUESTS=1
def write_to_file(file_path, text):
    with open(file_path, 'a') as file:
        file.write(text + '\n')
async def fetch(session, semaphore, sub, target_domain):
    url = f"http://{sub}.{target_domain}"
    domain=target_domain.strip(".com")
    async with semaphore:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    write_to_file(f"C:/Users/PC/GIT/Web-Scanner/subdomains_{domain}.txt",url.strip("http://"))
                elif response.status == 401:
                    write_to_file("C:/Users/PC/GIT/Web-Scanner/test.txt",url.strip("http://"))
        except aiohttp.ClientError as e:
          return None
        except asyncio.TimeoutError as e:
          return None

async def enumerate_subdomains(target_domain, subdomain_list, rate):
    MAX_CONCURRENT_REQUESTS=rate
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
    Timeout=aiohttp.ClientTimeout(10)
    async with aiohttp.ClientSession(timeout=Timeout) as session:
        tasks = [fetch(session, semaphore, sub, target_domain) for sub in subdomain_list]
        await asyncio.gather(*tasks)

def load_subdomains_from_file(file_path):
    with open(file_path) as file:
        return file.read().splitlines()

def extract_subdomains_from_crtSH(domain):
    flag=0
    url = f"https://crt.sh/?Identity={domain}&exclude=expired"

    request=requests.get(url)
    if request.status_code != 200:
        print("crt_sh response qaytarmadi")
        return []
    soup=BeautifulSoup(request.content,"html.parser")
    subdomains=set()
    for row in soup.find_all("tr"):

        tds = row.find_all("td")
        if len(tds) > 4:  
            for subdomain in tds[4].text.split('<BR>'):
                if domain in subdomain:
                    subdomains.add(subdomain.strip('*'))
    return subdomains