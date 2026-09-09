from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.company import Company
from app.models.opportunity import Opportunity
from app.models.opportunity_skill import OpportunitySkill
from app.models.skill import Skill
from app.services.security import get_current_user


router = APIRouter(
    prefix="/seed",
    tags=["Demo Seed"]
)


@router.post("/opportunity")
def seed_demo_opportunity(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # ---------------------------------------------------------
    # Check whether demo opportunity already exists
    # ---------------------------------------------------------

    existing = (
        db.query(Opportunity)
        .filter(
            Opportunity.title == "AI/ML Intern"
        )
        .first()
    )

    if existing:
        return {
            "message": "Demo opportunity already exists",
            "opportunity_id": existing.opportunity_id
        }

    # ---------------------------------------------------------
    # Create company
    # ---------------------------------------------------------

    company = (
        db.query(Company)
        .filter(
            Company.name == "TechNova Solutions"
        )
        .first()
    )

    if not company:
        company = Company(
            name="TechNova Solutions",
            industry="Technology",
            location="Bengaluru",
            website="https://technova.example.com"
        )

        db.add(company)
        db.flush()

    # ---------------------------------------------------------
    # Create opportunity
    # ---------------------------------------------------------

    opportunity = Opportunity(
        company_id=company.company_id,
        title="AI/ML Intern",
        description=(
            "Work on machine learning models, data analysis, "
            "and Python-based AI applications."
        ),
        location="Bengaluru"
    )

    db.add(opportunity)
    db.flush()

    # ---------------------------------------------------------
    # Find or create required skills
    # ---------------------------------------------------------

    skill_names = [
        "Python",
        "Machine Learning",
        "SQL"
    ]

    for skill_name in skill_names:

        skill = (
            db.query(Skill)
            .filter(
                Skill.skill_name == skill_name
            )
            .first()
        )

        if not skill:
            category = (
                "Programming"
                if skill_name == "Python"
                else "Technical"
            )

            skill = Skill(
                skill_name=skill_name,
                category=category
            )

            db.add(skill)
            db.flush()

        existing_link = (
            db.query(OpportunitySkill)
            .filter(
                OpportunitySkill.opportunity_id
                == opportunity.opportunity_id,
                OpportunitySkill.skill_id
                == skill.skill_id
            )
            .first()
        )

        if not existing_link:
            opportunity_skill = OpportunitySkill(
                opportunity_id=opportunity.opportunity_id,
                skill_id=skill.skill_id,
                required_level="Intermediate"
            )

            db.add(opportunity_skill)

    db.commit()

    return {
        "message": "Demo opportunity created successfully",
        "company_id": company.company_id,
        "opportunity_id": opportunity.opportunity_id,
        "title": opportunity.title,
        "required_skills": skill_names
    }