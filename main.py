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
    json_output = {
        "comment": "You have a great sense of style! Your outfit is casual and layered, creating a modern and comfortable look.",
        "style_name": "casual",
        "fashion_items_as_keywords": [
            {
                "link": "https://www.amazon.com/Gildan-Mens-T-Shirt-White-Small/dp/B077ZCT9SS?source=ps-sl-shoppingads-lpcontext&ref_=fplfs&psc=1&smid=ATVPDKIKX0DER&rct=j&q=&esrc=s&opi=95576897&sa=U&ved=0ahUKEwiit_yM87yCAxVHEDQIHZyIBvUQguUECKwV&usg=AOvVaw2B3E6Tvin-9eieWWsJQ7bw",
                "name": "Gildan Men's Crew T-Shirt 6 Pack, White, Small",
                "price": "$15.97",
            },
            {
                "link": "https://www.amazon.com/Dickies-Pullover-Fleece-Hoodie-Heather/dp/B07WHDVBD1?source=ps-sl-shoppingads-lpcontext&ref_=fplfs&psc=1&smid=ATVPDKIKX0DER&rct=j&q=&esrc=s&opi=95576897&sa=U&ved=0ahUKEwjg49-O87yCAxVdLzQIHQeTA3sQguUECOoW&usg=AOvVaw3lypwoHcG9_0siJ7qYZ_zr",
                "name": "Dickies Men's Fleece Pullover Hoodie, TW292, Heather Gray",
                "price": "$29.99",
            },
            {
                "link": "https://www.abercrombie.com/shop/us/p/a-and-f-sloane-tailored-pant-53796877?seq=42&source=googleshopping&rct=j&q=&esrc=s&opi=95576897&sa=U&ved=0ahUKEwiC5sSQ87yCAxVrCTQIHY6nAQkQguUECOkT&usg=AOvVaw3A2mqZ8qTWEen3rqko8gUi",
                "name": "Women's A&F Sloane Tailored Pant in Green | Size 32 | Abercrombie & Fitch",
                "price": "$76.50",
            },
            {
                "link": "https://stockx.com/air-jordan-4-retro-midnight-navy-ps?country=US&currencyCode=USD&size=1Y&srsltid=AfmBOorKPjOF04TDFI0IDWcHhANaPK-CdEk5tmRDRtN6J6ObTVX2TbG9FYQ&rct=j&q=&esrc=s&opi=95576897&sa=U&ved=0ahUKEwjs7qCS87yCAxXCLzQIHQkgARoQguUECKgX&usg=AOvVaw2LfGLeDl2uu9cJ0BmSBIET",
                "name": "Jordan 4 Retro Midnight Navy (PS) BQ7669-140",
                "price": "$74.00",
            },
            {
                "link": "https://www.ebay.com/itm/355114695090?chn=ps&mkevt=1&mkcid=28&srsltid=AfmBOop_NaG04RzOkMYJOfpNKTVPF6xT5s51xJVxh9vl5AW67Je7t5xMAAo&com_cvv=d30042528f072ba8a22b19c81250437cd47a2f30330f0ed03551c4efdaf3409e&rct=j&q=&esrc=s&opi=95576897&sa=U&ved=0ahUKEwjmlKWU87yCAxU8CTQIHWxeAjYQgOUECIAQ&usg=AOvVaw1QlKafd2ti-z8gP_xSdKx7",
                "name": "Men's Stainless Steel Durable Waterproof Watch - Dark Blue Dial -",
                "price": "$78.99",
            },
        ],
    }

    # loop = None

    # try:
    #     loop = asyncio.get_event_loop()
    # except RuntimeError:
    #     print("Creating new event loop")
    #     loop = asyncio.new_event_loop()
    #     asyncio.set_event_loop(loop)

    # # output = await ask_shopwise_all_at_once(json_output["fashion_items_as_keywords"])

    # output_shopwise = []
    # for keyword in json_output["fashion_items_as_keywords"]:
    #     output_shopwise.append(await ask_shopwise(keyword))

    return json_output


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000)
