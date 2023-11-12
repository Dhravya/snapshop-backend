from typing import List, Optional
from os import environ as env
from rich import print
from pydantic import AnyHttpUrl
from redis_om import get_redis_connection, HashModel, JsonModel, Field
from pydantic import AnyHttpUrl
from os import environ as env
from dotenv import load_dotenv
load_dotenv()

print(env.get("REDIS_OM_URL"))

redis = get_redis_connection(url=env.get("REDIS_OM_URL"))

class User(JsonModel):
    """User model"""
    email: str = Field(primary_key=True)
    name: str
    image_url: str
    gender: str

    class Meta:
        database = redis
        global_key_prefix = "user:"

class Generation(JsonModel):
    """Generated outputs with links"""
    generated_json_output_as_dict: dict = Field()

    class Meta:
        database = redis
        global_key_prefix = "generation:"

def get_user(email: str) -> Optional[User]:
    """Get user from redis"""
    user = User.get(pk=email)
    return user

def create_user(name: str, email: str, image_url: AnyHttpUrl, gender: str) -> User:
    """Create user in redis"""
    user = User(name=name, email=email, image_url=image_url, gender=gender)
    user.save()
    return user

def create_generation(generated_json_output_as_dict: dict) -> Generation:
    """Create generation in redis"""
    generation = Generation(generated_json_output_as_dict=generated_json_output_as_dict)
    generation.save()
    return generation

def get_all_generations() -> List[Generation]:
    """Get all generations from redis"""
    generations = Generation.all_pks()

    g = [Generation.get(pk=generation).dict()['generated_json_output_as_dict'] for generation in generations]

    return g
