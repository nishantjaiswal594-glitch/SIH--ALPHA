from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.assessment_result import AssessmentResult
from app.models.student import Student
from app.services.security import get_current_user


router = APIRouter(
    prefix="/skills",
    tags=["Skill Analysis"]
)


@router.get("/analysis")
def get_skill_analysis(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Find logged-in student's profile
    student = (
        db.query(Student)
        .filter(Student.user_id == current_user["id"])
        .first()
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student profile not found"
        )

    # Get latest assessment result
    result = (
        db.query(AssessmentResult)
        .filter(
            AssessmentResult.student_id == student.student_id
        )
        .order_by(
            AssessmentResult.completed_at.desc()
        )
        .first()
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="No assessment result found. Complete the assessment first."
        )

    category_scores = {
        "Technical Skills": result.technical_score,
        "Aptitude": result.aptitude_score,
        "Communication": result.communication_score,
        "Problem Solving": result.problem_solving_score
    }

    skills = []

    for skill_name, score in category_scores.items():

        if score >= 80:
            level = "Expert"
            status = "Strong"

        elif score >= 60:
            level = "Intermediate"
            status = "Developing"

        elif score >= 40:
            level = "Beginner"
            status = "Needs Improvement"

        else:
            level = "Beginner"
            status = "Skill Gap"

        skills.append({
            "skill": skill_name,
            "score": score,
            "level": level,
            "status": status
        })

    return {
        "student_id": student.student_id,
        "assessment_id": result.assessment_id,
        "overall_score": result.overall_score,
        "skills": skills,
        "status": "completed"
    }