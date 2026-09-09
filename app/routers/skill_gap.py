from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.assessment_result import AssessmentResult
from app.models.student import Student
from app.services.security import get_current_user


router = APIRouter(
    prefix="/skills",
    tags=["Skill Gap"]
)


@router.get("/gaps")
def get_skill_gaps(
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

    # The minimum score required to consider a skill satisfactory
    required_score = 70

    category_scores = {
        "Technical Skills": result.technical_score,
        "Aptitude": result.aptitude_score,
        "Communication": result.communication_score,
        "Problem Solving": result.problem_solving_score
    }

    gaps = []
    strong_skills = []

    for skill_name, current_score in category_scores.items():

        if current_score >= required_score:
            strong_skills.append(skill_name)

        else:
            gap = required_score - current_score

            if gap >= 30:
                priority = "High"
            elif gap >= 15:
                priority = "Medium"
            else:
                priority = "Low"

            gaps.append({
                "skill": skill_name,
                "current_score": current_score,
                "required_score": required_score,
                "gap": gap,
                "priority": priority
            })

    return {
        "student_id": student.student_id,
        "assessment_id": result.assessment_id,
        "overall_score": result.overall_score,
        "required_score": required_score,
        "strong_skills": strong_skills,
        "gaps": gaps,
        "status": "completed"
    }