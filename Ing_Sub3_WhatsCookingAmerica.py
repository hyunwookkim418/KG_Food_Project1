import csv
import json
import re

csv_file_path = 'C:\\Users\\hwkim\\GitHub_work\\KG_Food_Project1\\KG_Food_Data_Websites\\Ing_Sub3.csv'
json_file_path = 'C:\\Users\\hwkim\\GitHub_work\\KG_Food_Project1\\Ing_Sub3_WhatsCookingAmerica.json'


def separate_substitution(data):
    result = []
    words = data.split(' ')
    i = 0
    while i < len(words):
        if re.match(r'^\d+(\.\d+)?(/(\d+))?$', words[i]):
            quantity = words[i]
            if '/' in words[i]:
                fraction_match = re.match(r'(\d+)/(\d+)', words[i])
                if fraction_match:
                    numerator = int(fraction_match.group(1))
                    denominator = int(fraction_match.group(2))
                    quantity = numerator / denominator

                fraction_match = re.match(r'(\d+)\s+(\d+)/(\d+)', words[i])
                if fraction_match:
                    whole_number = int(fraction_match.group(1))
                    numerator = int(fraction_match.group(2))
                    denominator = int(fraction_match.group(3))
                    quantity = whole_number + (numerator / denominator)

            unit = ''
            if i + 1 < len(words):
                unit = words[i + 1].strip('.').lower()

            ingredient_name = ''
            if i + 2 < len(words):
                ingredient_name = ' '.join(words[i + 2:]).lower()

            result.append({'quantity': quantity, 'unit': unit, 'ingredient_name': ingredient_name})

            break

        i += 1

    return result


data = []

with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        ingredient = row['Ingredient']
        amount = row['Amount']
        substitute = row['Substitute']
        source = "WhatsCookingAmerica (https://whatscookingamerica.net/information/ingredientsubstitution.htm)"

        amount_data = []
        if len(amount.split()) >= 2:
            quantity = amount.split()[0]
            if re.match(r'^\d+(\.\d+)?(/(\d+))?$', quantity):
                if '/' in quantity:
                    numerator, denominator = quantity.split('/')
                    quantity = float(numerator) / float(denominator)
                else:
                    quantity = float(quantity)
                unit = amount.split()[1].strip('.')
                amount_data.append({"quantity": quantity, "unit": unit})

        substitute_data = []
        if substitute:
            substitute_ingredients = substitute.split(' and ')
            for ingredient_data in substitute_ingredients:
                if ',' in ingredient_data:
                    ingredient_pairs = ingredient_data.split(',')
                    for pair in ingredient_pairs:
                        ingredient_info = separate_substitution(pair)
                        if ingredient_info:
                            substitute_quantity = float(ingredient_info[0]['quantity'])
                            substitute_unit = ingredient_info[0]['unit']
                            substitute_name = ingredient_info[0]['ingredient_name']
                            substitute_data.append(
                                {"quantity": substitute_quantity, "unit": substitute_unit,
                                 "ingredient_name": substitute_name})
                    if 'and' in ingredient_data and len(ingredient_pairs) > 1:
                        substitute_data.append({"and": "and"})
                else:
                    ingredient_info = separate_substitution(ingredient_data)
                    if ingredient_info:
                        substitute_quantity = float(ingredient_info[0]['quantity'])
                        substitute_unit = ingredient_info[0]['unit']
                        substitute_name = ingredient_info[0]['ingredient_name']
                        substitute_data.append(
                            {"quantity": substitute_quantity, "unit": substitute_unit,
                             "ingredient_name": substitute_name})

        entry = {"Ingredient": ingredient, "Description" : " ", "Amount": amount_data, "Substitute": substitute_data, "Image_location": " ", "Source": source}
        data.append(entry)

with open(json_file_path, 'w') as json_file:
    json.dump(data, json_file, indent=4)

print("CSV file converted to JSON successfully.")
