import requests
from bs4 import BeautifulSoup

def extract_amazon_product_details(url):
    """
    Extract product details from an Amazon product page.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract product name
    product_name = soup.find('span', {'id': 'productTitle'}).text.strip()

    # Extract price
    price_element = soup.find('span', {'class': 'a-price-whole'})
    price = price_element.text.strip() if price_element else "Price not available"

    # Extract description
    description_element = soup.find('div', {'id': 'productDescription'})
    description = description_element.text.strip() if description_element else "No description available"

    return {
        'name': product_name,
        'price': price,
        'description': description
    }

def search_flipkart(product_name):
    """
    Search for similar products on Flipkart.
    """
    search_query = product_name.replace(" ", "+")
    flipkart_url = f"https://www.flipkart.com/search?q={search_query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(flipkart_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract similar products
    similar_products = []
    for item in soup.find_all('div', {'class': '_2kHMtA'}):  # Flipkart product class
        name = item.find('div', {'class': '_4rR01T'}).text.strip()
        price = item.find('div', {'class': '_30jeq3'}).text.strip()
        description = item.find('div', {'class': 'fMghEO'}).text.strip() if item.find('div', {'class': 'fMghEO'}) else "No description available"
        similar_products.append({'name': name, 'price': price, 'description': description})

    return similar_products