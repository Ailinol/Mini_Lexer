from openai import OpenAI

client = OpenAI()

def suggest_with_llm(token, context="Pascal compiler"):
    prompt = f"""
You are a compiler assistant for Pascal language.

The user wrote a token that caused a lexical error.

Token: "{token}"

Task:
- Suggest the most likely correct token
- If it's a keyword mistake, fix it
- If it's invalid, explain briefly
Return only the correction suggestion.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content