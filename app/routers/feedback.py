from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Feedback, User
from app.database import get_db
from app.schemas.feedback import FeedbackCreate, FeedbackResponse, FeedbackListResponse
from app.oauth2 import get_current_user

# Initialize the router
router = APIRouter(
    tags=["Feedback"],
)


# Create new feedback
@router.post("", response_model=FeedbackResponse)
def create_feedback(
    feedback: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Create new feedback for a user.
    """
    # Ensure the receiver exists
    receiver = db.query(User).filter(User.id == feedback.receiver_id).first()
    if not receiver:
        raise HTTPException(status_code=404, detail="Receiver user not found")

    # Prevent self-feedback
    if feedback.receiver_id == current_user.id:
        raise HTTPException(status_code=400, detail="You cannot give feedback to yourself")

    # Create feedback
    new_feedback = Feedback(
        rating=feedback.rating,
        comment=feedback.comment,
        receiver_id=feedback.receiver_id,
        giver_id=current_user.id,
    )
    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)
    return new_feedback


# Get feedback received by a user
@router.get("/received", response_model=FeedbackListResponse)
def get_received_feedbacks(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Retrieve feedback received by the current user.
    """
    feedbacks = db.query(Feedback).filter(Feedback.receiver_id == current_user.id).all()
    return {"feedbacks": feedbacks}


# Get feedback given by the current user
@router.get("/given", response_model=FeedbackListResponse)
def get_given_feedbacks(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Retrieve feedback given by the current user.
    """
    feedbacks = db.query(Feedback).filter(Feedback.giver_id == current_user.id).all()
    return {"feedbacks": feedbacks}


# Delete feedback by ID
@router.delete("/{feedback_id}")
def delete_feedback(
    feedback_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Delete feedback given by the current user.
    """
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")

    # Only allow the giver to delete the feedback
    if feedback.giver_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this feedback")

    db.delete(feedback)
    db.commit()
    return {"message": "Feedback deleted successfully"}
