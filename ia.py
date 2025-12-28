from openai import OpenAI

client = OpenAI()

def gerar_texto(prompt: str) -> str:
    resposta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Você é um assistente legislativo institucional, especializado em redação legislativa brasileira."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return resposta.choices[0].message.content.strip()
