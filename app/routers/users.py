from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.application import Application
from app.models.project import Project
from app.models.skill import Skill
from app.models.student import Student
from app.models.student_skill import StudentSkill
from app.models.user import User
from app.schemas.user import StudentProfileUpdate
from app.services.security import get_current_user


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/me")
def read_users_me(
    current_user: dict = Depends(get_current_user)
):
    return {
        "message": "You are authenticated",
        "user": current_user
    }


@router.get("/me/profile")
def get_my_student_profile(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user.get("id")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authenticated user"
        )

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    student = (
        db.query(Student)
        .filter(Student.user_id == user.id)
        .first()
    )

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found"
        )

    student_skills = (
        db.query(StudentSkill, Skill)
        .join(
            Skill,
            StudentSkill.skill_id == Skill.skill_id
        )
        .filter(
            StudentSkill.student_id == student.student_id
        )
        .all()
    )

    skills = [
        {
            "skill_id": skill.skill_id,
            "skill_name": skill.skill_name,
            "category": skill.category,
            "proficiency_level": student_skill.proficiency_level
        }
        for student_skill, skill in student_skills
    ]

    skills_count = (
        db.query(func.count(StudentSkill.skill_id))
        .filter(
            StudentSkill.student_id == student.student_id
        )
        .scalar()
    )

    applications_count = (
        db.query(func.count(Application.application_id))
        .filter(
            Application.student_id == student.student_id
        )
        .scalar()
    )

    projects_count = (
        db.query(func.count(Project.project_id))
        .filter(
            Project.student_id == student.student_id
        )
        .scalar()
    )

    return {
        "personal": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "is_verified": user.is_verified,
            "phone": student.phone,
            "date_of_birth": student.date_of_birth,
            "location": student.location
        },
        "academic": {
            "student_id": student.student_id,
            "college": student.college,
            "degree": student.degree,
            "branch": student.branch,
            "graduation_year": student.graduation_year,
            "semester": student.semester,
            "cgpa": student.cgpa
        },
        "career": {
            "preferred_roles": student.preferred_roles,
            "preferred_industries": student.preferred_industries,
            "preferred_work_locations": student.preferred_work_locations
        },
        "profile": {
            "profile_picture_url": student.profile_picture_url,
            "resume_url": student.resume_url
        },
        "skills": skills,
        "statistics": {
            "skills_added": skills_count or 0,
            "applications": applications_count or 0,
            "projects": projects_count or 0,
            "internships": None
        }
    }


@router.put("/me/profile")
def update_my_student_profile(
    profile_data: StudentProfileUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user.get("id")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    student = (
        db.query(Student)
        .filter(Student.user_id == user.id)
        .first()
    )

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found"
        )

    update_data = profile_data.model_dump(exclude_unset=True)

    # Personal information
    if "name" in update_data:
        user.name = update_data["name"]

    if "phone" in update_data:
        student.phone = update_data["phone"]

    if "date_of_birth" in update_data:
        try:
            student.date_of_birth = (
                date.fromisoformat(update_data["date_of_birth"])
                if update_data["date_of_birth"]
                else None
            )
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="date_of_birth must use YYYY-MM-DD format"
            )

    if "location" in update_data:
        student.location = update_data["location"]

    # Academic information
    if "college" in update_data:
        student.college = update_data["college"]

    if "degree" in update_data:
        student.degree = update_data["degree"]

    if "branch" in update_data:
        student.branch = update_data["branch"]

    if "graduation_year" in update_data:
        student.graduation_year = update_data["graduation_year"]

    if "semester" in update_data:
        student.semester = update_data["semester"]

    if "cgpa" in update_data:
        student.cgpa = update_data["cgpa"]

    # Career preferences
    if "preferred_roles" in update_data:
        student.preferred_roles = update_data["preferred_roles"]

    if "preferred_industries" in update_data:
        student.preferred_industries = update_data["preferred_industries"]

    if "preferred_work_locations" in update_data:
        student.preferred_work_locations = update_data[
            "preferred_work_locations"
        ]

    db.commit()

    db.refresh(user)
    db.refresh(student)

    return {
        "message": "Student profile updated successfully",
        "personal": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "is_verified": user.is_verified,
            "phone": student.phone,
            "date_of_birth": student.date_of_birth,
            "location": student.location
        },
        "academic": {
            "student_id": student.student_id,
            "college": student.college,
            "degree": student.degree,
            "branch": student.branch,
            "graduation_year": student.graduation_year,
            "semester": student.semester,
            "cgpa": student.cgpa
        },
        "career": {
            "preferred_roles": student.preferred_roles,
            "preferred_industries": student.preferred_industries,
            "preferred_work_locations": student.preferred_work_locations
        }
    }


@router.get("/me/skills")
def get_my_skills(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user.get("id")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )

    student = (
        db.query(Student)
        .filter(Student.user_id == user_id)
        .first()
    )

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found"
        )

    student_skills = (
        db.query(StudentSkill, Skill)
        .join(
            Skill,
            StudentSkill.skill_id == Skill.skill_id
        )
        .filter(
            StudentSkill.student_id == student.student_id
        )
        .all()
    )

    return {
        "student_id": student.student_id,
        "skills": [
            {
                "skill_id": skill.skill_id,
                "skill_name": skill.skill_name,
                "category": skill.category,
                "proficiency_level": student_skill.proficiency_level
            }
            for student_skill, skill in student_skills
        ]
    }


@router.post("/me/skills")
def add_my_skill(
    skill_id: int,
    proficiency_level: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user.get("id")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )

    student = (
        db.query(Student)
        .filter(Student.user_id == user_id)
        .first()
    )

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found"
        )

    skill = (
        db.query(Skill)
        .filter(Skill.skill_id == skill_id)
        .first()
    )

    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found"
        )

    existing_skill = (
        db.query(StudentSkill)
        .filter(
            StudentSkill.student_id == student.student_id,
            StudentSkill.skill_id == skill_id
        )
        .first()
    )

    if existing_skill:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Skill already added to your profile"
        )

    new_student_skill = StudentSkill(
        student_id=student.student_id,
        skill_id=skill_id,
        proficiency_level=proficiency_level
    )

    db.add(new_student_skill)
    db.commit()

    return {
        "message": "Skill added successfully",
        "skill": {
            "skill_id": skill.skill_id,
            "skill_name": skill.skill_name,
            "category": skill.category,
            "proficiency_level": proficiency_level
        }
    }


@router.delete("/me/skills/{skill_id}")
def delete_my_skill(
    skill_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user.get("id")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )

    student = (
        db.query(Student)
        .filter(Student.user_id == user_id)
        .first()
    )

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found"
        )

    student_skill = (
        db.query(StudentSkill)
        .filter(
            StudentSkill.student_id == student.student_id,
            StudentSkill.skill_id == skill_id
        )
        .first()
    )

    if not student_skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found in your profile"
        )

    db.delete(student_skill)
    db.commit()

    return {
        "message": "Skill removed successfully"
    }


@router.get("/me/projects")
def get_my_projects(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user.get("id")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )

    student = (
        db.query(Student)
        .filter(Student.user_id == user_id)
        .first()
    )

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found"
        )

    projects = (
        db.query(Project)
        .filter(Project.student_id == student.student_id)
        .order_by(Project.project_id)
        .all()
    )

    return {
        "student_id": student.student_id,
        "projects": [
            {
                "project_id": project.project_id,
                "title": project.title
            }
            for project in projects
        ]
    }


@router.post("/me/projects")
def add_my_project(
    title: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user.get("id")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )

    student = (
        db.query(Student)
        .filter(Student.user_id == user_id)
        .first()
    )

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found"
        )

    title = title.strip()

    if not title:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Project title cannot be empty"
        )

    project = Project(
        student_id=student.student_id,
        title=title
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return {
        "message": "Project added successfully",
        "project": {
            "project_id": project.project_id,
            "title": project.title
        }
    }


@router.delete("/me/projects/{project_id}")
def delete_my_project(
    project_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user.get("id")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )

    student = (
        db.query(Student)
        .filter(Student.user_id == user_id)
        .first()
    )

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found"
        )

    project = (
        db.query(Project)
        .filter(
            Project.project_id == project_id,
            Project.student_id == student.student_id
        )
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found in your profile"
        )

    db.delete(project)
    db.commit()

    return {
        "message": "Project removed successfully"
    }