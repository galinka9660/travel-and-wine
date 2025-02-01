from openai import OpenAI
import os

def open_file(file_path):
    with open(file_path, "r") as file:
        return file.read()


def write_file(file_path, content):
    with open(file_path, "w") as file:
        file.write(content)

system_path = os.path.join("prompts", "system.txt")
query_path = os.path.join("prompts", "query.txt")

system = open_file(system_path)
query = open_file(query_path)

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system", 
            "content": system
        },
        {
            "role": "user",
            "content": query
        }
    ]
)

write_to = os.path.join("responses", "countries_wineyards.txt")
write_file(write_to, completion.choices[0].message.content)