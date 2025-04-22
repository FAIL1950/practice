import time
import inspect
from pathlib import Path
import traceback
from libs.logger import get_logger
from dotenv import load_dotenv
import os

from openai import OpenAIError

class ProcessingContextManager:
    def __init__(self, env_path:str = ""):
        if env_path == "":
            self.env_path = Path(__file__).parent.parent / "config.env"
        else:
            self.env_path = Path(env_path)
        self.buffer = []
        self.end = None

    def __enter__(self):
        load_dotenv(dotenv_path=self.env_path, override=True)
        log_file_path = Path(__file__).parent.parent / "logs" / "logs.log"
        log_file_path.parent.mkdir(parents=True, exist_ok=True)
        self.logger = get_logger("logs",log_file_path)
        self.logger.info("-- Start processing --")
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        if exc_type is None:
            self.logger.info("-- Successful end of processing --")
            self.end = time.time()
            self.print_statistics()
            return True

        if isinstance(exc_val, OpenAIError):
            return self._handle_openai_error(type(exc_val).__name__, exc_val, exc_type, exc_tb)

        non_critical = (ValueError, TypeError, ZeroDivisionError, FileNotFoundError)

        if issubclass(exc_type, non_critical):

            self.logger.error(f"Non critical error: {exc_type.__name__} - {exc_val}")
            print(f"Non critical error: {exc_type.__name__} - {exc_val}. Watch logs for more info.")
            self.logger.error(''.join(traceback.format_exception(exc_type, exc_val, exc_tb)))
            self.print_statistics()
            return True


        self.logger.error(f"Critical error: {exc_type.__name__} - {exc_val}")
        print(f"Critical error: {exc_type.__name__} - {exc_val}. Watch logs for more info.")
        self.logger.error(''.join(traceback.format_exception(exc_type, exc_val, exc_tb)))
        self.print_statistics()
        return False

    def log_msg(self, isbegin:bool):
        caller_frame = inspect.currentframe().f_back
        caller_name = caller_frame.f_code.co_name
        caller_file = os.path.basename(caller_frame.f_code.co_filename)
        if isbegin:
            self.logger.info(f"{caller_file}: {caller_name}() BEGIN")
        else:
            self.logger.info(f"{caller_file}: {caller_name}() END")

    def another_log_msg(self, text: str):
        caller_frame = inspect.currentframe().f_back
        caller_name = caller_frame.f_code.co_name
        caller_file = os.path.basename(caller_frame.f_code.co_filename)

        self.logger.info(f"{caller_file}: {caller_name} - {text}")

    def add_to_buffer(self, msg:str):
        self.buffer.append(msg)

    def print_statistics(self):
        self.logger.info("-- Statistics --")
        print("-- Statistics --")
        for i in range(len(self.buffer)):
            self.logger.info(self.buffer[i])
            print(self.buffer[i])
        self.end = time.time()
        diff = self.end - self.start_time
        self.logger.info("Work time: %.2f seconds\n", diff)
        print("Work time: %.2f seconds\n" % diff)

    def _handle_openai_error(self, error_type_name: str, exc_val, exc_type, exc_tb):
        self.logger.error(f"OpenAI {error_type_name}: {exc_val}")
        print(f"OpenAI {error_type_name}. Try again. Watch logs for more info.")
        self.logger.error(''.join(traceback.format_exception(exc_type, exc_val, exc_tb)))
        self.print_statistics()
        return True
