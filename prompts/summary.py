def get_summary_prompt(text: str):
    return [
        {
            "role": "system",
            "content": "You are a helpful assistant that creates clear and concise summaries of documents."
        },
        {
            "role": "user",
            "content": f"""Summarize the key ideas of the following document.

Your summary should:
- Identify the main topic.
- Highlight the core findings or arguments.
- Mention any relevant data, sources, or recommendations if available.
- Be 3–5 sentences long, clear, and professional.
- Do not use markdown symbols such as **, __, ## or similar formatting.
- Write the summary in the same language as the original document.


Document:
{text}"""
        }
    ]
