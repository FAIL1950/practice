import os
from openai import OpenAI
from prompts.summary import get_summary_prompt
from prompts.contents import generate_toc, count_sections, gen_theses
from libs.tokens import Tokens

class LLM:
    def __init__(self, ctx):
        self.tokens = Tokens()
        self.ctx = ctx
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def __del__(self):
        prompt_tokens, completion_tokens, total_tokens = self.tokens.get_tokens()
        self.ctx.add_to_buffer(f"Prompt tokens: {prompt_tokens}")
        self.ctx.add_to_buffer(f"Completion tokens: {completion_tokens}")
        self.ctx.add_to_buffer(f"Total tokens: {total_tokens}")

    def generate_summary(self, text: str):
        self.ctx.log_msg(True)
        message = get_summary_prompt(text)
        self.ctx.another_log_msg("Send request to OpenAI.")
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=message
        )
        self.ctx.another_log_msg("Successfully received response from OpenAI.")
        response_text = response.choices[0].message.content
        self.tokens.add_prompt_tokens(response.usage.prompt_tokens)
        self.tokens.add_completion_tokens(response.usage.completion_tokens)
        self.ctx.log_msg(False)
        return response_text

    def get_contents_and_theses(self, text: str):
        self.ctx.log_msg(True)
        self.ctx.another_log_msg("Send request to OpenAI.")
        toc_response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=generate_toc(text)
        )
        self.ctx.another_log_msg("Successfully received response from OpenAI.")
        self.tokens.add_prompt_tokens(toc_response.usage.prompt_tokens)
        self.tokens.add_completion_tokens(toc_response.usage.completion_tokens)
        toc = toc_response.choices[0].message.content

        self.ctx.another_log_msg("Send request to OpenAI.")
        count_response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=count_sections(toc)
        )
        self.ctx.another_log_msg("Successfully received response from OpenAI.")
        self.tokens.add_prompt_tokens(count_response.usage.prompt_tokens)
        self.tokens.add_completion_tokens(count_response.usage.completion_tokens)
        section_count = int(count_response.choices[0].message.content)

        self.ctx.another_log_msg("Send request to OpenAI.")
        theses_response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=gen_theses(toc, text)
        )
        self.ctx.another_log_msg("Successfully received response from OpenAI.")
        self.tokens.add_prompt_tokens(theses_response.usage.prompt_tokens)
        self.tokens.add_completion_tokens(theses_response.usage.completion_tokens)
        theses = theses_response.choices[0].message.content
        self.ctx.log_msg(False)
        return theses, section_count

