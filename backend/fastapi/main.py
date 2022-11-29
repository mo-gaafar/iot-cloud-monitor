import uvicorn
from fastapi import FastAPI

from app.app import app


app = app

#TODO: remember to set reload to false when deploying
if __name__ == "__main__":
    uvicorn.run("app.app:app", port=8080, reload=True)
