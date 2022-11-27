import uvicorn

#TODO: remember to set reload to false when deploying
if __name__ == "__main__":
    uvicorn.run("app.app:app", port= 80, host="no1rz2.deta.dev",
    reload= False)