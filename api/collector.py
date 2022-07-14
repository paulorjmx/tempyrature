import asyncio
import logging
import httpx
from bs4 import BeautifulSoup

from confluent_kafka import Producer


logger = logging.getLogger("collector")

cities = []
with open("api/cities.txt", "r") as f:
    cities = f.readlines()
cities = [c.strip() for c in cities[:1]]


producer = Producer(
    {'bootstrap.servers': 'kafka:9092'}
)


async def get_temp(session: httpx.AsyncClient, city: str):
    q = "+".join(city.split())
    # url = f'https://www.google.com/search?q={q}+temperatura'
    url = ""
    
    try:
        res = await session.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        temp_div = soup.find("div", {"class": "BNeawe iBp4i AP7Wnd"})
        if temp_div:
            return temp_div.text.split()[0]
    except Exception as e:
        return 25


async def main():
    headers = {
        "user-agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
    }

    while True:
        async with httpx.AsyncClient(headers=headers) as session:
            tasks = [get_temp(session, city) for city in cities]
            values = await asyncio.gather(*tasks)
        
        for c, t in zip(cities, values):
            logger.info(f"Cidade {c}, temp {t}")   
            producer.produce("city_temp", f"{c} {t}".encode("utf-8"))

        await asyncio.sleep(60)

if __name__ == '__main__':
    logger.info("Collector started")
    asyncio.run(main())
