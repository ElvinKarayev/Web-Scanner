import asyncio
import aiohttp


MAX_CONCURRENT_REQUESTS=1

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


    