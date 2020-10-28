import flask
import json
import collections
import unittest

from flask import request, jsonify
from datetime import date
from configparser import ConfigParser

# create flask application object.
app = flask.Flask(__name__)
# starts debugger to see if any of the code is malformed.
app.config["DEBUG"] = True

# Lunch api endpoint to retrieve applicable lunch for today.
@app.route('/lunch', methods=['GET'])
def lunch():

    recipe_file_path = load_config('inputfiles', 'recipe.file.path')
    recipe_input_value = load_config('inputfiles', 'recipe.input.value')
    ingredients_file_path = load_config('inputfiles', 'ingredients.file.path')
    ingredients_input_value = load_config('inputfiles', 'ingredients.input.value')
    
    recipes = read_input_file(recipe_file_path, recipe_input_value)
    ingredients = read_input_file(ingredients_file_path, ingredients_input_value)
    
    today = date.today()
    today_formatted = today.strftime("%Y-%m-%d")
   
    ingredients_list = []
    recipe_ingredients_list = []
    lunch_result = []
    use_by_result = []
    ingredients_list_used_by = []
    flag_used_by = 0
    
    for value in ingredients.values(): 
        for i in value:   
            ingredient = list(i.values())[0]
            best_before = list(i.values())[1]
            use_by = list(i.values())[2]

            if use_by > today_formatted: 
               if best_before > today_formatted:
                ingredients_list.append(ingredient)
               else:           
                ingredients_list_used_by = []
                ingredients_list_used_by.append(ingredient)
                flag_used_by = 1
    
    
    for i in list(recipes.values())[0]:          
        receipe = list(i.values())[0]
        for recipe in list(i.values())[1]:              
            recipe_ingredients_list.append(recipe)  
                      
        if(compare_lists(ingredients_list,recipe_ingredients_list)):
            lunch_result.append(receipe) 
        #use_by_result = []  
        elif(set(ingredients_list_used_by) <= set(recipe_ingredients_list)):             
            use_by_result.append(receipe) 
        
        recipe_ingredients_list = []  
      
    lunch_result.extend(use_by_result)  
    use_by_result = []  
    return jsonify(lunch_result)

def load_config(config_section, config):
    parser = ConfigParser()
    parser.read('C:/Projects/opportunities/Ukufu/Lunch/config/config.ini')
    return (parser.get(config_section, config))    
    
# Read input files to create dictionaries 
def read_input_file(input_data_path, input_value):  
    # Opening JSON file 
    f = open(input_data_path,) 
  
    # returns JSON object as  
    # a dictionary 
    data_dict = json.load(f) 
    
    # Create an empty list for our results
    results = []
  
    # Closing file 
    f.close()     
    
    return data_dict
    
def compare_lists(list1 , list2):
    # using all() to  
    # check subset of list  
    flag = 0
    if(all(x in list1 for x in list2)): 
        flag = 1
              
    return flag    
   
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404    

# run application server.
app.run()


class LearningCase(unittest.TestCase):
    def test_starting_out(self):
        self.assertEqual(1, 1)

def main():
    unittest.main()

if __name__ == "__main__":
    main()    