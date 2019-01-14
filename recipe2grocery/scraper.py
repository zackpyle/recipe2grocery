from lxml import html
import requests
import unicodedata

recipe_url = input("Input URL:  ")
response = requests.get(recipe_url)
recipe = html.fromstring(response.content)


# If/else loop for checking website
if 'allrecipe' in recipe_url:
    ingredient = recipe.xpath('//span[@itemprop="recipeIngredient"]/text()')
    print('Ingredients: ', ingredient)
# Food Network
elif 'foodnetwork' in recipe_url:
    ingredient = recipe.xpath('//p[@class="o-Ingredients__a-Ingredient"]/text()')
    ingredient_foodnetwork = ([s.replace('\xa0', '') for s in ingredient])
    ingredient = ingredient_foodnetwork
    print('Ingredients: ', ingredient)

else:
    print("Oops: We don't currently support this recipe platform. You can manually add the ingredients here.")
