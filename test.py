
 # Replace with the path to your HTML file

# print(final_data)


from bs4 import BeautifulSoup
import json
import uuid

# Load the HTML content
with open('coincap.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Extract the necessary data
job_id = str(uuid.uuid4())
tasks = []

# Assuming we need to extract data for different coins
coins = ["DUKO", "NOT", "GORILLA"]
for coin in coins:
    # This is an example structure. You'll need to adjust the selectors based on actual HTML structure
    # For instance, to get price, we might look for a specific class or ID
    coin_data = {
        "coin": coin,
        "output": {
            "price": (soup.find('span', {'class': 'sc-d1ede7e3-0 fsQm base-text'}).text.strip().replace('$', '')),
            "price_change": float(soup.find('p', {'class': 'sc-71024e3e-0 sc-58c82cf9-1 bgxfSG iPawMI'}).text.strip()[:4].replace('%', '')),
            "market_cap": int(soup.find('dd', {'class': 'sc-d1ede7e3-0 hPHvUM base-text'}).text.split("%")[1].replace('$', '').replace(',', '')),
            "market_cap_rank": int(soup.find('span', {'class': 'text slider-value rank-value'}).text.strip().replace('#', '')),
            "volume": int(soup.find('dd', {'class': 'sc-d1ede7e3-0 hPHvUM base-text'}).text.split("%")[1].replace('$', '').replace(',', '')),
            "volume_rank": int(soup.find('span', {'class': 'text slider-value rank-value'}).text.strip().replace('#', '')),
            "volume_change": float(soup.find('span', {'class': 'volume-change'}).text.strip().replace('%', '')),
            "circulating_supply": int(soup.find('div', {'class': 'circulating-supply'}).text.strip().replace(',', '')),
            "total_supply": int(soup.find('div', {'class': 'total-supply'}).text.strip().replace(',', '')),
            "diluted_market_cap": int(soup.find('div', {'class': 'diluted-market-cap'}).text.strip().replace('$', '').replace(',', '')),
            "contracts": [
                {
                    "name": soup.find('span', {'class': 'contract-name'}).text.strip(),
                    "address": soup.find('span', {'class': 'contract-address'}).text.strip()
                }
            ],
            "official_links": [
                {
                    "name": link.text.strip(),
                    "link": link['href']
                }
                for link in soup.find_all('a', {'class': 'official-link'})
            ],
            "socials": [
                {
                    "name": link.text.strip(),
                    "url": link['href']
                }
                for link in soup.find_all('a', {'class': 'social-link'})
            ]
        }
    }
    tasks.append(coin_data)

# print(coin_data)
# Combine the job ID and tasks into the final structure
final_data = {
    "job_id": job_id,
    "tasks": tasks
}

# Convert to JSON
# json_data = json.dumps(final_data, indent=2)

# # Print or save the JSON data
# print(json_data)
# # Or save to a file
# with open('/mnt/data/output.json', 'w', encoding='utf-8') as output_file:
#     output_file.write(json_data)
