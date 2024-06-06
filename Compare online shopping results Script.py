import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import sqlite3
import time
from fuzzywuzzy import fuzz


def scrape_reliance(search_url):
    print("Going to url: ", search_url)
    headers = {
        'User-Agent': ''
    }
    response = requests.get(search_url, headers=headers)
    
    if response.status_code != 200:
        print("Failed to retrieve the webpage")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    results = []
    with open('reliance.txt', 'w', encoding='utf-8') as file:
        file.write(soup.prettify())

    for product in soup.find_all('div', {'class': 'sp__product'}):
        name_tag = product.find('p', {'class': 'sp__name'})
        price_tag = product.find('span', {'class': 'TextWeb__Text-sc-1cyx778-0'})
        
        if name_tag and price_tag:
            name = name_tag.text.strip()
            price = price_tag.text.strip()
            results.append({'name': name, 'price': price})
    
    return results


def scrape_flipkart(search_url):
    print("Going to url: ", search_url)
    headers = {
        'User-Agent': '*',
    }
    response = requests.get(search_url, headers=headers)
    
    if response.status_code != 200:
        print("Failed to retrieve the webpage")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    results = []

    for product in soup.find_all('div', {'class': 'cPHDOP'}):
        name_tag = product.find('div', {'class': 'KzDlHZ'})
        price_tag = product.find('div', {'class': 'Nx9bqj _4b5DiR'})
        
        if name_tag and price_tag:
            name = name_tag.text.strip()
            price = price_tag.text.strip()
            results.append({'name': name, 'price': price})
    
    return results


def match_and_compare(data1, data2):
    matched_data = []
    for product1 in data1:
        for product2 in data2:
            if fuzz.partial_ratio(product1['name'], product2['name']) >= 65:
                matched_data.append((product1, product2))
    return matched_data


def visualize_data(matched_data):
    reliance_prices = [data[0]['price'] for data in matched_data]
    flipkart_prices = [data[1]['price'] for data in matched_data]
    product_names = [data[0]['name'] for data in matched_data]
    num_products = len(product_names)

    # Set the width of the bars and the gap between them
    bar_width = 0.35
    gap = 0.1

    plt.figure(figsize=(12, 6))

    # Adjust the x-coordinates of the bars
    x_reliance = [i - (bar_width + gap) for i in range(num_products)]
    x_flipkart = [i + (bar_width + gap) for i in range(num_products)]

    plt.bar(x_reliance, reliance_prices, width=bar_width, label='Reliance Digital')
    plt.bar(x_flipkart, flipkart_prices, width=bar_width, label='Flipkart')

    # Set the x-ticks and labels
    plt.xticks([i for i in range(num_products)], product_names, rotation=35)

    plt.xlabel('Product Name')
    plt.ylabel('Price')
    plt.title('Price Comparison of Reliance digital vs Flipkart')
    plt.legend()
    plt.tight_layout()
    plt.show()


def store_in_database(data1, data2, matched_data):
    conn = sqlite3.connect('products.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS reliance
                 (name TEXT, price REAL, other_details TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS flipkart
                 (name TEXT, price REAL, other_details TEXT)''')

    for product in data1:
        c.execute("INSERT INTO reliance VALUES (?, ?)", (product['name'], product['price']))

    for product in data2:
        c.execute("INSERT INTO flipkart VALUES (?, ?)", (product['name'], product['price']))

    conn.commit()
    conn.close()


def main():
    # searchQuery = input('Enter Search Query (Leave Blank for default: "voltas air conditioner 1.5 ton split"): ')
    # searchQuery = "voltas air conditioner 1.5 ton split" if searchQuery == "" else searchQuery
    # searchQuery = "voltas air conditioner 1.5 ton split"

    # relianceQuery = searchQuery.replace(' ', '%20')
    # flipkartQuery = searchQuery.replace(' ', '%20')

    # reliance = scrape_reliance(f'https://www.reliancedigital.in/search?q={relianceQuery}%20split:relevance')
    # flipkart = scrape_flipkart(f'https://www.flipkart.com/search?q={flipkartQuery}')

    reliance = [{'name': 'Voltas 1.5 Ton 3 star split AC, 183 Vectra Prism ( 100 Percent copper, Dual temperature display, Dual protection filter, self diagnosis)', 'price': '₹41,490.00'}, {'name': 'Voltas 1.5 Ton 5 Star 5-in-1 Convertible Inverter Split AC, 185V Vertis Magnum\xa0(Dual temp display, Turbo tech, Anti Fungal, 100 percent Copper, 2023 launch)', 'price': '₹39,990.00'}, {'name': 'Voltas 1.5 Ton 5 Star 4-in-1 Convertible Inverter Split AC, 185V Vectra Magnum\xa0(Turbo tech, Dual temp display, Anti Fungal, 100 percent Copper 2023 launch)', 'price': '₹44,490.00'}, {'name': 'Voltas 1.5 Ton 3 Star 4-in-1 Convertible Inverter Split AC, 183V Vectra Magnum (100 percent Copper, Turbo tech, Dual temp display, Anti-Fungal, 2023 launch)', 'price': '₹32,990.00'}, {'name': 'Voltas 2 Ton 3 star 4-in-1 Convertible Inverter split AC, 243V Vectra Elegant (100 Percent copper, Dual temperature display, Dual protection filter, self diagnosis)', 'price': '₹43,990.00'}, {'name': 'Voltas 1 Ton 3 Star 5-in-1 Convertible Inverter Split AC, 123V Vertis Magnum (100 percent Copper, Anti Fungal, Turbo tech, Blue Fin, 2023 launch)', 'price': '₹28,990.00'}, {'name': 'Voltas 2 Ton 5 star 6-in-1 Convertible Inverter split AC, 245V Vectra Plus ( 100 Percent copper, 4-way Swing, Dual Temperature Display, Dual Protection Filter, Self Diagnosis)', 'price': '₹54,990.00'}]
    flipkart = [{'name': 'Voltas 1.5 Ton 3 Star Split Inverter AC  - White', 'price': '₹32,990'}, {'name': 'Voltas 1.5 Ton 5 Star Split Inverter AC  - White', 'price': '₹38,990'}, {'name': 'Voltas 2023 Model 1.5 Ton 5 Star Split Inverter AC  - White', 'price': '₹38,990'}, {'name': 'Voltas 2023 Model 1.5 Ton 3 Star Split Inverter AC  - White', 'price': '₹32,990'}, {'name': 'Voltas 2023 Model 1.5 Ton 5 Star Split Inverter AC  - White', 'price': '₹39,990'}, {'name': 'Voltas 1.5 Ton 3 Star Split Inverter AC  - White', 'price': '₹35,490'}, {'name': 'Voltas 1.5 Ton 3 Star Split Inverter AC  - White', 'price': '₹32,990'}, {'name': 'Voltas 2023 Model 1.5 Ton 3 Star Split Inverter AC  - White', 'price': '₹35,990'}, {'name': 'Voltas 1.5 Ton 3 Star Split Inverter AC  - White', 'price': '₹32,990'}, {'name': 'Voltas 2023 Model 1.5 Ton 3 Star Split AC  - White', 'price': '₹33,699'}, {'name': 'Voltas 1.5 Ton 3 Star Split Inverter adjustible AC  - White', 'price': '₹37,900'}, {'name': 'Voltas 1.5 Ton 3 Star Split Inverter AC  - White', 'price': '₹33,499'}, {'name': 'Voltas 1.5 Ton 3 Star Split Inverter AC  - White', 'price': '₹34,490'}, {'name': 'Voltas 2023 Model 1.5 Ton 5 Star Split Inverter AC  - White', 'price': '₹42,499'}]    
    
    # print(reliance)
    # print("********************************************************")
    # print(flipkart)

    matched_data = match_and_compare(reliance, flipkart)
    # print(matched_data)

    visualize_data(matched_data)

    # store_in_database(data1, data2, matched_data)

if __name__ == '__main__':
    main()