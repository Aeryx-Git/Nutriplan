from pydantic import BaseModel, Field
from typing import List

class Recipe(BaseModel):
    recipe_name: str = Field(description="The name of the recipe.")
    ingredients: List[str] = Field(description="A list of ingredients required for the recipe.")
    instructions: List[str] = Field(description="A list of step-by-step instructions to prepare the recipe.")
