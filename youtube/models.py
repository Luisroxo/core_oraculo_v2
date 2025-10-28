from pydantic import BaseModel
from typing import Optional

class Video(BaseModel):
    video_id: str
    title: str
    published_at: str
    description: Optional[str]
    channel_id: str
    transcricao: str = ""
    view_count: Optional[int] = None
    like_count: Optional[int] = None
    comment_count: Optional[int] = None
    duration: Optional[str] = None
    url: Optional[str] = None
    thumbnail: Optional[str] = None
    tags: Optional[str] = None
