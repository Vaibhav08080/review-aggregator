from scraper import extract_amazon_product_details, search_flipkart

def display_results(similar_products, amazon_details):
    """
    Display results to the user.
    """
    if similar_products:
        print("Similar products found on Flipkart:")
        for product in similar_products:
            print(f"{product['name']} - {product['price']} - Rating: {product['rating']}")
    else:
        print("No similar products found on Flipkart. Showing results for Amazon only.")
        print(f"Product Name: {amazon_details['name']}")
        print(f"Price: {amazon_details['price']}")
        print(f"Rating: {amazon_details['rating']}")
        if 'features' in amazon_details:
            print(f"Features: {', '.join(amazon_details['features'])}")
        else:
            print("Features: No features available")
        # Provide recommendation based on Amazon data only
        provide_recommendation(amazon_details)

def provide_recommendation(product_details):
    """
    Provide a recommendation based on product details.
    """
    price = product_details['price']
    if price == "Price not available":
        print("Recommendation: Price not available. Cannot provide recommendation.")
        return

    # Remove currency symbols and commas
    price = price.replace('₹', '').replace(',', '')
    try:
        price = float(price)
    except ValueError:
        print("Recommendation: Invalid price format. Cannot provide recommendation.")
        return

    # Extract rating (e.g., "4.5 out of 5 stars" -> 4.5)
    rating = product_details['rating']
    if rating != "Rating not available":
        try:
            rating_value = float(rating.split()[0])  # Extract the numeric part
        except (ValueError, IndexError):
            rating_value = None
    else:
        rating_value = None

    # Provide recommendation based on price and rating
    if rating_value is not None:
        if price < 20000 and rating_value >= 4.0:
            print("Recommendation: Buy (Good price and high rating!)")
        elif price < 30000 and rating_value >= 3.5:
            print("Recommendation: Wait (Moderate price and decent rating).")
        else:
            print("Recommendation: Don't Buy (Price is too high or rating is low).")
    else:
        if price < 20000:
            print("Recommendation: Buy (Good price!)")
        elif price < 30000:
            print("Recommendation: Wait (Price is moderate).")
        else:
            print("Recommendation: Don't Buy (Price is too high).")

def main():
    # Step 1: User provides a product link
    user_link = input("Enter the Amazon product link: ")

    # Step 2: Extract product details from Amazon
    print("Extracting product details...")
    amazon_details = extract_amazon_product_details(user_link)
    print(f"Product Name: {amazon_details['name']}")
    print(f"Price: {amazon_details['price']}")
    print(f"Rating: {amazon_details['rating']}")
    if 'features' in amazon_details:
        print(f"Features: {', '.join(amazon_details['features'])}")
    else:
        print("Features: No features available")

    # Step 3: Search for similar products on Flipkart
    print("Searching for similar products on Flipkart...")
    similar_products = search_flipkart(amazon_details['name'])

    # Step 4: Display results
    display_results(similar_products, amazon_details)

if __name__ == "__main__":
    main()