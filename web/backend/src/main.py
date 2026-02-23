from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def get_hello():
    return {"text": "Hello, NOZERO!"}
