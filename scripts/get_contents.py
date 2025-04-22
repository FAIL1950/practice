from libs.context import ProcessingContextManager
from libs.storage import MyStorage
from services.llm import LLM

def main(ctx, for_rest = False, text = ""):
    ctx.log_msg(True)
    storage = None
    if not for_rest:
        storage = MyStorage(ctx)
        text = storage.get_text()
    llm = LLM(ctx)
    response_text, section_count = llm.get_contents_and_theses(text)
    if not for_rest:
        storage.save_res(response_text)
    ctx.logger.info(f"Count of sections: {section_count}")
    ctx.log_msg(False)
    return response_text

if __name__ == '__main__':
    with ProcessingContextManager() as ctx:
        main(ctx)