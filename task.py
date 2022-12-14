from block_runner.base_task import BaseTask


class Task(BaseTask):

    prompt = None

    def __init__(self, token: str, prompt: str):
        super().__init__(token)
        self.prompt = prompt
