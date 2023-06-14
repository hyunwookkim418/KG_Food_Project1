from bs4 import BeautifulSoup
import requests

# Create an empty list to store href values
href_list = []

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
    href_list.extend([tag['href'] for tag in a_tags])

# Additional URL
ingredient_urls = ['https://foodsubs.com' + h_list for h_list in href_list]

combined_description = ''
combined_nutritional_table = ''

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
    nutritional_table = ' '.join([div1.get_text(' ') for div1 in divs1 if not any(['col-md-1' in class_str or 'col-md-fixed' in class_str for class_str in div1.get('class', [])])])

    # Remove unwanted content information from nutritional_table
    nutritional_table = nutritional_table.split(' Substitutes: ')[0]

    combined_description += f'{main_ingredient}\n{description}\n'
    combined_nutritional_table += f'{main_ingredient}\n{nutritional_table}\n'

with open('ingredients_combined.txt', 'w', encoding='utf-8') as file:
    file.write(combined_description + '\n' + combined_nutritional_table)
