from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from helpers.redis_helpers import create_user
from helpers.models import UserInfo, TryOnImage
from dotenv import load_dotenv
from api_calls import get_fashion_and_user_image
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

print(env.get("REDIS_OM_URL"))
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
async def new_user(user: UserInfo = Body(...)):
    url = upload_image(user.image)
    user = create_user(user.name, user.email, url)

    return JSONResponse(content=user.dict())


@app.post("/fashion_sense")
async def predict(image: TryOnImage = Body(...)):
    json_output = await get_fashion_and_user_image(
        image.original_image, image.user_email
    )

    return JSONResponse(content=json_output)


@app.post("/fashion_sense_test")
async def predict_test(image: TryOnImage = Body(...)):
    with open("test.json", "r") as f:
        json_output = json.load(f)

        return json_output


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000)
