from pydantic import BaseModel
from typing import List, Dict, Optional, Union

######### GENAI MODELS #########
class GenAiQuestion(BaseModel):
    question: str

class GenAiAnswer(BaseModel):
    answer: str

class PromptRequest(BaseModel):
    prompt: str