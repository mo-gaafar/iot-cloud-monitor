import uvicorn

#TODO: remember to set reload to false when deploying
if __name__ == "__main__":
    uvicorn.run("app.app:app", port= 8000, 
    reload= True)