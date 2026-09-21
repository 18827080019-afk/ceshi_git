from openai import OpenAI
import json


class LLM:

    def __init__(self,api_key,base_url,model):
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.model=model



    def chat(self,messages):
        response=self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )

        text=response.choices[0].message.content


        try:
            return json.loads(text)

        except json.JSONDecodeError:
            return text

   