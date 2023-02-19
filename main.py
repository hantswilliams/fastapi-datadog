import os
from fastapi import FastAPI, HTTPException
import uvicorn
from dotenv import load_dotenv
from utils.logging_dd import logger

## load in the .env.dev file
load_dotenv('.env.dev')

# Set up the FastAPI app
app = FastAPI()

@app.get("/")
def read_root():
    logger.warning("Handling root request")
    ## print the ENV variable from .env.dev
    print(os.getenv('ENV'))
    ## log the ENV variable from .env.dev
    logger.info('ENV: {}'.format(os.getenv('ENV')))
    return {"Hello": "World 3"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    if item_id == 3:
        logger.warning("Handling item request #3 doesnt like!")
        raise HTTPException(status_code=418, detail="Nope!! I don't like 3.")
    return {"item_id ": item_id, "q": q}

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        log_config=None, 
        access_log=True, 
        use_colors=True,
        port=8000, 
        reload=True)

