import openai

from resources.constants_loader import load_constants

constants = load_constants()

openai.api_key = constants.get("API", "OPENAI")
print(openai.Model.list())

completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": "Hello!"}
  ]
)

print(completion.choices[0].message["content"])
