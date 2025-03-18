import openai
import os
import config

token = os.getenv("TOKEN_OPENAI")
token = "sk-proj-" + token[:3:-1] if token.startswith("gpt:") else token
openai.api_key = token

class ChatGPTService:
    def __init__(self):
        self.message_history = []

    def set_system_message(self, content):
        self.message_history.append({"role": "system", "content": content})

    def add_user_message(self, user_content):
        self.message_history.append({"role": "user", "content": user_content})

    def add_assistant_message(self, content):
        self.message_history.append({"role": "assistant", "content": content})

    def get_response(self, model="gpt-3.5-turbo", temperature=0.7):
        response = openai.ChatCompletion.create(
            model=model,
            messages=self.message_history,
            temperature=temperature,
            max_tokens=1000
        )
        assistant_reply = response["choices"][0]["message"]["content"]
        self.add_assistant_message(assistant_reply)

        return assistant_reply

    def get_recommendation(self, category, genre, disliked_list):
        """Генерирует рекомендацию по категории и жанру"""
        prompt = f"Дай мне одну рекомендацию {category} в жанре {genre}. Не используй следующие: {', '.join(disliked_list)}."

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]