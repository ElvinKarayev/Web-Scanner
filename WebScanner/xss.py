import requests
import re
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from colorama import Fore, Style
import argparse

async def read_payloads(file_path):
    try:
        with open(file_path, 'r') as file:
            payloads = [line.strip() for line in file.readlines() if line.strip()]
        return payloads
    except Exception as e:
        print(f"{Fore.RED}Fayl yolu yanlis daxil edildi : {str(e)}")
        return []

async def find_inputs(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, allow_redirects=True, timeout=10) as response:
                html = await response.text()
        except Exception as e:
            print(f"{Fore.RED}Hedef URL ile elaqe qurula bilmedi {str(e)}")
            return []
    soup = BeautifulSoup(html, 'html.parser')
    inputs = soup.find_all('input')
    return inputs

async def test_payload(url, input_name, payload):
    async with aiohttp.ClientSession() as session:
        test_url = f"{url}?{input_name}={payload}"
        try:
            response = await session.get(test_url, allow_redirects=True, timeout=10)
            await asyncio.sleep(0.2)  # kicik gozlenti
            if payload in await response.text():
                print(f"{Fore.GREEN}Payload '{payload}' ugurla çalıştı: {test_url}")
            else:
                print(f"{Fore.RED}Payload '{payload}' ugursuz oldu : {test_url}")
        except Exception as e:
            print(f"{Fore.RED}Payload  xətası. Bu payload'i manuel şəkildə yoxlamğınız tövsiyyə olunur.: '{payload}': {str(e)}")

async def detect_xss(url, inputs, payloads, max_payloads_before_error=5):
    tasks = []
    payload_counter = 0

    for input_field in inputs:
        input_name = input_field.get('name') or input_field.get('id')
        if input_name:
            for payload in payloads:
                task = asyncio.create_task(test_payload(url, input_name, payload))
                tasks.append(task)
                payload_counter += 1

                # Maksimum sorgu sayısına catdiqda
                if payload_counter >= max_payloads_before_error:
                    await asyncio.gather(*tasks, return_exceptions=True)
                    tasks = []  # sıfırlama
                    payload_counter = 0

    # qalan payloadlarin elave edilmesi
    if tasks:
        await asyncio.gather(*tasks, return_exceptions=True)

def parse_arguments():
    parser = argparse.ArgumentParser(description='XSS scanner')
    parser.add_argument('url', type=str, nargs='?', help='Hədəf URL')
    parser.add_argument('--threads', type=int, default=5, help='Thread sayısı')
    parser.add_argument('--payloads', type=str, default='xsspayloads.txt', help='Payload yaylının yolu')
    return parser.parse_args()

def get_user_input(prompt, default=None):
    user_input = input(prompt + (f" (deafult: {default})" if default else "") + ": ")
    return user_input if user_input else default

if __name__ == "__main__":
    args = parse_arguments()

    if not args.url:
        attempts = 0
        while attempts < 3:
            target_url = get_user_input("Xahis edilir mumkun url daxil edin: ")
            if re.match(r'https?://(?:www\.)?[\w\.-]+(?:\.[\w\.-]+)+', target_url):
                args.url = target_url
                break
            else:
                print("Daxil edilen Url islemedi.Duzgun url daxil etmeyiniz xahis olunur...")
                attempts += 1

        if attempts == 3:
            print("Yanlis daxil edilme limitine catdiniz, programdan cixilir")
            exit()

    # Payload'ların fayldan oxunmasi
    payloads_file_path = args.payloads
    payloads = asyncio.run(read_payloads(payloads_file_path))

    # Hədəf URL'deki inputların tapilmasi
    user_inputs = asyncio.run(find_inputs(args.url))

    # İnputlarda payloadların yoxlanması və nəticəsi
    asyncio.run(detect_xss(args.url, user_inputs, payloads, max_payloads_before_error=args.threads))
