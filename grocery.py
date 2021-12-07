import urllib.request
import json

store_urls = [
    "https://acceleratorlake.blob.core.windows.net/code/store_a.json",
    "https://acceleratorlake.blob.core.windows.net/code/store_b.json",
    "https://acceleratorlake.blob.core.windows.net/code/store_c.json",
]


def get_json(url):
    """
    Fires a request to the given URL and
    converts the json response into a dictionary and returns it
    """
    try:
        contents = urllib.request.urlopen(url).read()
    except Exception as e:
        raise Exception(f"something went wrong while trying to do an HTTP Get: {e}")
    return json.loads(contents)


def write_file(path, content):
    "Writes the given content into a file whose complete path is given"
    with open(path, "w") as file:
        file.write(content)


def process_resposne(response):
    """
    Loops through a given response and returns the total_sales and distinct categories
    """
    total_sales, categories = 0, set()
    for order in response.get("orders", []):
        for item in order.get("items", []):
            # add the price of the item to the total sales
            total_sales += item["total_price"]
            # add the category of the item to a set
            categories.add(item["category"])
    return total_sales, categories


total_sales, categories = {"total_sales": 0}, set()

for url in store_urls:
    # get the sales and categories for the store by processing the data from the url
    sales_for_store, categories_for_store = process_resposne(get_json(url))
    total_sales["total_sales"] += sales_for_store
    # update the categories set with new values (if any)
    categories.update(categories_for_store)

# convert total_sales into a json string and write it to a file called total_sales.json
write_file("total_sales.json", json.dumps(total_sales, indent=4))

# create a dictionary, convert it to a json string and then write it to a file called categories.json
write_file("categories.json", json.dumps({"categories": list(categories)}, indent=4))
