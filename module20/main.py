from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}
@app.get("/")
def read_root(name):
    return {"message": f"Hello , {name}!"}
