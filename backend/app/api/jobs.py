from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from backend.app.services.jobs import job_runner

router = APIRouter(tags=["jobs"])


@router.get("/jobs/{job_id}/events")
async def get_job_events(job_id: str):
    """
    Server-Sent Events (SSE) streaming endpoint untuk progres nyata
    pipeline Machine Learning dan perakitan debat.
    """
    return StreamingResponse(
        job_runner.event_generator(job_id),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )
