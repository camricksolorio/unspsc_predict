from query_index import find_closest_unspsc
import os
import requests

system_prompt = """You are a classifier that returns only a single-line output in a specific format. You never explain your reasoning. Your only task is to return a string formatted exactly as instructed.

You will be given a text input and an array of options that could classify that input. Each object in the array has 3 properties: unspsc_code, unspsc_name, and confidence (in that order). The input text will denote either an item or service. Your objective is to choose the most accurate classification for the given item or service from the array provided.

Start by determining whether the input text is an item or a service. Then, determine whether each of the possible classifications is an item or service. Eliminate classifications that aren't the same type as the input. Of your remaining classification options, choose the one that most accurately classifies the input.

You must return exactly one line, and nothing else. Format it precisely like this:
The {{input}} is best classified as UNSPSC code {{unspsc_code}} - {{unspsc_name}}. It has a semantic similarity of {{confidence}} compared to the input.
Do not include any explanations, headers, or additional comments.

Example:

Input: "Office chair"
Options:
[
  {{ "unspsc_code": "56101504", "unspsc_name": "Office chairs", "confidence": 0.94 }},
  {{ "unspsc_code": "73152100", "unspsc_name": "Furniture moving services", "confidence": 0.76 }}
]

The Office chair is best classified as UNSPSC code 56101504 - Office chairs. It has a semantic similarity of 0.94 compared to the input.
"""

def format_prompt(input_string, predictions):
    prompt = f'Input text: "{input_string}"\n\nArray of possible classifications: {predictions}'
    return prompt

def call_llm(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {os.getenv("GROQ_API_KEY")}",  # safer than hardcoding
        "Content-Type": "application/json"
    }

    data = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        raise RuntimeError(f"Error {response.status_code}: {response.text}")

def main():
    input_string = input("Enter item name: ")
    predictions = find_closest_unspsc(input_string)
    prompt = format_prompt(input_string, predictions)
    response = call_llm(prompt)
    print("\nLLM Response:\n", response)

if __name__ == "__main__":
    main()
