import httpx
from openai import OpenAI
from funcs import functions
import asyncify
from helpers.redis_helpers import get_user, create_generation
import asyncio
import json
from helpers.upload_image import upload_image

client = OpenAI()

async def ask_shopwise(item_name: str):
    print("Asking shopwise for " + item_name)
    # response = httpx.get(f"https://dropit2-production.up.railway.app/googleSearch?itemName={item_name}")
    # return response.json()

    response = httpx.get(f"https://dropit2-production.up.railway.app/googleSearch?itemName={item_name}")
    return response.json()

@asyncify
def get_fashion_image(base64_image: str):
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What’s in this image? Describe it in as detail as possible. You are a fashion stylist. Be as descriptive about the fashion items as possible.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    },
                ],
            }
        ],
        max_tokens=250,
    )

    function_response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"What’s in this image? Describe it in as detail as possible. You are a fashion stylist. Be as descriptive about the fashion items as possible. Here's the description of the image: {response.choices[0]}",
                    },
                ],
            }
        ],
        max_tokens=500,
        functions=functions,
        function_call="auto",
    )

    function_response = json.loads(function_response.choices[0].message.function_call.arguments)

    function_response.fashion_items_as_keywords = [
            {outputKey: ask_shopwise(outputKey)} for outputKey in function_response["fashion_items_as_keywords"]
        ]

    return function_response

async def get_fashion_and_user_image(original_image: str, user_email: str):
    user_image = get_user(user_email).image_url

    if not user_image:
        return {
            "error": "User not found",
        }

    output_json = await asyncio.gather(
        get_fashion_image(original_image),
    )

    # json.loads output_json if it's a string
    if not isinstance(output_json, dict):
        output_json = json.loads(output_json)

    create_generation(output_json)

    return output_json
