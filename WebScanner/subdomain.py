import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup



MAX_CONCURRENT_REQUESTS = 10  


async def fetch(session, semaphore, sub, target_domain):
    url = f"http://{sub}.{target_domain}"
    async with semaphore:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    print("\033[92mValid domain:\033[0m", url)
                    print("\033[90mStatus:200\033[0m")
                elif response.status == 401:
                    print("\033[92mValid domain:\033[0m", url) 
                    print("\033[90mStatus:401\033[0m")
        except aiohttp.ClientError as e:
          return None
        except asyncio.TimeoutError as e:
          return None

async def enumerate_subdomains(target_domain, subdomain_list):
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
    Timeout=aiohttp.ClientTimeout(10)
    async with aiohttp.ClientSession(timeout=Timeout) as session:
        tasks = [fetch(session, semaphore, sub, target_domain) for sub in subdomain_list]
        await asyncio.gather(*tasks)

def load_subdomains_from_file(file_path):
    with open(file_path) as file:
        return file.read().splitlines()
    
def extract_subdomains_from_crtSH(domain):
    url = f"https://crt.sh/?q=%.{domain}&exclude=expired"
    request=requests.get(url)
    if request.status_code != 200:
        print("crt_sh response qaytarmadi")
        return []
    soup=BeautifulSoup(request.content,"html.parser")
    subdomains=set()
    for row in soup.find_all("tr"):
        for td in row.find_all("td"):
            if "@" not in td.text:
                possible_subdomain = td.text.strip()
                if "." + domain in possible_subdomain:
                    subdomains.add(possible_subdomain)
    return subdomains



    