from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

# chat_response = client.responses.create(
#     model="gpt-5-nano",
#     instructions="You are an educator with expertise in simplifying complex topics.",
#     input="Explain the theory of relativity.",
#     reasoning={
#         "effort": "minimal",
#     },
# )

# print(chat_response.output_text)

chat_stream = client.responses.create(
    model="gpt-5-nano",
    instructions="You are an educator with expertise in simplifying complex topics.",
    input="Explain the theory of relativity.",
    reasoning={
        "effort": "minimal",
    },
    stream=True
)

for event in chat_stream:
    # print(event)  # Print the full event for debugging
    if event.type == 'response.output_text.delta':
        print(event.delta, end='', flush=True)