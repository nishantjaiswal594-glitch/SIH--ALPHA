from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.application import Application
from app.models.company import Company
from app.models.opportunity import Opportunity
from app.models.opportunity_skill import OpportunitySkill
from app.models.skill import Skill
from app.models.student import Student
from app.models.student_skill import StudentSkill
from app.services.security import get_current_user


router = APIRouter(
    prefix="/opportunities",
    tags=["Opportunities"]
)


SKILL_LEVELS = {
    "Beginner": 1,
    "Intermediate": 2,
    "Advanced": 3,
    "Expert": 4
}


def level_score(student_level, required_level):
    student_value = SKILL_LEVELS.get(student_level, 1)
    required_value = SKILL_LEVELS.get(required_level, 1)

    if required_value <= 0:
        return 100

    return min(
        round((student_value / required_value) * 100),
        100
    )


def get_student(db: Session, user_id: int):
    student = (
        db.query(Student)
        .filter(Student.user_id == user_id)
        .first()
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student profile not found"
        )

    return student


def get_student_skill_map(db: Session, student_id: int):
    student_skills = (
        db.query(StudentSkill, Skill)
        .join(
            Skill,
            StudentSkill.skill_id == Skill.skill_id
        )
        .filter(
            StudentSkill.student_id == student_id
        )
        .all()
    )

    return {
        student_skill.skill_id: {
            "name": skill.skill_name,
            "level": student_skill.proficiency_level
        }
        for student_skill, skill in student_skills
    }


def calculate_opportunity_match(
    db: Session,
    student_id: int,
    opportunity_id: int
):
    student_skill_map = get_student_skill_map(
        db,
        student_id
    )

    required_skills = (
        db.query(OpportunitySkill, Skill)
        .join(
            Skill,
            OpportunitySkill.skill_id == Skill.skill_id
        )
        .filter(
            OpportunitySkill.opportunity_id
            == opportunity_id
        )
        .all()
    )

    if not required_skills:
        return {
            "compatibility_score": 50,
            "matching_skills": [],
            "missing_skills": []
        }

    matching_skills = []
    missing_skills = []
    skill_scores = []

    for opportunity_skill, skill in required_skills:

        student_skill = student_skill_map.get(
            opportunity_skill.skill_id
        )

        if student_skill:

            score = level_score(
                student_skill["level"],
                opportunity_skill.required_level
            )

            skill_scores.append(score)

            if score >= 70:
                matching_skills.append({
                    "skill": skill.skill_name,
                    "student_level": student_skill["level"],
                    "required_level": opportunity_skill.required_level,
                    "score": score
                })
            else:
                missing_skills.append({
                    "skill": skill.skill_name,
                    "student_level": student_skill["level"],
                    "required_level": opportunity_skill.required_level,
                    "score": score,
                    "gap": 100 - score
                })

        else:

            skill_scores.append(0)

            missing_skills.append({
                "skill": skill.skill_name,
                "student_level": None,
                "required_level": opportunity_skill.required_level,
                "score": 0,
                "gap": 100
            })

    compatibility_score = round(
        sum(skill_scores) / len(skill_scores)
    )

    return {
        "compatibility_score": compatibility_score,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills
    }


# ============================================================
# RECOMMENDED OPPORTUNITY
# ============================================================

@router.get("/recommended")
def get_recommended_opportunity(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    student = get_student(
        db,
        current_user["id"]
    )

    opportunities = (
        db.query(Opportunity)
        .order_by(Opportunity.created_at.desc())
        .all()
    )

    if not opportunities:
        raise HTTPException(
            status_code=404,
            detail="No opportunities available"
        )

    recommendations = []

    for opportunity in opportunities:

        match = calculate_opportunity_match(
            db,
            student.student_id,
            opportunity.opportunity_id
        )

        company = (
            db.query(Company)
            .filter(
                Company.company_id
                == opportunity.company_id
            )
            .first()
        )

        recommendations.append({
            "opportunity_id": opportunity.opportunity_id,
            "title": opportunity.title,
            "description": opportunity.description,
            "location": opportunity.location,
            "company": {
                "company_id": company.company_id
                if company else None,
                "name": company.name
                if company else "Unknown Company",
                "industry": company.industry
                if company else None,
                "location": company.location
                if company else None,
                "website": company.website
                if company else None
            },
            "compatibility_score": match[
                "compatibility_score"
            ],
            "matching_skills": match[
                "matching_skills"
            ],
            "missing_skills": match[
                "missing_skills"
            ]
        })

    recommendations.sort(
        key=lambda item: item["compatibility_score"],
        reverse=True
    )

    return {
        "student_id": student.student_id,
        "recommendation": recommendations[0],
        "status": "success"
    }


# ============================================================
# OPPORTUNITY COMPATIBILITY
# ============================================================

@router.get("/{opportunity_id}/compatibility")
def get_opportunity_compatibility(
    opportunity_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    student = get_student(
        db,
        current_user["id"]
    )

    opportunity = (
        db.query(Opportunity)
        .filter(
            Opportunity.opportunity_id == opportunity_id
        )
        .first()
    )

    if not opportunity:
        raise HTTPException(
            status_code=404,
            detail="Opportunity not found"
        )

    match = calculate_opportunity_match(
        db,
        student.student_id,
        opportunity_id
    )

    score = match["compatibility_score"]

    if score >= 80:
        recommendation = "Strong Match"
    elif score >= 60:
        recommendation = "Good Match"
    elif score >= 40:
        recommendation = "Moderate Match"
    else:
        recommendation = "Needs Skill Development"

    return {
        "opportunity_id": opportunity.opportunity_id,
        "student_id": student.student_id,
        "title": opportunity.title,
        "overall_compatibility": score,
        "matched_skills": match["matching_skills"],
        "skill_gaps": match["missing_skills"],
        "recommendation": recommendation,
        "status": "success"
    }


# ============================================================
# APPLY TO OPPORTUNITY
# ============================================================

@router.post("/{opportunity_id}/apply")
def apply_to_opportunity(
    opportunity_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Find student
    student = get_student(
        db,
        current_user["id"]
    )

    # Check opportunity exists
    opportunity = (
        db.query(Opportunity)
        .filter(
            Opportunity.opportunity_id == opportunity_id
        )
        .first()
    )

    if not opportunity:
        raise HTTPException(
            status_code=404,
            detail="Opportunity not found"
        )

    # Check whether this student already applied
    existing_application = (
        db.query(Application)
        .filter(
            Application.student_id == student.student_id,
            Application.opportunity_id == opportunity_id
        )
        .first()
    )

    if existing_application:
        return {
            "message": "Already applied to this opportunity",
            "application_id": existing_application.application_id,
            "status": existing_application.status
        }

    # Create application
    application = Application(
        student_id=student.student_id,
        opportunity_id=opportunity_id,
        status="Applied"
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return {
        "message": "Application submitted successfully",
        "application_id": application.application_id,
        "student_id": student.student_id,
        "opportunity_id": opportunity_id,
        "status": application.status
    }