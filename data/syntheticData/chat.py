import openai

class Chat:
    def __init__(self, model, temperature) -> None:
        self.model = model
        self.temperature = temperature
    
    def get_completion(self, prompt):
        message = [{"role": "user", "content": prompt}]
        response = openai.chat.completions.create(
            model = self.model,
            messages = message,
            temperature = self.temperature
        )
        return response.choices[0].message.content
    
    def chat(self, messages):
        response = openai.chat.completions.create(
            model = self.model,
            messages = messages,
            temperature = self.temperature
        )
        return response.choices[0].message.content