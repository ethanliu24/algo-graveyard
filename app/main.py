from fastapi import FastAPI
from .config import Configs

app = FastAPI()
configs = Configs()

@app.get("/")
def main():
    return "Hello world"