from openai import OpenAI
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()

# configure OpenAI service client 
client = OpenAI()
deployment = "gpt-5-nano"

# add your completion code
system_prompt = "You are a helpful and knowledgeable study buddy, and you have particular expertise in generative AI. " \
    "You explain complex concepts in simple terms, provide relevant examples, and suggest useful resources for further learning."

topic = input("Enter a topic you want to learn about (example: Retrieval Augmented Generation): ")
prompt = f"""{system_prompt} Suggest a beginner lesson for {topic} in the following format:
    Format:
        - concepts:
        - brief explanation of the lesson:
        - exercise in code with solutions:
    """
messages = [{"role": "user", "content": prompt}]
# make completion
completion = client.chat.completions.create(model=deployment, messages=messages)

# print response
print(completion.choices[0].message.content)