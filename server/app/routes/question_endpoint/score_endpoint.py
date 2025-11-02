from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from app.repo.schemas.subject_schemas.all_questions_schemas import SubmittedQuestions, SubmittedQ
from app.repo.queries.subject_queries.all_scores_quires import AllScoresQueries
from app.repo.schemas.default_server_res import DefaultServerApiRes
from app.repo.schemas.subject_schemas.subject_score_schemas import AddScoreSchemas, ScoreIdInfo
from app.repo import db_injection
from typing import Annotated
from app.security.token_generator import verify_token


score_endpoint = APIRouter(prefix="/score", tags=["Exam Scoring"])

@score_endpoint.post("/submit_exam_result", response_model=DefaultServerApiRes[AddScoreSchemas])
async def submit_exam_result(
    db: db_injection,
        current_user: Annotated[dict, Depends(verify_token)],
    submission: SubmittedQuestions[SubmittedQ]
):
    score_query = AllScoresQueries(db)
    result = await score_query.process_score(submission)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Score already exists for this student and subject."
        )

    return DefaultServerApiRes(
        statusCode=200,
        message="Exam graded successfully.",
        data=result
    )



@score_endpoint.post("/check_proceed_exam", response_model=DefaultServerApiRes[bool])
async def check_proceed_exam(db:db_injection, current_user: Annotated[dict, Depends(verify_token)], details: ScoreIdInfo):
    score_query = AllScoresQueries(db)
    status = await score_query.check_score_exist(student_id=details.studentId, subject_id=details.subjectId)
    if status:
        return JSONResponse(
        status_code=400,
        content={"message": "you have already taken this exam", "data": False},

        )
    return DefaultServerApiRes(
        statusCode=200,
        message="you have already taken this exam",
        data=True
        )