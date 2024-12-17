from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


# Base Feedback Schema
class FeedbackBase(BaseModel):
    rating: int
    comment: Optional[str] = None
    receiver_id: int  # ID of the user receiving the feedback


# Schema for Creating Feedback
class FeedbackCreate(FeedbackBase):
    """
    Schema for creating new feedback.
    """
    pass


# Schema for Feedback Response
class FeedbackResponse(FeedbackBase):
    """
    Schema for returning feedback details.
    """
    id: int
    giver_id: int  # ID of the user giving the feedback
    created_at: datetime

    class Config:
        orm_mode = True


# Schema for a List of Feedbacks
class FeedbackListResponse(BaseModel):
    """
    Schema for returning a list of feedback.
    """
    feedbacks: List[FeedbackResponse]

    class Config:
        orm_mode = True
