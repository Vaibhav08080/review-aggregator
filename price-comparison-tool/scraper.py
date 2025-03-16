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
    product_name = soup.find('span', {'id': 'productTitle'})
    product_name = product_name.text.strip() if product_name else "Product name not found"

    # Extract price
    price_element = soup.find('span', {'class': 'a-price-whole'})
    price = price_element.text.strip() if price_element else "Price not available"

    # Extract rating
    rating_element = soup.find('span', {'class': 'a-icon-alt'})
    if rating_element:
        rating_text = rating_element.text.strip()
        # Extract numeric part of the rating (e.g., "4.5 out of 5 stars" -> 4.5)
        rating = rating_text.split()[0]
    else:
        rating = "Rating not available"

    # Extract features (if available)
    feature_elements = soup.find_all('li', {'class': 'a-spacing-mini'})
    features = list(set([element.text.strip() for element in feature_elements])) if feature_elements else ["No features available"]

    return {
        'name': product_name,
        'price': price,
        'rating': rating,
        'features': features
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
        name = item.find('div', {'class': '_4rR01T'})
        price = item.find('div', {'class': '_30jeq3'})
        rating = item.find('div', {'class': '_3LWZlK'})
        if name and price:
            similar_products.append({
                'name': name.text.strip(),
                'price': price.text.strip(),
                'rating': rating.text.strip() if rating else "Rating not available"
            })

    return similar_products if similar_products else None