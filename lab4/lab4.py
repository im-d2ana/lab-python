import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import re
from urllib.parse import urljoin
import warnings
from fake_useragent import UserAgent

warnings.filterwarnings('ignore')
ua = UserAgent()

def get_headers():
    return {
        'User-Agent': ua.random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
    }

def search_vessel_by_name(vessel_name):
    base_url = "https://www.vesselfinder.com"
    search_url = f"{base_url}/ru/vessels"
    headers = get_headers()
    params = {'name': vessel_name}

    try:
        time.sleep(random.uniform(3, 6))
        session = requests.Session()
        session.headers.update(headers)
        session.get(base_url, timeout=30)
        response = session.get(search_url, params=params, timeout=30)

        if response.status_code != 200:
            return None, 0
        soup = BeautifulSoup(response.text, 'html.parser')
        results_div = soup.find('div', class_='search-results')

        if results_div:
            ship_links = results_div.find_all('a', class_='ship-link')
            count = len(ship_links)
            if count == 1:
                return urljoin(base_url, ship_links[0].get('href', '')), 1
            return None, count
        
        ship_links = soup.find_all('a', href=re.compile(r'/ru/vessels/'))
        direct_vessels = [l.get('href', '') for l in ship_links if '/ru/vessels/' in l.get('href', '') and ('IMO-' in l.get('href', '') or 'MMSI-' in l.get('href', '') or 'vessels/details/' in l.get('href', ''))]
        count = len(direct_vessels)

        if count == 1:
            return urljoin(base_url, direct_vessels[0]), 1
        if count == 0 and (soup.find('div', class_='vi__r1 vi__sticky-wrap') or soup.find('div', class_='vi__r1') or soup.find('h1', class_='text-nowrap')):
            return response.url, 1
        return None, count
    
    except:
        return None, 0

def parse_vessel_page(soup):
    result = {'Название': '', 'IMO': '', 'MMSI': '', 'Тип': ''}
    try:
        for sel in ['h1', '.vi__r1 h1', '.text-nowrap', '.ship-name', '[itemprop="name"]']:
            el = soup.select_one(sel)
            if el and el.get_text(strip=True):
                result['Название'] = el.get_text(strip=True)
                break

        for sel in ['.imo', '[data-imo]', 'span:contains("IMO")', 'td:contains("IMO") + td', 'th:contains("IMO") + td', '.ship-data .imo']:
            el = soup.select_one(sel)
            if el:
                m = re.search(r'(\d{7})', el.get_text(strip=True))
                if m:
                    result['IMO'] = m.group(1)
                    break

        if not result['IMO']:
            text = soup.get_text()
            for p in [r'IMO\s*[:]?\s*(\d{7})', r'IMO\s+(\d{7})', r'IMO\s*№?\s*(\d{7})', r'IMO:\s*(\d{7})', r'IMO/.*?(\d{7})', r'IMO.*?(\d{7})']:
                m = re.search(p, text, re.IGNORECASE)
                if m:
                    result['IMO'] = m.group(1)
                    break

        for sel in ['span:contains("MMSI")', 'td:contains("MMSI") + td', 'th:contains("MMSI") + td', '[data-mmsi]', '.ship-data .mmsi']:
            el = soup.select_one(sel)
            if el:
                m = re.search(r'(\d{9})', el.get_text(strip=True))
                if m:
                    result['MMSI'] = m.group(1)
                    break

        if not result['MMSI']:
            text = soup.get_text()
            for p in [r'MMSI\s*[:]?\s*(\d{9})', r'MMSI\s+(\d{9})', r'MMSI:\s*(\d{9})', r'MMSI.*?(\d{9})']:
                m = re.search(p, text, re.IGNORECASE)
                if m:
                    result['MMSI'] = m.group(1)
                    break

        type_text = ''
        for sel in ['.ship-type', '.vessel-type', 'span:contains("Type")', 'td:contains("Type") + td', 'th:contains("Type") + td', 'td:contains("Тип") + td', 'th:contains("Тип") + td', '[itemprop="additionalType"]', '.vi__sticky-wrap span:contains("Type")', '.vi__r1 span:contains("Type")', '.ship-info span:contains("Type")']:
            el = soup.select_one(sel)
            if el:
                parent_text = el.parent.get_text(strip=True) if el.parent else el.get_text(strip=True)
                m = re.search(r'(?:Type|Тип)[:\s]+([^,;\n]+)', parent_text, re.IGNORECASE)
                if m:
                    type_text = m.group(1).strip()
                    break

        if not type_text:
            text = soup.get_text()
            for p in [r'Type[:\s]+([^,\n;]{3,30})', r'Тип[:\s]+([^,\n;]{3,30})', r'Ship Type[:\s]+([^,\n;]{3,30})', r'Vessel Type[:\s]+([^,\n;]{3,30})', r'Type of vessel[:\s]+([^,\n;]{3,30})']:
                m = re.search(p, text, re.IGNORECASE)
                if m:
                    type_text = m.group(1).strip()
                    break

        result['Тип'] = re.sub(r'[^\w\s\-/]', ' ', type_text).strip()

    except:
        pass

    return result

def get_vessel_details(vessel_url):
    try:
        headers = get_headers()
        time.sleep(random.uniform(2, 4))
        response = requests.get(vessel_url, headers=headers, timeout=30)

        if response.status_code != 200:
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        data = parse_vessel_page(soup)

        if not data['Название']:
            h1 = soup.find('h1')
            if h1:
                data['Название'] = h1.get_text(strip=True)

        if not data['IMO']:
            m = re.search(r'IMO-(\d{7})', vessel_url)
            if m:
                data['IMO'] = m.group(1)
        return data
    
    except:
        return None

def extract_vessel_name_from_url(url):
    m = re.search(r'name=([^&]+)', url)
    if m:
        return m.group(1).replace('+', ' ').strip()
    
    parts = url.split('/')
    if parts:
        return parts[-1].replace('-', ' ').strip()
    return ''

def process_vessel(url):
    vessel_name = extract_vessel_name_from_url(url)
    if not vessel_name:
        return None
    
    vessel_url, count = search_vessel_by_name(vessel_name)
    if count != 1 or not vessel_url:
        return None
    
    return get_vessel_details(vessel_url)

def main():
    try:
        df_links = pd.read_excel('Links.xlsx')
    except:
        return
    
    if 'Ссылка' not in df_links.columns:
        return
    urls = df_links['Ссылка'].dropna().tolist()

    # urls = urls[:10]
    results = []

    for url in urls:
        data = process_vessel(url)
        if data and any(data.values()):
            results.append(data)
        time.sleep(random.uniform(5,10))

    if results:
        df_results = pd.DataFrame(results)
        if 'Ссылка' in df_results.columns:
            df_results = df_results.drop(columns=['Ссылка'])
        df_results.to_excel('result.xlsx', index=False)

if __name__ == "__main__":
    main()