import json
from bs4 import BeautifulSoup
import requests

# Create an empty list to store ingredient data
ingredient_data = []

# Loop through page numbers from 0 to 100
for page_number in range(1):
    # Specify the URL of the webpage to scrape
    url = f'https://foodsubs.com/groups?page.number={page_number}&page.size=40&i=true'

    # Send an HTTP GET request to the webpage
    response = requests.get(url)

    # Create BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all <a> tags with class "card-title"
    a_tags = soup.find_all('a', class_='card-title')

    # Extract href values from the <a> tags and append them to the list
    href_list = [tag['href'] for tag in a_tags]

    # Additional URL
    ingredient_urls = ['https://foodsubs.com' + h_list for h_list in href_list]

    for website in ingredient_urls:
        result = requests.get(website)
        content = result.text
        soup = BeautifulSoup(content, 'html.parser')

        box = soup.find(class_='ingredient')
        main_ingredient = box.find('h1').get_text() if box else ''

        divs = soup.select('.ingredient p') if box else []
        description = ' '.join([div.get_text(' ') for div in divs])

        box1 = soup.find(class_='ingredients-table-wrapper sortable-table')
        divs1 = box1.find_all('div') if box1 else []
        nutritional_table = ' '.join([div1.get_text(' ') for div1 in divs1 if 'col-md-3' in div1.get('class', []) and 'sub-details' in div1.get('class', [])])

        box2 = soup.find(class_='img-thumbnail d-flex align-items-center bg-white')
        imgs2 = box2.find_all('img') if box2 else []
        image_location = ' '.join([img2['src'] for img2 in imgs2])

        # Remove unwanted content information from nutritional_table
        nutritional_table = nutritional_table.strip()

        # Create an ingredient object
        ingredient_obj = {
            'main_ingredient': main_ingredient,
            'description': description,
            'nutritional_table': nutritional_table,
            'image_location': image_location
        }

        # Append ingredient object to the list
        ingredient_data.append(ingredient_obj)

# Save ingredient data to a JSON file
with open('ingredients_combined.json', 'w', encoding='utf-8') as file:
    json.dump(ingredient_data, file, ensure_ascii=False, indent=4)
