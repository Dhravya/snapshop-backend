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
                    "description": "A list of fashion items in the image as a google searchable word. There must be one string for every item in image. Include the color and brand where necessary",
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
