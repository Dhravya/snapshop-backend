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

    response = httpx.get(f"https://dropit2-production.up.railway.app/googleSearch?itemName={item_name}", timeout=6000)
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

    return function_response

async def get_fashion_and_user_image(original_image: str, user_email: str):
    user_image = get_user(user_email).image_url

    if not user_image:
        return {
            "error": "User not found",
        }

    output_json = await get_fashion_image(original_image)
    print(output_json)

    shopping_links = output_json['fashion_items_as_keywords']
    print(shopping_links)

    shopping_links = await asyncio.gather(
        *[ask_shopwise(keyword) for keyword in shopping_links]
    )
    output_json['fashion_items_as_keywords'] = shopping_links
    output_json['original_image'] = upload_image(original_image)
    
    if not isinstance(output_json, dict):
        output_json = json.loads(output_json)

    print(output_json)

    try:
        create_generation(output_json)
    except Exception as e:
        print(e)

    return output_json

import json
with open("test.json", "r") as f:
    json_output = json.load(f)

    asyncio.run(get_fashion_and_user_image(json_output["original_image"], "dhravyashah@gmail.com"))