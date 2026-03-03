# Validator agent logic
import yaml
from openai import OpenAI

class QueryValidator:
    def __init__(self, model="gpt-4o"):
        self.client = OpenAI()
        with open("prompt.yaml", "r") as f:
            self.prompts = yaml.safe_load(f)

    def validate(self, generated_sql):
        system_msg = self.prompts['query_validator']['system_message'].format(
            generated_sql=generated_sql
        )
        
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": system_msg}],
            temperature=0
        )
        
        result = response.choices[0].message.content.strip()
        return result # Expected to be "VALID" or an error explanation