class Tokens:
    def __init__(self):
        self.prompt_tokens = 0
        self.completion_tokens = 0

    def add_prompt_tokens(self, cnt):
        self.prompt_tokens += cnt

    def add_completion_tokens(self, cnt):
        self.completion_tokens += cnt

    def get_tokens(self):
        return self.prompt_tokens, self.completion_tokens, self.prompt_tokens + self.completion_tokens