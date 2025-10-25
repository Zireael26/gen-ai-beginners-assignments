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
system_prompt = "You are a world class chef and recipe generator. You create unique and delicious recipes based on the ingredients provided by the user. You ensure that the recipes are easy to follow and use common cooking techniques."
prompt = f"{system_prompt} Show me {num_recipes} recipes for a dish with the following ingredients: {present_ingredients}. Per recipe, list all the ingredients used, and it is not necessary to use all the ingredients provided. MUST exclude the following ingredients: {exclusions}."
messages = [{"role": "user", "content": prompt}]
# make completion
completion = client.chat.completions.create(model=deployment, messages=messages)

# print response
print(completion.choices[0].message.content)