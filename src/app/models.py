from pydantic import BaseModel, Field, field_validator
from typing import Optional

class PromptRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=500, description="The prompt for the LLM")

    @field_validator('prompt')
    def validate_prompt(cls, value):
        if any(bad_word in value.lower() for bad_word in ["badword1", "badword2"]):
            raise ValueError("Prompt contains inappropriate content")
        return value