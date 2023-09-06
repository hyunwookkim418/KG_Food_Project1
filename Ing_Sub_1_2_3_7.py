import json
import glob

#3920 with duplicates (148)

output_file_path = 'Ing_Sub_1_2_3_7.json'
input_files = [
    'C:\\Users\\hwkim\\GitHub_work\\KG_Food_Project1\\Ing_Sub1_theSpruceEats.json',
    'C:\\Users\\hwkim\\GitHub_work\\KG_Food_Project1\\Ing_Sub2_allrecipes.json',
    'C:\\Users\\hwkim\\GitHub_work\\KG_Food_Project1\\Ing_Sub3_WhatsCookingAmerica.json',
    'C:\\Users\\hwkim\\GitHub_work\\KG_Food_Project1\\Ing_Sub7_FoodSub.json'
]

combined_data = []

# Iterate over the input files
for file_path in input_files:
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        combined_data.extend(data)

# Sort the combined data based on the "Ingredient" field
combined_data.sort(key=lambda item: item.get("Ingredient", ""))

# Write the combined and sorted data to the output file
with open(output_file_path, 'w') as json_file:
    json.dump(combined_data, json_file, indent=4)

print("JSON files combined and sorted successfully.")
