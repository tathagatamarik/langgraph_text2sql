# Generator agent logic
import yaml
from openai import OpenAI
from database.schema import get_db_schema

class QueryGenerator:
    def __init__(self, model="gpt-4o"):
        self.client = OpenAI() # Assumes OPENAI_API_KEY in .env
        with open("prompt.yaml", "r") as f:
            self.prompts = yaml.safe_load(f)

    def generate(self, user_query, feedback=None):
        schema_info = get_db_schema()
        system_msg = self.prompts['query_generator']['system_message'].format(
            schema_info=schema_info
        )
        
        # If this is a retry, append the feedback from the Validator
        user_content = user_query
        if feedback:
            user_content = f"Your previous SQL failed. Feedback: {feedback}\nUser Question: {user_query}"

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_content}
            ],
            temperature=0
        )
        return response.choices[0].message.content.strip()