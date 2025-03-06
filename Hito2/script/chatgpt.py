from openai import OpenAI
import os

client = OpenAI(api_key='')

# Definir el ID del asistente
assistant_id = "asst_68M0vY8lXyoaic1GNOcHWFdS"


def mandarImagen(i):
    try:
        thread = client.beta.threads.create()

        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=[
                {
                    "type": "image_url",
                    "image_url": {"url": f"https://raw.githubusercontent.com/alenavarroxp/DISIA/refs/heads/main/Hito2/sin_procesar/{i}.jpg"}
                },
                {
                    "type": "text",
                    "text": "Por favor, proporciona solo 'Transitable' o 'No Transitable' además de 'Inundado' o 'No inundado'. Mucha gente depende de tu decisión, piensa antes de hablar."
                }
            ],
        )
        run_response = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
        )

        run_id = run_response.id
        status = run_response.status

        while status not in ["completed", "failed", "cancelled"]:
            run_response = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run_id)
            status = run_response.status

        if status == "failed":
            print("Error: El asistente no pudo procesar la imagen.")
        elif status == "completed":
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            for message in reversed(messages.data):
                if message.role == "assistant":
                    print(f"Img {i}: {message.content[0].text.value}")
                    break
        else:
            print(f"Estado final inesperado: {status}")

    except Exception as e:
        print(f"Error en la ejecución: {str(e)}")

for i in range(50):
    mandarImagen(i+1)
