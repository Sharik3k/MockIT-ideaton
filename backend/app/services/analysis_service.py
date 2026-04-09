from typing import Dict, Any, List, Set
from ..core.store import store
from ..schemas.analysis import MockMatchResponse, MockQuestionsResponse, QuestionItem

def calculate_match_score(candidate_skills: List[str], must_have_skills: List[str], 
                         nice_to_have_skills: List[str]) -> int:
    """Calculate match score based on skill overlap."""
    if not must_have_skills:
        return 85  # Default score if no must-have skills
    
    candidate_skills_set = set(skill.lower() for skill in candidate_skills)
    must_have_set = set(skill.lower() for skill in must_have_skills)
    
    matched_must_have = len(candidate_skills_set & must_have_set)
    total_must_have = len(must_have_set)
    
    if total_must_have == 0:
        return 85
    
    # Base score from must-have skills (70% weight)
    must_have_score = (matched_must_have / total_must_have) * 70
    
    # Bonus for nice-to-have skills (30% weight)
    if nice_to_have_skills:
        nice_to_have_set = set(skill.lower() for skill in nice_to_have_skills)
        matched_nice_to_have = len(candidate_skills_set & nice_to_have_set)
        total_nice_to_have = len(nice_to_have_set)
        nice_to_have_score = (matched_nice_to_have / total_nice_to_have) * 30
    else:
        nice_to_have_score = 15  # Default bonus
    
    total_score = int(must_have_score + nice_to_have_score)
    return min(100, max(0, total_score))

def generate_risks(candidate_skills: List[str], missing_skills: List[str], 
                  candidate_notes: str) -> List[str]:
    """Generate risk factors for candidate-vacancy match."""
    risks = []
    
    if not candidate_skills:
        risks.append("Limited skill data available")
    
    if len(missing_skills) > 2:
        risks.append("Several required skills are missing")
    
    if candidate_notes and ("pet project" in candidate_notes.lower() or 
                           "personal project" in candidate_notes.lower()):
        risks.append("No clear commercial experience")
    
    if not candidate_notes or len(candidate_notes.strip()) < 10:
        risks.append("Limited candidate information available")
    
    return risks

def mock_match_analysis(candidate_id: str, vacancy_id: str, workspace_id: str) -> MockMatchResponse:
    """Generate mock match analysis between candidate and vacancy."""
    # Get candidate and vacancy
    candidate = store.get_candidate_by_id(candidate_id)
    vacancy = store.get_vacancy_by_id(vacancy_id)
    
    if not candidate or candidate.get("workspaceId") != workspace_id:
        raise ValueError("Candidate not found or access denied")
    
    if not vacancy or vacancy.get("workspaceId") != workspace_id:
        raise ValueError("Vacancy not found or access denied")
    
    # Extract skills
    candidate_skills = candidate.get("skills", [])
    must_have_skills = vacancy.get("mustHaveSkills", [])
    nice_to_have_skills = vacancy.get("niceToHaveSkills", [])
    
    # Calculate matches
    candidate_skills_set = set(skill.lower() for skill in candidate_skills)
    must_have_set = set(skill.lower() for skill in must_have_skills)
    nice_to_have_set = set(skill.lower() for skill in nice_to_have_skills)
    
    matched_skills = list(candidate_skills_set & (must_have_set | nice_to_have_set))
    missing_skills = list(must_have_set - candidate_skills_set)
    partial_skills = list(candidate_skills_set & nice_to_have_set - must_have_set)
    
    # Calculate score
    score = calculate_match_score(candidate_skills, must_have_skills, nice_to_have_skills)
    
    # Generate risks
    risks = generate_risks(candidate_skills, missing_skills, candidate.get("notes", ""))
    
    return MockMatchResponse(
        overallMatchScore=score,
        matchedSkills=matched_skills,
        missingSkills=missing_skills,
        partialSkills=partial_skills if partial_skills else None,
        risks=risks
    )

def generate_interview_questions(candidate_skills: List[str], must_have_skills: List[str],
                                nice_to_have_skills: List[str], missing_skills: List[str],
                                candidate_notes: str) -> List[QuestionItem]:
    """Generate mock interview questions."""
    questions = []
    
    # Questions for matched skills
    for skill in candidate_skills[:2]:  # Limit to first 2 skills
        if skill.lower() in [s.lower() for s in must_have_skills + nice_to_have_skills]:
            questions.append(QuestionItem(
                category="resume",
                question=f"Tell me more about your experience with {skill}.",
                whyGenerated=f"{skill} appears in both the candidate profile and vacancy requirements."
            ))
    
    # Questions for missing must-have skills
    for skill in missing_skills[:2]:  # Limit to first 2 missing skills
        questions.append(QuestionItem(
            category="skill_verification",
            question=f"How comfortable are you with {skill} in real projects?",
            whyGenerated=f"{skill} is required in the vacancy but missing from the candidate profile."
        ))
    
    # Project question if notes mention projects
    if candidate_notes and ("project" in candidate_notes.lower()):
        questions.append(QuestionItem(
            category="project",
            question="Can you walk me through your most challenging project?",
            whyGenerated="Candidate's notes mention project experience."
        ))
    
    # Always add a behavioral question
    behavioral_questions = [
        "Describe a time when you had to learn a new technology quickly.",
        "Tell me about a time you faced a technical challenge and how you solved it.",
        "How do you handle disagreements with team members?",
        "Describe your approach to debugging complex issues."
    ]
    
    questions.append(QuestionItem(
        category="behavioral",
        question=behavioral_questions[len(questions) % len(behavioral_questions)],
        whyGenerated="Behavioral assessment is important for team fit."
    ))
    
    return questions[:8]  # Return max 8 questions

def mock_questions_analysis(candidate_id: str, vacancy_id: str, workspace_id: str) -> MockQuestionsResponse:
    """Generate mock interview questions for candidate-vacancy pair."""
    # Get candidate and vacancy
    candidate = store.get_candidate_by_id(candidate_id)
    vacancy = store.get_vacancy_by_id(vacancy_id)
    
    if not candidate or candidate.get("workspaceId") != workspace_id:
        raise ValueError("Candidate not found or access denied")
    
    if not vacancy or vacancy.get("workspaceId") != workspace_id:
        raise ValueError("Vacancy not found or access denied")
    
    # Extract skills
    candidate_skills = candidate.get("skills", [])
    must_have_skills = vacancy.get("mustHaveSkills", [])
    nice_to_have_skills = vacancy.get("niceToHaveSkills", [])
    
    # Calculate missing skills
    candidate_skills_set = set(skill.lower() for skill in candidate_skills)
    must_have_set = set(skill.lower() for skill in must_have_skills)
    missing_skills = list(must_have_set - candidate_skills_set)
    
    # Generate questions
    questions = generate_interview_questions(
        candidate_skills, must_have_skills, nice_to_have_skills,
        missing_skills, candidate.get("notes", "")
    )
    
    return MockQuestionsResponse(questions=questions)
