from typing import Dict

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.assessment_result import AssessmentResult
from app.models.student import Student
from app.services.security import get_current_user


router = APIRouter(
    prefix="/assessment",
    tags=["Assessment"]
)


# ============================================================
# ASSESSMENT DATA
# ============================================================

ASSESSMENT = {
    "id": "demo-assessment",
    "title": "Skill Assessment",
    "questions": [

        # ====================================================
        # TECHNICAL SKILLS
        # ====================================================

        {
            "id": "technical-skills-1",
            "category": "Technical Skills",
            "topic": "Data Structures",
            "difficulty": "Medium",
            "question": "What data structure provides average O(1) lookup time by key?",
            "options": [
                {
                    "id": "A",
                    "label": "Array",
                    "description": "Provides indexed access in O(1), but not key-based lookup."
                },
                {
                    "id": "B",
                    "label": "Linked List",
                    "description": "Provides sequential access in O(n) time."
                },
                {
                    "id": "C",
                    "label": "Hash Table",
                    "description": "Provides average O(1) lookup time by key."
                },
                {
                    "id": "D",
                    "label": "Binary Tree",
                    "description": "Provides O(log n) lookup in balanced cases."
                }
            ],
            "correct_answer": "C"
        },

        {
            "id": "technical-skills-2",
            "category": "Technical Skills",
            "topic": "Data Structures",
            "difficulty": "Medium",
            "question": "Which structure follows the LIFO principle?",
            "options": [
                {
                    "id": "A",
                    "label": "Queue",
                    "description": "First in, first out."
                },
                {
                    "id": "B",
                    "label": "Stack",
                    "description": "Last in, first out."
                },
                {
                    "id": "C",
                    "label": "Graph",
                    "description": "Stores connected nodes."
                },
                {
                    "id": "D",
                    "label": "Heap",
                    "description": "Maintains priority ordering."
                }
            ],
            "correct_answer": "B"
        },

        {
            "id": "technical-skills-3",
            "category": "Technical Skills",
            "topic": "Web Fundamentals",
            "difficulty": "Medium",
            "question": "Which HTTP method is normally used to retrieve a resource?",
            "options": [
                {
                    "id": "A",
                    "label": "POST",
                    "description": "Creates or submits data."
                },
                {
                    "id": "B",
                    "label": "GET",
                    "description": "Retrieves a resource."
                },
                {
                    "id": "C",
                    "label": "PUT",
                    "description": "Replaces a resource."
                },
                {
                    "id": "D",
                    "label": "DELETE",
                    "description": "Removes a resource."
                }
            ],
            "correct_answer": "B"
        },

        {
            "id": "technical-skills-4",
            "category": "Technical Skills",
            "topic": "Algorithms",
            "difficulty": "Medium",
            "question": "What is the time complexity of binary search on sorted data?",
            "options": [
                {
                    "id": "A",
                    "label": "O(n)",
                    "description": "Linear search."
                },
                {
                    "id": "B",
                    "label": "O(log n)",
                    "description": "Halves the search space each step."
                },
                {
                    "id": "C",
                    "label": "O(n²)",
                    "description": "Quadratic growth."
                },
                {
                    "id": "D",
                    "label": "O(1)",
                    "description": "Constant time."
                }
            ],
            "correct_answer": "B"
        },

        {
            "id": "technical-skills-5",
            "category": "Technical Skills",
            "topic": "Databases",
            "difficulty": "Medium",
            "question": "Which SQL clause filters grouped results?",
            "options": [
                {
                    "id": "A",
                    "label": "WHERE",
                    "description": "Filters rows before grouping."
                },
                {
                    "id": "B",
                    "label": "HAVING",
                    "description": "Filters grouped results."
                },
                {
                    "id": "C",
                    "label": "ORDER BY",
                    "description": "Sorts results."
                },
                {
                    "id": "D",
                    "label": "JOIN",
                    "description": "Combines tables."
                }
            ],
            "correct_answer": "B"
        },

        # ====================================================
        # APTITUDE
        # ====================================================

        {
            "id": "aptitude-1",
            "category": "Aptitude",
            "topic": "Logical Reasoning",
            "difficulty": "Medium",
            "question": "If all A are B and all B are C, what follows?",
            "options": [
                {
                    "id": "A",
                    "label": "All C are A",
                    "description": "Not necessarily."
                },
                {
                    "id": "B",
                    "label": "All A are C",
                    "description": "This follows logically."
                },
                {
                    "id": "C",
                    "label": "No A are C",
                    "description": "Contradicts the statements."
                },
                {
                    "id": "D",
                    "label": "All C are B",
                    "description": "Not necessarily."
                }
            ],
            "correct_answer": "B"
        },

        {
            "id": "aptitude-2",
            "category": "Aptitude",
            "topic": "Quantitative Reasoning",
            "difficulty": "Medium",
            "question": "A task takes 4 hours at a constant rate. How much is completed in 1 hour?",
            "options": [
                {
                    "id": "A",
                    "label": "10%",
                    "description": "Too low."
                },
                {
                    "id": "B",
                    "label": "25%",
                    "description": "One quarter of the task."
                },
                {
                    "id": "C",
                    "label": "40%",
                    "description": "Too high."
                },
                {
                    "id": "D",
                    "label": "75%",
                    "description": "Too high."
                }
            ],
            "correct_answer": "B"
        },

        {
            "id": "aptitude-3",
            "category": "Aptitude",
            "topic": "Pattern Recognition",
            "difficulty": "Medium",
            "question": "Find the next number: 2, 4, 8, 16, ?",
            "options": [
                {
                    "id": "A",
                    "label": "18",
                    "description": "Does not continue doubling."
                },
                {
                    "id": "B",
                    "label": "24",
                    "description": "Does not continue doubling."
                },
                {
                    "id": "C",
                    "label": "32",
                    "description": "Each number doubles."
                },
                {
                    "id": "D",
                    "label": "30",
                    "description": "Does not continue doubling."
                }
            ],
            "correct_answer": "C"
        },

        {
            "id": "aptitude-4",
            "category": "Aptitude",
            "topic": "Logical Reasoning",
            "difficulty": "Medium",
            "question": "Which is the odd one out?",
            "options": [
                {
                    "id": "A",
                    "label": "Triangle",
                    "description": "A polygon."
                },
                {
                    "id": "B",
                    "label": "Square",
                    "description": "A polygon."
                },
                {
                    "id": "C",
                    "label": "Circle",
                    "description": "Not a polygon."
                },
                {
                    "id": "D",
                    "label": "Rectangle",
                    "description": "A polygon."
                }
            ],
            "correct_answer": "C"
        },

        {
            "id": "aptitude-5",
            "category": "Aptitude",
            "topic": "Quantitative Reasoning",
            "difficulty": "Medium",
            "question": "A train travels 60 km in one hour. What is its speed?",
            "options": [
                {
                    "id": "A",
                    "label": "30 km/h",
                    "description": "Half the distance."
                },
                {
                    "id": "B",
                    "label": "60 km/h",
                    "description": "Distance per hour."
                },
                {
                    "id": "C",
                    "label": "90 km/h",
                    "description": "Too high."
                },
                {
                    "id": "D",
                    "label": "120 km/h",
                    "description": "Double the distance."
                }
            ],
            "correct_answer": "B"
        },

        # ====================================================
        # COMMUNICATION
        # ====================================================

        {
            "id": "communication-1",
            "category": "Communication",
            "topic": "Professional Communication",
            "difficulty": "Easy",
            "question": "What is the clearest way to confirm understanding in a meeting?",
            "options": [
                {
                    "id": "A",
                    "label": "Interrupt immediately",
                    "description": "Can disrupt the speaker."
                },
                {
                    "id": "B",
                    "label": "Summarize the key point",
                    "description": "Confirms shared understanding."
                },
                {
                    "id": "C",
                    "label": "Ignore unclear details",
                    "description": "Creates confusion."
                },
                {
                    "id": "D",
                    "label": "Change the subject",
                    "description": "Avoids the issue."
                }
            ],
            "correct_answer": "B"
        },

        {
            "id": "communication-2",
            "category": "Communication",
            "topic": "Written Communication",
            "difficulty": "Easy",
            "question": "Which email subject is most specific?",
            "options": [
                {
                    "id": "A",
                    "label": "Hello",
                    "description": "Too vague."
                },
                {
                    "id": "B",
                    "label": "Important",
                    "description": "Does not explain the topic."
                },
                {
                    "id": "C",
                    "label": "Meeting",
                    "description": "Missing context."
                },
                {
                    "id": "D",
                    "label": "Project Alpha review – Friday",
                    "description": "Clear topic and timing."
                }
            ],
            "correct_answer": "D"
        },

        {
            "id": "communication-3",
            "category": "Communication",
            "topic": "Feedback",
            "difficulty": "Easy",
            "question": "Constructive feedback should primarily be?",
            "options": [
                {
                    "id": "A",
                    "label": "Personal",
                    "description": "Focus on the person."
                },
                {
                    "id": "B",
                    "label": "Specific and actionable",
                    "description": "Helps the receiver improve."
                },
                {
                    "id": "C",
                    "label": "Public by default",
                    "description": "May embarrass people."
                },
                {
                    "id": "D",
                    "label": "Delayed indefinitely",
                    "description": "Loses usefulness."
                }
            ],
            "correct_answer": "B"
        },

        {
            "id": "communication-4",
            "category": "Communication",
            "topic": "Active Listening",
            "difficulty": "Easy",
            "question": "What is active listening?",
            "options": [
                {
                    "id": "A",
                    "label": "Waiting to speak",
                    "description": "This does not demonstrate listening."
                },
                {
                    "id": "B",
                    "label": "Interrupting frequently",
                    "description": "Interruptions reduce understanding."
                },
                {
                    "id": "C",
                    "label": "Paying attention and responding thoughtfully",
                    "description": "This demonstrates active listening."
                },
                {
                    "id": "D",
                    "label": "Ignoring the speaker",
                    "description": "Prevents understanding."
                }
            ],
            "correct_answer": "C"
        },

        {
            "id": "communication-5",
            "category": "Communication",
            "topic": "Team Communication",
            "difficulty": "Easy",
            "question": "What helps communication in a collaborative team?",
            "options": [
                {
                    "id": "A",
                    "label": "Keeping information secret",
                    "description": "Teams need information sharing."
                },
                {
                    "id": "B",
                    "label": "Clear and respectful communication",
                    "description": "Supports collaboration."
                },
                {
                    "id": "C",
                    "label": "Ignoring team members",
                    "description": "Reduces participation."
                },
                {
                    "id": "D",
                    "label": "Avoiding responsibilities",
                    "description": "Reduces accountability."
                }
            ],
            "correct_answer": "B"
        },

        # ====================================================
        # PROBLEM SOLVING
        # ====================================================

        {
            "id": "problem-solving-1",
            "category": "Problem Solving",
            "topic": "Debugging",
            "difficulty": "Medium",
            "question": "What is the best first step when debugging an unfamiliar issue?",
            "options": [
                {
                    "id": "A",
                    "label": "Change many things at once",
                    "description": "Makes causes harder to isolate."
                },
                {
                    "id": "B",
                    "label": "Reproduce and isolate the problem",
                    "description": "Creates reliable evidence."
                },
                {
                    "id": "C",
                    "label": "Delete the code",
                    "description": "Loses information."
                },
                {
                    "id": "D",
                    "label": "Ignore logs",
                    "description": "Removes useful clues."
                }
            ],
            "correct_answer": "B"
        },

        {
            "id": "problem-solving-2",
            "category": "Problem Solving",
            "topic": "Critical Thinking",
            "difficulty": "Medium",
            "question": "When a solution fails, what is a useful next step?",
            "options": [
                {
                    "id": "A",
                    "label": "Repeat it unchanged",
                    "description": "Provides no new information."
                },
                {
                    "id": "B",
                    "label": "Review assumptions and evidence",
                    "description": "Helps identify the cause."
                },
                {
                    "id": "C",
                    "label": "Blame the user",
                    "description": "Does not solve the issue."
                },
                {
                    "id": "D",
                    "label": "Stop immediately",
                    "description": "Ends the investigation."
                }
            ],
            "correct_answer": "B"
        },

        {
            "id": "problem-solving-3",
            "category": "Problem Solving",
            "topic": "Problem Analysis",
            "difficulty": "Medium",
            "question": "What is a good approach to a complex problem?",
            "options": [
                {
                    "id": "A",
                    "label": "Solve everything at once",
                    "description": "Can make the problem harder to manage."
                },
                {
                    "id": "B",
                    "label": "Break it into smaller manageable parts",
                    "description": "Makes analysis easier."
                },
                {
                    "id": "C",
                    "label": "Ignore dependencies",
                    "description": "Dependencies can affect the solution."
                },
                {
                    "id": "D",
                    "label": "Avoid planning",
                    "description": "Planning often improves outcomes."
                }
            ],
            "correct_answer": "B"
        },

        {
            "id": "problem-solving-4",
            "category": "Problem Solving",
            "topic": "Decision Making",
            "difficulty": "Medium",
            "question": "What is useful when comparing multiple solutions?",
            "options": [
                {
                    "id": "A",
                    "label": "Choose the first idea",
                    "description": "Options should be evaluated."
                },
                {
                    "id": "B",
                    "label": "Evaluate advantages and disadvantages",
                    "description": "Supports an informed choice."
                },
                {
                    "id": "C",
                    "label": "Ignore constraints",
                    "description": "Constraints affect feasibility."
                },
                {
                    "id": "D",
                    "label": "Avoid analysis",
                    "description": "Analysis supports decisions."
                }
            ],
            "correct_answer": "B"
        },

        {
            "id": "problem-solving-5",
            "category": "Problem Solving",
            "topic": "Testing",
            "difficulty": "Medium",
            "question": "Why should a solution be tested?",
            "options": [
                {
                    "id": "A",
                    "label": "To make the process longer",
                    "description": "Testing has a practical purpose."
                },
                {
                    "id": "B",
                    "label": "To verify that it works correctly",
                    "description": "Testing validates the solution."
                },
                {
                    "id": "C",
                    "label": "To avoid feedback",
                    "description": "Feedback can improve solutions."
                },
                {
                    "id": "D",
                    "label": "To skip implementation",
                    "description": "Testing follows implementation work."
                }
            ],
            "correct_answer": "B"
        }
    ]
}


# ============================================================
# REQUEST SCHEMA
# ============================================================

class AssessmentSubmitRequest(BaseModel):
    assessment_id: str
    answers: Dict[str, str]


# ============================================================
# GET CURRENT ASSESSMENT
# ============================================================

@router.get("/current")
def get_current_assessment(
    current_user=Depends(get_current_user)
):
    return {
        "id": ASSESSMENT["id"],
        "title": ASSESSMENT["title"],
        "questions": [
            {
                "id": question["id"],
                "category": question["category"],
                "topic": question["topic"],
                "difficulty": question["difficulty"],
                "question": question["question"],
                "options": question["options"]
            }
            for question in ASSESSMENT["questions"]
        ]
    }


# ============================================================
# SUBMIT ASSESSMENT
# ============================================================

@router.post("/submit")
def submit_assessment(
    request: AssessmentSubmitRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if request.assessment_id != ASSESSMENT["id"]:
        raise HTTPException(
            status_code=404,
            detail="Assessment not found"
        )

    # Find the student's profile
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

    question_map = {
        question["id"]: question
        for question in ASSESSMENT["questions"]
    }

    correct_answers = 0

    category_total = {}
    category_correct = {}

    # Calculate scores
    for question in ASSESSMENT["questions"]:

        category = question["category"]

        category_total[category] = (
            category_total.get(category, 0) + 1
        )

        category_correct.setdefault(category, 0)

        user_answer = request.answers.get(
            question["id"]
        )

        if user_answer == question["correct_answer"]:
            correct_answers += 1
            category_correct[category] += 1

    total_questions = len(
        ASSESSMENT["questions"]
    )

    answered_questions = sum(
        1
        for question_id in question_map
        if question_id in request.answers
    )

    overall_score = (
        round(
            (correct_answers / total_questions) * 100
        )
        if total_questions
        else 0
    )

    category_scores = {}

    for category in category_total:
        category_scores[category] = round(
            (
                category_correct[category]
                / category_total[category]
            ) * 100
        )

    # ========================================================
    # SAVE RESULT TO DATABASE
    # ========================================================

    result = AssessmentResult(
        student_id=student.student_id,
        assessment_id=ASSESSMENT["id"],
        overall_score=overall_score,
        technical_score=category_scores.get(
            "Technical Skills",
            0
        ),
        aptitude_score=category_scores.get(
            "Aptitude",
            0
        ),
        communication_score=category_scores.get(
            "Communication",
            0
        ),
        problem_solving_score=category_scores.get(
            "Problem Solving",
            0
        )
    )

    db.add(result)
    db.commit()
    db.refresh(result)

    return {
        "result_id": result.result_id,
        "assessment_id": ASSESSMENT["id"],
        "student_id": student.student_id,
        "total_questions": total_questions,
        "answered_questions": answered_questions,
        "correct_answers": correct_answers,
        "overall_score": overall_score,
        "category_scores": category_scores,
        "status": "completed"
    }


# ============================================================
# GET LATEST ASSESSMENT RESULT
# ============================================================

@router.get("/result")
def get_assessment_result(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Find the logged-in student's profile
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

    # Get the latest assessment result
    result = (
        db.query(AssessmentResult)
        .filter(
            AssessmentResult.student_id
            == student.student_id
        )
        .order_by(
            AssessmentResult.completed_at.desc()
        )
        .first()
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="No assessment result found"
        )

    return {
        "result_id": result.result_id,
        "assessment_id": result.assessment_id,
        "student_id": result.student_id,
        "overall_score": result.overall_score,
        "category_scores": {
            "Technical Skills": result.technical_score,
            "Aptitude": result.aptitude_score,
            "Communication": result.communication_score,
            "Problem Solving": result.problem_solving_score
        },
        "completed_at": result.completed_at,
        "status": "completed"
    }