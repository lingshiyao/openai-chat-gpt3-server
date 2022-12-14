import openai

from app_constance import AppConstance
from block_runner.base import Base
from task import Task

# Set the OpenAI API key
openai.api_key = "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"

# Use the GPT-3 model to generate some text
model_engine = "text-davinci-003"


class MyGPT3(Base):

    def chat(self, task: Task):
        if self.lock:
            return None
        else:
            self.lock = True
            print("start")
            completions = openai.Completion.create(
                engine=model_engine,
                prompt=task.prompt,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.5,
            )
            generated_text = completions.choices[0].text
            print(generated_text)
            with open(AppConstance.GPT3_RESULT + task.token + ".txt", "w") as f:
                f.write(generated_text)
            self.lock = False
            return AppConstance.GPT3_RESULT + task.token + ".txt"
