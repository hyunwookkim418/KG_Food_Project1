import json
import glob

output_file_path = 'combined.json'
input_files = [
    'C:\\Users\\hwkim\\OneDrive\\바탕 화면\\Ingredient_Substitution_AI\\KG_Food_Project_Revathy\\Ing_Sub1.json',
    'C:\\Users\\hwkim\\OneDrive\\바탕 화면\\Ingredient_Substitution_AI\\KG_Food_Project_Revathy\\Ing_Sub2.json',
    'C:\\Users\\hwkim\\OneDrive\\바탕 화면\\Ingredient_Substitution_AI\\KG_Food_Project_Revathy\\Ing_Sub3.json',
    'C:\\Users\\hwkim\\OneDrive\\바탕 화면\\Ingredient_Substitution_AI\\KG_Food_Project_Revathy\\FoodSub_Dictionary1.json'
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
