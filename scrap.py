import requests
from bs4 import BeautifulSoup

def fetch_uranium_price_table():
    url = "https://www.cameco.com/invest/markets/uranium-price"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Find the price table
    table = soup.find("table")

    # Extract headers (years)
    headers = [th.get_text(strip=True) for th in table.find("tr").find_all("th")]
    years = headers[1:]  # first column is "Month"

    # Extract rows (month + values for each year)
    price_data = []
    for row in table.find_all("tr")[1:]:
        cols = [td.get_text(strip=True) for td in row.find_all("td")]
        if not cols:
            continue
        month = cols[0]
        prices = cols[1:]
        for year, price in zip(years, prices):
            if price != "":
                price_data.append((f"{month} {year}", float(price)))

    return price_data

def get_last_two_prices():
    data = fetch_uranium_price_table()
    #print(data[-2:])
    return data[-2:]  # last two entries

if __name__ == "__main__":
    last_two = get_last_two_prices()
    for date, price in last_two:
        print(f"{date}: ${price}/lb")
