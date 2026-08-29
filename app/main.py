from fastapi import FastAPI

from .routers import wallets

app = FastAPI()
app.include_router(wallets.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
