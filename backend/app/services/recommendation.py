from sqlalchemy.orm import Session

from ..models.internship import Internship
from ..models.project import Project
from ..models.project_skill import ProjectSkill
from ..models.skill import Skill
from ..models.student_profile import StudentProfile
from ..utils.similarity import compute_similarity, overlap_ratio
from ..utils.text_processing import clean_text


def _parse_skill_text(skill_text: str | None) -> list[str]:
    if not skill_text:
        return []

    separators_normalized = skill_text.replace("/", ",").replace("|", ",")
    return [part.strip() for part in separators_normalized.split(",") if part.strip()]


def _project_skill_map(db: Session, project_ids: list[int]) -> dict[int, list[str]]:
    if not project_ids:
        return {}

    rows = (
        db.query(ProjectSkill.project_id, Skill.name)
        .join(Skill, Skill.id == ProjectSkill.skill_id)
        .filter(ProjectSkill.project_id.in_(project_ids))
        .all()
    )

    mapping: dict[int, list[str]] = {project_id: [] for project_id in project_ids}
    for project_id, skill_name in rows:
        mapping.setdefault(project_id, []).append(skill_name)
    return mapping


def _project_text(project: Project, skills: list[str]) -> str:
    return clean_text(
        " ".join(
            filter(
                None,
                [
                    project.title,
                    project.description,
                    project.student_role,
                    project.outcome,
                    " ".join(skills),
                ],
            )
        )
    )


def _internship_text(internship: Internship) -> str:
    return clean_text(
        " ".join(
            filter(
                None,
                [
                    internship.role_title,
                    internship.role_description,
                    internship.required_skills,
                ],
            )
        )
    )


def _blend_scores(text_score: float, skill_score: float, title_score: float = 0.0) -> float:
    return (text_score * 0.6) + (skill_score * 0.3) + (title_score * 0.1)


def recommend_internships_for_student(student_id: int, db: Session):
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == student_id).first()
    projects = db.query(Project).filter(Project.student_id == student_id).all()

    if not projects:
        return []

    project_ids = [project.id for project in projects]
    project_skills = _project_skill_map(db, project_ids)

    student_skill_set: list[str] = []
    project_documents: list[str] = []
    project_titles: list[str] = []
    for project in projects:
        skills = project_skills.get(project.id, [])
        student_skill_set.extend(skills)
        project_documents.append(_project_text(project, skills))
        project_titles.append(project.title)

    student_text = clean_text(
        " ".join(
            filter(
                None,
                [
                    profile.about_me if profile else "",
                    profile.department if profile else "",
                    " ".join(project_titles),
                    " ".join(project_documents),
                    " ".join(student_skill_set),
                ],
            )
        )
    )

    internships = db.query(Internship).all()
    internship_texts = [_internship_text(internship) for internship in internships]
    text_scores = compute_similarity(student_text, internship_texts)

    results = []
    for internship, text_score in zip(internships, text_scores):
        internship_skills = _parse_skill_text(internship.required_skills)
        skill_score = overlap_ratio(student_skill_set, internship_skills)
        title_score = overlap_ratio(project_titles, [internship.role_title])
        score = _blend_scores(text_score, skill_score, title_score)

        results.append(
            {
                "internship_id": internship.id,
                "role_title": internship.role_title,
                "similarity_score": round(score * 100, 2),
            }
        )

    return sorted(results, key=lambda item: item["similarity_score"], reverse=True)


def recommend_projects_for_internship(internship_id: int, db: Session):
    internship = db.query(Internship).filter(Internship.id == internship_id).first()
    if not internship:
        return []

    internship_text = _internship_text(internship)
    internship_skills = _parse_skill_text(internship.required_skills)

    projects = db.query(Project).all()
    project_ids = [project.id for project in projects]
    project_skills = _project_skill_map(db, project_ids)
    project_texts = [_project_text(project, project_skills.get(project.id, [])) for project in projects]
    text_scores = compute_similarity(internship_text, project_texts)

    results = []
    for project, text_score in zip(projects, text_scores):
        skills = project_skills.get(project.id, [])
        skill_score = overlap_ratio(internship_skills, skills)
        title_score = overlap_ratio([internship.role_title], [project.title])
        score = _blend_scores(text_score, skill_score, title_score)

        results.append(
            {
                "project_id": project.id,
                "title": project.title,
                "similarity_score": round(score * 100, 2),
            }
        )

    return sorted(results, key=lambda item: item["similarity_score"], reverse=True)
