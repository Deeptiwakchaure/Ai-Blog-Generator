from huggingface_hub import InferenceClient
import time

class BlogWriter:
    def __init__(self, model_name="mistralai/Mistral-7B-Instruct-v0.2", api_token=None):
        self.model_name = model_name
        self.client = InferenceClient(
            model=model_name,
            token=api_token,
            timeout=120
        )

    def write(self, topic):
        """Generate a blog post using chat completion API with retries."""
        system_message = """You are a professional blog writer. Write comprehensive, engaging blog posts that include:
        - An attention-grabbing introduction
        - 3-5 key points with descriptive subheadings
        - Practical examples or insights
        - A strong conclusion with a call-to-action
        Format everything in proper Markdown."""
        
        user_message = f"Write a detailed blog post about {topic}."
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.client.chat_completion(
                    messages,
                    max_tokens=2048,
                    temperature=0.7,
                    top_p=0.9,
                )
                return response.choices[0].message['content']
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(2)  # Wait before retrying
                    continue
                return f"Error generating blog: {str(e)}\n\nThis model might not support chat completion. Try a different model."