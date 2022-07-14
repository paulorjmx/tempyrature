import httpx
import bs4

r = httpx.get("https://pt.wikipedia.org/wiki/Lista_de_munic%C3%ADpios_do_Brasil_por_popula%C3%A7%C3%A3o")

soup = bs4.BeautifulSoup(r.text, 'html.parser')
table = soup.find("table", {"class": "wikitable sortable"})
table_body = table.find('tbody')

data = []

rows = table_body.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    if len(cols) > 3:
        print(cols[2])
