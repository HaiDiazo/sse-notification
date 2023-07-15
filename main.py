from fastapi import FastAPI
from router import queue
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])


@app.get('/', include_in_schema=False)
def redirect():
    return RedirectResponse('/docs')


app.include_router(queue.app, prefix="/queue", tags=['Queue'])
