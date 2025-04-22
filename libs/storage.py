import os

class MyStorage:
    def __init__(self, ctx):
        self.ctx = ctx
        self.PATH_INPUT_FILE = os.getenv("PATH_INPUT_FILE")
        self.PATH_RESULT_FILE = os.getenv("PATH_RESULT_FILE")

    def get_text(self):
        self.ctx.log_msg(True)
        with open(os.getenv("PATH_INPUT_FILE"), "r", encoding="utf-8") as file:
            text = file.read()
        self.ctx.another_log_msg("Input file was read successfully")
        self.ctx.log_msg(False)
        return text

    def save_res(self, text):
        self.ctx.log_msg(True)
        with open(os.getenv("PATH_RESULT_FILE"), "w", encoding="utf-8") as file:
            file.write(text)
        self.ctx.another_log_msg("Output file was written successfully")
        self.ctx.log_msg(False)