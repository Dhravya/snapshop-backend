from datetime import datetime

todays_date = datetime.now().strftime("%Y-%m-%d")

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
                    "description": "A very short positive comment about the fashion sense of the image",
                },
                "style_name": {
                    "type": "string",
                    "description": "A style name, like 'formal', 'casual', etc.",
                },
                "fashion_items_as_keywords": {
                    "type": "array",
                    "description": "A list of fashion items in the image as a google searchable word. There must be one string for every item in image. Include the color, gender of the subject and brand where necessary - like mens blue zip-up hoodie. The user should be able to create a google search query with this string.",
                    "items": {"type": "string"},
                },
            },
            "required": [
                "comment",
                "style_name",
                "fashion_items_as_keywords",
            ],
        },
    }
]

other_func = [
        {
        "name": "give_fashion_recommendation",
        "description": f"From the user's situation and context, give a fashion recommendation. For eg: I'm going to london for a tech conference next week, what should I wear? -> should return a list of fashion items that the user should wear, like semiformal, warm clothes, etc. Today's date is {todays_date}",
        "type": "function",
        "parameters": {
            "type": "object",
            "properties": {
                "comment": {
                    "type": "string",
                    "description": "A very short comment about the considerations for the fashion recommendations, for example - 'the weather may be warm, and since its a tech conference, you should wear semiformal clothes'.",
                },
                "style_name": {
                    "type": "string",
                    "description": "A style name, like 'formal', 'casual', etc.",
                },
                "fashion_items_as_keywords": {
                    "type": "array",
                    "description": "A list of fashion items in the image as a google searchable word. There must be one string for every item in image. Include the color, gender of the subject and brand where necessary. The user should be able to create a google search query with this string.",
                    "items": {"type": "string"},
                },
            },
            "required": [
                "comment",
                "style_name",
                "fashion_items_as_keywords",
            ],
        },
    },
]