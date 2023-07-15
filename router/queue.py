import time
import traceback

from sse_starlette.sse import EventSourceResponse
from service.consume import ConsumeService
from fastapi import APIRouter

app = APIRouter()


@app.get("/test-message")
async def data_queue():
    start_time = time.time()
    service = ConsumeService()
    finish_time = time.time() - start_time
    # payload = {
    #     'status_code': 200,
    #     'execution_time': finish_time,
    #     'message': 'success',
    #     'data': result
    # }
    return EventSourceResponse(service.consume())


