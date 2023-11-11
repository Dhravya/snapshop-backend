from openai import OpenAI
from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import json


class Image(BaseModel):
    image: str


app = FastAPI()
client = OpenAI()

functions = [
    {
        "name": "get_users_fashion_sense",
        "description": "Get the user's fashion sense",
        "type": "function",
        "parameters": {
            "type": "object",
            "properties": {
                "comment": {
                    "type": "string",
                    "description": "A positive comment about the fashion sense of the image",
                },
                "style_name": {
                    "type": "string",
                    "description": "A style name, like 'formal', 'casual', etc.",
                },
                "fashion_items_as_keywords": {
                    "type": "array",
                    "description": "A list of fashion items in the image as keywords for search - if there's a color, include the color, and brand, if identifiable. For every item, there must be a keyword. This is a list of items, so each item should be a different string without repeating. One item can be 'navy blue sued and fabric sneakers', another can be 'blue zip-up jacket'. Also include non-fashion products, like 'black iPhone 12 Pro Max'. Do not include hair and other bodily features. It should only have fashion items and non-fashion products. Wherever possible, mention the brand. So, instead of 'laptop with apple logo', say 'macbook pro'.",
                    "items": {"type": "string"},
                },
                # "fashion_items_as_description": {
                #     "type": "array",
                #     "description": "A list of fashion items in the image as a readable description with all details. For every item, there must be a description, it should include everything, including the color, type, brand, if identified. Each item should be a different string in the json.",
                #     "items": {"type": "string"},
                # },
            },
            "required": [
                "comment",
                "style_name",
                "fashion_items_as_keywords",
                # "fashion_items_as_description",
            ],
        },
    },
]


@app.get("/")
def read_root():
    return {"healthcheck": "ALL GOOD"}


@app.post("/fashion_sense")
def predict(image: Image = Body(...)):
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
                            "url": f"data:image/jpeg;base64,{image.image}",
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

    json_output = function_response.choices[0].message.function_call.arguments

    return JSONResponse(content=json.loads(json_output))


@app.post("/fashion_sense_test")
def predict(image: Image = Body(...)):
    json_output = {
        "comment": "You have a great sense of style! Your outfit is casual and layered, creating a modern and comfortable look. The combination of colors and textures is well-coordinated, giving off a casual yet sophisticated vibe. The choice of eyewear and the relaxed fit of the trousers add a contemporary touch to the overall outfit. The apple logo on the laptop adds a tech-savvy element to your style.",
        "style_name": "casual",
        "fashion_items_as_keywords": [
            "glasses",
            "short textured hair",
            "white crewneck t-shirt",
            "heather gray pullover hoodie",
            "blue zip-up jacket",
            "dark green trousers",
            "cuffed trousers",
            "ankle-revealing trousers",
            "drop-crotch silhouette trousers",
            "navy blue sneakers",
            "suede and fabric sneakers",
            "laptop with apple logo",
        ],
        "fashion_items_as_description": [
            "Pair of dark-rimmed glasses",
            "Short textured hair",
            "White crewneck t-shirt",
            "Heather gray pullover hoodie",
            "Blue zip-up jacket with a visible texture",
            "Dark green trousers with a relaxed fit",
            "Cuffed dark green trousers that reveal the ankles",
            "Trousers with a slight drop-crotch silhouette",
            "Navy blue sneakers with a clean and sleek design",
            "Laptop computer with a visible Apple Inc. logo",
        ],
    }
    return JSONResponse(content=json.loads(json_output))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", reload=True)
