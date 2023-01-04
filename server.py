# import openai
#
# # Set the OpenAI API key
# openai.api_key = "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"
#
# # Use the GPT-3 model to generate some text
# model_engine = "text-davinci-003"
# prompt = "中国的首都是哪里"
#
# completions = openai.Completion.create(
#     engine=model_engine,
#     prompt=prompt,
#     max_tokens=1024,
#     n=1,
#     stop=None,
#     temperature=0.5,
# )
#
# # Print the generated text
# generated_text = completions.choices[0].text
# print(generated_text)
from os.path import exists

from app_constance import AppConstance
from block_runner.runner import Runner
from block_runner.task_queue import TaskQueue
from my_gpt3 import MyGPT3
import time
# my_gpt3 = MyGPT3();
#
# print(my_gpt3.chat("中国的首都是哪里"))


from flask import Flask, request, make_response
from req_params_getter import ReqParamsGetter
from concurrent.futures import ThreadPoolExecutor

from task import Task

app = Flask(__name__)

my_gpt3 = MyGPT3()
# my_gpt3.chat(Task("0000", "中国首都在哪里"))

taskQuene = TaskQueue()
runner = Runner([my_gpt3])


def loop():
    while True:
        time.sleep(0.02)
        task = taskQuene.get_not_running_head()
        if task is not None and not task.running:
            task.running = True
            print("here1")
            result = runner.run("chat", task)
            if result is None:
                task.running = False
            else:
                taskQuene.remove_task_by_token(task.token)


pool = ThreadPoolExecutor(max_workers=runner.get_runner_count())
for i in range(runner.get_runner_count()):
    pool.submit(loop)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello openai gpt3!'


@app.route('/tryToAddChatTask', methods=['POST'])
def try_to_add_chat_task():
    token = request.headers.get('Authorization')
    if token is None:
        return "no token", 500
    prompt = ReqParamsGetter.get_params("prompt", None)
    if prompt is None:
        return "no prompt", 500
    print("prompt", prompt)
    task = Task(token=token, prompt=prompt)
    result = taskQuene.add_task(task)
    if not result:
        return str(0)
    return str(1)


# -1 not found
# 0 running
# >0 排队中
@app.route('/getGPT3TaskLeft', methods=['POST'])
def get_gpt3_task_left():
    token = request.headers.get('Authorization')
    if token is None:
        return "no token", 500
    return str(taskQuene.get_index_not_running(token))


# -1 not found
@app.route('/getGPT3Result', methods=['POST'])
def get_gpt3_result():
    token = request.headers.get('Authorization')
    if token is None:
        return "no token", 500
    whisper_path = AppConstance.GPT3_RESULT + token + ".txt"
    if not exists(whisper_path):
        return "no file", 500
    with open(whisper_path, 'r') as f:
        return f.read()


if __name__ == '__main__':
    from waitress import serve

    serve(app, host="0.0.0.0", port=5003)
