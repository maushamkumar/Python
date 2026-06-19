from openai import OpenAI

client = OpenAI(api_key="OpenAI API key")

response = client.responses.create(
    model="gpt-5.2",
    input="what is python?"
)

print(response.output_text)


