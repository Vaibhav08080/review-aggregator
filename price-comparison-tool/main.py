from scraper import extract_amazon_product_details, search_flipkart
from utils import is_similar, is_same_product

def display_results(similar_products, amazon_description):
    """
    Display similar products to the user.
    """
    if similar_products:
        print("We couldn't find the exact product, but here are some similar options:")
        for product in similar_products:
            if is_same_product(amazon_description, product['description']):
                print(f"Exact Match Found: {product['name']} - {product['price']}")
            else:
                print(f"Similar Product: {product['name']} - {product['price']}")
    else:
        print("Sorry, we couldn't find this product or any similar options.")

def main():
    # Step 1: User provides a product link
    user_link = input("Enter the Amazon product link: ")

    # Step 2: Extract product details from Amazon
    print("Extracting product details...")
    product_details = extract_amazon_product_details(user_link)
    print(f"Product Name: {product_details['name']}")
    print(f"Price: {product_details['price']}")
    print(f"Description: {product_details['description']}")

    # Step 3: Search for similar products on Flipkart
    print("Searching for similar products on Flipkart...")
    similar_products = search_flipkart(product_details['name'])

    # Step 4: Display results
    display_results(similar_products, product_details['description'])

if __name__ == "__main__":
    main()