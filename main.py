from fastapi import FastAPI

app = FastAPI(title="ORMs - Erros Comuns")


@app.get("/")
def root():
    return {"message": "Hello from orms-erros-comuns!"}
