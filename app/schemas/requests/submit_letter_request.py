from pydantic import BaseModel, Field


class SubmitLetterRequest(BaseModel):
    session_id: str = Field(min_length=36, max_length=36)
    guess_word: str = Field(min_length=3, max_length=7)