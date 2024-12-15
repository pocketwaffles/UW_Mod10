import pandas as pd
import re
import json
from flask import Flask, render_template

df_csv = pd.read_csv("crunchbase_odm_orgs.csv")

#Setting up a dataframe removing rows that meet both the condition of None in name and "company" in primary role
df = df_csv[~((df_csv['name'].isna()) & (df_csv['primary_role'] == 'company'))]

df_csv = pd.read_csv("crunchbase_odm_orgs.csv")

#Setting up a dataframe removing rows that meet both the condition of None in name and "company" in primary role
df_USA = df_csv[df_csv['country_code'] == "USA"]
df_sort = df_USA[df_USA['name'].str.contains(r'^Ac')]


#Importing data from CSV to dataframe
df_csv = pd.read_csv("crunchbase_odm_orgs.csv")
#Converting dataframe into json object
json_str = df_csv.to_json(orient='records')
#loading data into list of dictionaries
json_objects = json.loads(json_str)
#count the number of items in list
num_objects = len(json_objects)

#Creating text file with json objects
with open("data.txt", "w") as f:
    json.dump(json_objects, f)

with open('data.txt', 'r') as f:
    json_data = json.load(f)
    # converting data into dataframe
df = pd.DataFrame(json_data)
# filtering the items into a new "NYC only" data frame
df_NYC = df[df['city'] == "New York"]

#Creating json file for crunchbase companies
with open("crunchbase.json", "w") as f:
    json.dump(json_objects, f)

app = Flask("query")
#loading json data into its own variable
with open("crunchbase.json", "r") as f:
    data = json.load(f)
#setting up app to search the json data by city
@app.route('/search_by_city')
def search_by_city():
    query = request.args.get('query')
    if query:
        results = []
        for item in data:
            # Check if 'city' exists and is not None
            if 'city' in item and item['city']:
                if query.lower() == item['city'].lower():
                    results.append(item['name'])
        return jsonify(results)
    else:
        return jsonify({'error': 'No city parameter provided'}), 400

