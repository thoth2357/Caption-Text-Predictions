from fastapi import FastAPI
from scrape import start_scrape
import model

app = FastAPI()

@app.post("/scrape")
async def start_scraping(account_to_scrape: str, username: str, password: str):
    '''Starts the scraping process'''
    result = start_scrape(account_to_scrape, username, password)
    return {"message": result}

@app.post("/start-model")
async def start_model():
    '''Starts the model training process'''
    results = model.start_model()
    return results

