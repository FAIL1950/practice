def generate_toc(text: str):
    messages = [
        {"role": "system", "content": "You are an expert document analyst."},
        {"role": "user", "content": f"""You will be given a document in an unknown language.             

    Your task is:
    1. Analyze the content and automatically detect the language.
    2. Generate a **structured table of contents** for the entire document.
    3. Format the output as a clear numbered list with sections and subsections (e.g. 1, 2, 2.1, etc.).
    4. Do not use markdown symbols such as **, __, ## or similar formatting.
    5. Respond **in the same language** as the input document.
    

    Document:
    {text}
    """}
    ]
    return messages

def count_sections(text: str):
    messages = [
        {"role": "system", "content": "You are a helpful assistant that logs structured information."},
        {"role": "user", "content": f"""You will be given a previously generated **table of contents**.

    Your task is:
    1. Count how many **main sections** are in the table of contents.
    2. Log only the total number — just return the number, nothing else.
    3. Do not use markdown symbols such as **, __, ## or similar formatting.
    4. Respond **in the same language** as the document.

    Table of Contents:
    {text}
    """}
    ]
    return messages

def gen_theses(toc: str, text: str):
    messages = [
        {"role": "system", "content": "You are a precise analyst of documents."},
        {"role": "user", "content": f"""You will now analyze the document section by section, using the following previously generated **table of contents**:
    {toc}

    Your task is:
    1. For each section or subsection in the table of contents, extract **2–3 key theses or quotations**.
    2. Use direct quotes where possible.
    3. Do not use markdown symbols such as **, __, ## or similar formatting.
    4. Respond **in the same language as the document**.

    Document:
    {text}
    """}
    ]
    return messages