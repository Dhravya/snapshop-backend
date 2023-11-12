from fastapi import FastAPI, Body, Form
from fastapi.responses import JSONResponse
from helpers.redis_helpers import create_user, get_all_generations
from helpers.models import UserInfo, TryOnImage
from dotenv import load_dotenv
from api_calls import get_fashion_and_user_image, get_fashion_recommendation_with_shopping_links
from redis_om import Migrator, get_redis_connection
from os import environ as env
from dotenv import load_dotenv
from helpers.upload_image import upload_image
from api_calls import ask_shopwise
import asyncio
from rich.traceback import install
import json
import logging

install()
load_dotenv()

redis = get_redis_connection(url=env.get("REDIS_OM_URL"))
Migrator().run()

app = FastAPI()


async def ask_shopwise_all_at_once(keywords: list[str]):
    tasks = [asyncio.create_task(ask_shopwise(keyword)) for keyword in keywords]
    try:
        # Wait for all tasks to complete, with a timeout for each task
        output = await asyncio.gather(*tasks, return_exceptions=True)
        print(output)
        return [result for result in output if not isinstance(result, Exception)]
    except Exception as e:
        print(f"An error occurred: {e}")


@app.get("/")
def read_root():
    return {"healthcheck": "ALL GOOD"}


@app.post("/new_user")
async def new_user(image: str = Form(...), email: str = Form(...), gender: str = Form(...), name: str = Form(...) ):
    """Send a request to create a new user whenever a new user is created in the frontend"""
    url = upload_image(image)
    user = create_user(name, email, url, gender)

    return JSONResponse(content=user.dict())

@app.post("/fashion_sense")
async def predict(image: TryOnImage = Body(...)):
    """Predict endpoint, this takes an image and returns a prediction with the shopping links"""
    json_output = await get_fashion_and_user_image(
        image.original_image, image.user_email
    )

    return JSONResponse(content=json_output)

@app.get("/fashion_recommendation")
async def predict_recommendation(user_prompt: str, user_email: str):
    """Recommendation endpoint for chat, this takes a user prompt and returns a prediction with the shopping links"""
    json_output = await get_fashion_recommendation_with_shopping_links(
        user_prompt, user_email
    )

    return JSONResponse(content=json_output)


@app.post("/fashion_sense_test")
async def predict_test(image: TryOnImage = Body(...)):
    """Acts like predict / predict_recommendation but returns a test json instead of calling the api"""
    with open("test.json", "r") as f:
        json_output = json.load(f)
        return json_output
    
@app.get("/featured_page")
async def featured_page():
    """All generations are stored in redis, this endpoint returns all generations for the explore page"""
    return JSONResponse(get_all_generations())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000)
