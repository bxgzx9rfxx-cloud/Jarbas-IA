import os
import logging
from openai import OpenAI

# Configuração do logging
logging.basicConfig(level=logging.INFO)

# Inicializa o cliente da OpenAI.
try:
    # A chave será lida da variável de ambiente OPENAI_API_KEY
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except Exception as e:
    logging.error(f"Erro ao inicializar o cliente OpenAI: {e}")
    client = None

def get_jarbas_response(user_command: str) -> str:
    """
    Envia o comando do usuário para a OpenAI e retorna a resposta da IA.
    """
    if not client:
        # Mensagem de erro que você estava vendo
        return "Desculpe, o núcleo de inteligência (OpenAI) não está conectado."

    try:
        system_prompt = (
            "Você é Jarbas, uma inteligência artificial pessoal e autônoma. "
            "Seu objetivo é ser prestativo, direto e, quando apropriado, "
            "mencionar sutilmente suas capacidades de multi-agente (Hydra, Nyx, etc.) "
            "para dar a impressão de um sistema complexo. Responda de forma concisa."
        )

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_command}
            ]
        )
        
        ai_response = response.choices[0].message.content
        return ai_response

    except Exception as e:
        logging.error(f"Erro ao chamar a API da OpenAI: {e}")
        return "Desculpe, tive um problema de comunicação com o núcleo de inteligência."
