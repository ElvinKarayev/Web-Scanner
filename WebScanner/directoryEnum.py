import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

def check_directory(domain, directory):
    url = f"http://{domain}/{directory}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            
            return (url,response.status_code)
        elif response.status_code == 301:
            return (url,response.status_code)
    except:
        return None

def Enumerate(domain, directories,rate):
    results = []
    with ThreadPoolExecutor(max_workers=rate) as executor:
        future_to_url = {executor.submit(check_directory, domain, directory):directory for directory in directories}
        for future in as_completed(future_to_url):
            url = future.result()
            if url:
               results.append(url)
    return results