import requests
from bs4 import BeautifulSoup

final_data = {}

def parse_data(soup):
    data = {}

    # Existing logic
    # data['price'] = float(soup.find('div', class_='priceValue').text.replace('$', '').replace(',', ''))

    # New logic
    

    coin_stats = soup.find('div', {'data-module-name': 'Coin-stats'})
    # print(coin_stats.prettify())
    if coin_stats:
        base_text = coin_stats.find('span', class_='sc-d1ede7e3-0 fsQm base-text')
        
        if base_text:
            data['base_text'] = base_text.text

        coin_metrics_table = coin_stats.find('dl', class_='sc-d1ede7e3-0 bwRagp coin-metrics-table')
        if coin_metrics_table:
            data['coin_metrics_table'] = [item.text for item in coin_metrics_table.find_all('dd')]

        coin_info_links = coin_stats.find_all('div', class_='sc-d1ede7e3-0 sc-7f0f401-0 gRSwoF gQoblf')
        # print(coin_info_links)
        if coin_info_links:
            for links in coin_info_links:
            
                a_tags = links.find_all('a')
                for a in a_tags:
                        print(a.get('href'))
                data['coin_info_links'] = [link.text for link in links]
    # print(data)
    return data


official_link  = {}
social = {}
def check_html_file(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # If the response was successful, no Exception will be raised
        soup = BeautifulSoup(response.text, 'html.parser')
        coin = soup.find('div',{'class': 'sc-d1ede7e3-0 eaAjIS coin-stats-header'})
        coin_name = (coin.find('span',{'class': 'sc-d1ede7e3-0 bEFegK'}).get('title'))
        coin_info_table = soup.find('div', {'class': 'sc-d1ede7e3-0 cvkYMS coin-info-links'})
        # print(coin_info_table)
        for section in coin_info_table.find_all('div',class_ = 'sc-d1ede7e3-0 jTYLCR'):
            head = (section.find('div', class_ = 'sc-d1ede7e3-0 kdeYgj').text.strip())
            # print(section.prettify())
            # print("head"+ head)
            for site in (section.find_all('div',class_ = 'sc-d1ede7e3-0 sc-7f0f401-0 gRSwoF gQoblf')):
                sitename = site.text.strip()
                siteurl = site.find('a').get('href')
                # print(siteurl)
                if head == "Official links":
                    official_link[sitename] = siteurl
                elif head == "Socials":
                    social[sitename] = siteurl

                    
       
        price_class = (soup.find('div',class_ = 'sc-d1ede7e3-0 gNSoet flexStart alignBaseline'))
        price = price_class.text
        # print("here")
        details = price.split()
        # print(details[1][:-1])
        val = (float(details[0][1:].replace(',','')))
        para = soup.find('p',{ 'class': 'sc-71024e3e-0 sc-58c82cf9-1 ihXFUo iPawMI'})
        # print(para)
        color = (para.get('color'))
        if color == 'red':
            change =  -1* float(details[1][:-1])
        elif color == "green":
            change =  float(details[1][:-1])
        # price = details[0]
        # print(price)
        # print(change)


        coin_metric_table = soup.find('dl', {'class': 'sc-d1ede7e3-0 bwRagp coin-metrics-table'})
        for section in coin_metric_table.find_all('div', class_='sc-d1ede7e3-0 bwRagp'):
            metric_name = section.find('div', class_='sc-cd4f73ae-1 laHoVg').text.strip()
            metric_value = section.find('dd', class_='sc-d1ede7e3-0 hPHvUM base-text').text.strip()
            metric_rank = section.find('span',class_ = 'text slider-value rank-value')
            if metric_rank:
                metric_rank = metric_rank.text[1:]
            # print(metric_rank)
            if metric_name == 'Market cap':
                market_cap = float(metric_value.split('%')[1][1:].replace(',',''))
                market_cap_rank = float(metric_rank)
            elif metric_name == 'Volume (24h)':
                volume_24h = float(metric_value.split('%')[1][1:].replace(',',''))
                volume_rank = float(metric_rank)
            elif metric_name == 'Volume/Market cap (24h)':
                volume_market_cap_24h = float(metric_value.replace('%',''))
            elif metric_name == 'Circulating supply':
                circulating_supply = float(metric_value.split()[0].replace(',',''))
            elif metric_name == 'Total supply':
                total_supply = float(metric_value.split()[0].replace(',',''))
            elif metric_name == 'Max. supply':
                max_supply = metric_value
            elif metric_name == 'Fully diluted market cap':
                diluted_market_cap = float(metric_value[1:].replace(',',''))
            
            

        # Create the output structure
        task_data = {
            "coin": coin_name,
            "output": {
                "price": val,
                "price_change": change,
                "market_cap": market_cap,
                "volume": volume_24h,
                "volume_market_cap": volume_market_cap_24h,
                "circulating_supply": circulating_supply,
                "total_supply": total_supply,
            
                "diluted_market_cap": diluted_market_cap
            },
            "official_links": [{"name": key,"link": val}for key,val in official_link.items()],
            "socials": [{"name": key,"url": val} for key,val in social.items()],
        }

        # print(task_data)

        final_data = parse_data(soup=soup)

        return "The HTML file is working fine."
    except requests.HTTPError as http_err:
        return f'HTTP error occurred: {http_err}'
    except Exception as err:
        return f'Other error occurred: {err}'
    
print(check_html_file('https://coinmarketcap.com/currencies/bitcoin/')) 