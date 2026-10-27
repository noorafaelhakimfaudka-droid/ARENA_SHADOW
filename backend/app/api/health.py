from fastapi import APIRouter
from backend.app.config import settings
from backend.app.schemas import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def check_health() -> HealthResponse:
    from backend.app.services.llm import get_llm_status
    has_llm, reason = get_llm_status()

    return HealthResponse(
        ok=True,
        llm=has_llm,
        model=settings.gemini_model if has_llm else "",
        offline_reason=reason
    )
