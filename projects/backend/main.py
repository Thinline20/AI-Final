import uvicorn
from typing import Union
from fastapi import FastAPI

# from projects.lib.LibAI import process


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/stock/{stock_ticker}")
def read_ticker(stock_ticker: str):
    # return process(stock_ticker)
    pass
    


if __name__ == "__main__":
    uvicorn_config = uvicorn.Config("main:app", port=8000, log_level="info")
    server = uvicorn.Server(uvicorn_config)

    server.run()
