from sqlalchemy import select
from app.repo.models.subject.student_scores_model import StudentScoreModel
from app.repo.schemas.subject_schemas.all_questions_schemas import SubmittedQuestions, SubmittedQ
from app.repo.queries.subject_queries.all_question_queries import AllQuestionQueries
from uuid import UUID
from datetime import datetime
from app.repo.schemas.subject_schemas.subject_score_schemas import AddScoreSchemas

class AllScoresQueries:
    def __init__(self, session):
        self.session = session
        self.qa_query = AllQuestionQueries(session)

    async def check_score_exist(self, student_id: UUID, subject_id: UUID):
        res = await self.session.execute(
            select(StudentScoreModel)
            .where(StudentScoreModel.student_id == student_id)
            .where(StudentScoreModel.subject_id == subject_id)
        )
        return res.scalar_one_or_none()

    async def process_score(self, submission: SubmittedQuestions[SubmittedQ]):
        # ✅ Prevent duplicate score entry
        existing = await self.check_score_exist(
            student_id=submission.studentId,
            subject_id=submission.subjectId
        )
        if existing:
            return False

        
        all_questions = await self.qa_query.get_only_id_and_answer(subject_id=submission.subjectId)
        total_questions = len(all_questions)

        
        correct_answer_map = {str(q.id): q.answer for q in all_questions}

        # ✅ Count correct answers
        correct_answers = sum(
            1 for ans in submission.answers
            if str(ans.id) in correct_answer_map and ans.answer.lower() == correct_answer_map[str(ans.id)].lower()
        )

        # ✅ Calculate score
        score_value = (correct_answers / total_questions) * 100 if total_questions > 0 else 0

        # ✅ Create score entry
        new_score = StudentScoreModel(
            score=score_value,
            total_questions=total_questions,
            correct_answers=correct_answers,
            attempt_number=1,
            exam_status="submitted",
            created_at=datetime.now(),
            student_id=submission.studentId,
            subject_id=submission.subjectId
        )

        self.session.add(new_score)
        await self.session.commit()

        return AddScoreSchemas(
            score=int(score_value),
            total_questions=total_questions,
            correct_answers=correct_answers,
            attempt_number=1,
            exam_status="submitted",
            student_id=submission.studentId,
            subject_id=submission.subjectId
        )
