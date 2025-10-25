from openai import OpenAI
import os
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()

# configure OpenAI service client 
client = OpenAI()
deployment = "gpt-5-nano"

num_recipes = input("Enter number of recipes (exmaple: 5) to generate: ")
present_ingredients = input("Enter ingredients you have (example: bell peppers, potatoes, carrots, spring onions, red onions, garlic): ")
exclusions = input("Enter ingredients to exclude (example: meat, dairy, nuts): ")

# add your completion code
system_prompt = "You are a world class chef, nutritionist and recipe generator. " \
    "You create unique and delicious recipes based on the ingredients provided by the user." \
    "You ensure that the recipes are easy to follow and use common cooking techniques."
prompt = f"""{system_prompt} Show me {num_recipes} recipes for a dish with the following ingredients: {present_ingredients}. 
    Per recipe, list all the ingredients used, and it is not necessary to use all the ingredients provided. 
    Provide the nutritional information for each recipe generated above, including calories, protein, fat, carbohydrates, and fiber content per serving. 
    MUST exclude: {exclusions}."""
messages = [{"role": "user", "content": prompt}]
# make completion
completion = client.chat.completions.create(model=deployment, messages=messages)

print("\n")
print(completion.choices[0].message.content)

old_prompt_completion = completion.choices[0].message.content
additional_instructions = "Provide a shopping list for the recipes generated above, grouped by recipe. Do not include any ingredients I have at home." \
    "Include quantities and any special notes for each ingredient."
new_prompt = f"{old_prompt_completion}\n\n{additional_instructions}"
messages = [{"role": "user", "content": new_prompt}]

completion = client.chat.completions.create(model=deployment, messages=messages)
print("\n")
print(completion.choices[0].message.content)