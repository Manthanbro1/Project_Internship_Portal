# backend/app/services/recommendation.py
from sqlalchemy.orm import Session

from ..models.project import Project
from ..models.internship import Internship
from ..models.student_profile import StudentProfile
from ..utils.text_processsing import clean_text
from ..utils.simmilarity import compute_similarity
def recommend_internships_for_student(student_id: int, db: Session):
    profile = db.query(StudentProfile).filter(
        StudentProfile.user_id == student_id
    ).first()

    projects = db.query(Project).filter(
        Project.student_id == student_id
    ).all()

    if not projects:
        return []

    student_text = " ".join(
        filter(None, [
            profile.about_me if profile else "",
            *[p.description for p in projects],
            *[p.student_role for p in projects]
        ])
    )

    student_text = clean_text(student_text)

    internships = db.query(Internship).all()

    internship_texts = [
        clean_text(i.role_description + " " + (i.required_skills or ""))
        for i in internships
    ]

    scores = compute_similarity(student_text, internship_texts)

    results = []
    for internship, score in zip(internships, scores):
        results.append({
            "internship_id": internship.id,
            "role_title": internship.role_title,
            "similarity_score": round(score * 100, 2)
        })

    return sorted(results, key=lambda x: x["similarity_score"], reverse=True)

def recommend_projects_for_internship(internship_id: int, db: Session):
    internship = db.query(Internship).filter(
        Internship.id == internship_id
    ).first()

    if not internship:
        return []

    internship_text = clean_text(
        internship.role_description + " " + (internship.required_skills or "")
    )

    projects = db.query(Project).all()

    project_texts = [
        clean_text(p.description + " " + p.student_role)
        for p in projects
    ]

    scores = compute_similarity(internship_text, project_texts)

    results = []
    for project, score in zip(projects, scores):
        results.append({
            "project_id": project.id,
            "title": project.title,
            "similarity_score": round(score * 100, 2)
        })

    return sorted(results, key=lambda x: x["similarity_score"], reverse=True)
