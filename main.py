import aiohttp
import aiofiles
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Список ссылок
urls = [
    "https://regex101.com/",
    "https://docs.python.org/3/this-url-will-404.html",
    "https://www.nytimes.com/guides/",
    "https://www.mediamatters.org/",
    "https://1.1.1.1/",
    "https://www.politico.com/tipsheets/morning-money",
    "https://www.bloomberg.com/markets/economics",
    "https://www.ietf.org/rfc/rfc2616.txt"
]


# Асинхронная функция для получения HTML страницы
async def fetch(session, url):
    try:
        async with session.get(url, ssl=False) as response:
            if response.status == 200:
                return await response.text(), url
            else:
                print(f"Error: {url} returned status code {response.status}")
                return None, url
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None, url


# Асинхронная функция для извлечения ссылок
async def extract_links(html, base_url):
    if not html:
        return []

    soup = BeautifulSoup(html, 'html.parser')
    links = [urljoin(base_url, a.get('href')) for a in soup.find_all('a', href=True)]
    return links


# Асинхронная функция для записи ссылок в файл
async def write_links_to_file(links, filename='found_links.txt'):
    async with aiofiles.open(filename, 'a') as f:
        for link in links:
            await f.write(f"{link}\n")


# Основная асинхронная функция для обработки всех URL
async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        responses = await asyncio.gather(*tasks)

        all_links = []
        for html, base_url in responses:
            if html:
                links = await extract_links(html, base_url)
                all_links.extend(links)

        await write_links_to_file(all_links)


# Запуск асинхронной функции
if __name__ == '__main__':
    asyncio.run(main())
