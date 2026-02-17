from pydantic import BaseModel
from typing import List, Optional


from pydantic import BaseModel
from typing import List, Optional

class QuestionRequest(BaseModel):
    question: str
    session_id: str


class SourceItem(BaseModel):
    page: Optional[str]
    snippet: str


class QuestionResponse(BaseModel):
    answer: str
    sources: List[SourceItem]
    confidence: str


class UploadResponse(BaseModel):
    message: str
    total_chunks: int

    
# app/schemas/models.py
