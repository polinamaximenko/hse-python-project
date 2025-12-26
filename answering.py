import ollama

SYSTEM_PROMPT = """\
Ты — ассистент для ответов на вопросы по документам.

Правила:
- Используй ТОЛЬКО предоставленный контекст
- Не добавляй внешние знания
- Если ответа нет в контексте — скажи:
  "Ответ на этот вопрос не найден в предоставленном документе"
- Пиши кратко, структурировано и по существу
"""

class AnswerFormatter:
    def __init__(self, model: str = "gpt-oss:120b-cloud"):
        self.model = model

    def generate_answer(self, query: str, context: str) -> str:
        """Generate an answer based on the query and provided context."""
        if not context.strip():
            return "Ответ на этот вопрос не найден в предоставленном документе"
        
        user_message = f"""\
        Вопрос:
        {query}

        Контекст:
        {context}

        Ответь на вопрос, опираясь ТОЛЬКО на предоставленный контекст.
        """

        response = ollama.chat(model=self.model, messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_message
                }
        ])
        return response['message']['content']

    
if __name__ == "__main__":
    pass
