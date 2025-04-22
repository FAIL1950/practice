from fastapi import FastAPI
from pydantic import BaseModel
from starlette.concurrency import run_in_threadpool
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import os

from scripts.get_contents import main as contents_main
from scripts.get_summary import main as summary_main
from libs.context import ProcessingContextManager


@asynccontextmanager
async def lifespan(app: FastAPI):
    with ProcessingContextManager() as ctx:
        ctx.another_log_msg("FastAPI server started.")
        yield
        ctx.another_log_msg("FastAPI server shutdown.")

app = FastAPI(lifespan=lifespan)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB_DIR = os.path.join(BASE_DIR, "web")

class TextRequest(BaseModel):
    text: str

def run_summary_with_context(text):
    with ProcessingContextManager() as ctx:
        ctx.another_log_msg("Received summary request.")
        result = summary_main(ctx, True, text)
        ctx.another_log_msg("Summary successfully generated.")
        return result

def run_content_with_context(text):
    with ProcessingContextManager() as ctx:
        ctx.another_log_msg("Received contents & theses request.")
        result = contents_main(ctx, True, text)
        ctx.another_log_msg("Contents & theses successfully generated.")
        return result
@app.get("/")
async def root():
    with ProcessingContextManager() as ctx:
        ctx.another_log_msg("Sending main page: index.html")
        fl_response = FileResponse(os.path.join(WEB_DIR, "index.html"))
        ctx.another_log_msg("index.html successfully sent.")
        return fl_response

@app.post("/api/v1/get_summary")
async def get_summary(request: TextRequest):
    result = await run_in_threadpool(run_summary_with_context, request.text)
    return {"summary": result}

@app.post("/api/v1/get_contents_and_theses")
async def get_contents_and_theses(request: TextRequest):
    result = await run_in_threadpool(run_content_with_context, request.text)
    return {"contents_and_theses": result}

