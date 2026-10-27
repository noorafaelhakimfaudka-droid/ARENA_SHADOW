from typing import Any, Dict, List, Literal, Optional, Union
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Problem & Profile
# ---------------------------------------------------------------------------

class ProblemSpec(BaseModel):
    task: Literal["binary", "multiclass", "regression"] = "binary"
    target: str
    classes: List[str] = Field(default_factory=list)
    metric: str = "ROC-AUC"
    metric_label: str = "Area under ROC Curve"


class ClassBalanceItem(BaseModel):
    label: str
    share: float


class TopMissingItem(BaseModel):
    col: str
    pct: float


class PreviewData(BaseModel):
    cols: List[str]
    rows: List[List[Any]]


class DatasetProfile(BaseModel):
    n_numeric: int
    n_categorical: int
    missing_pct: float
    class_balance: List[ClassBalanceItem] = Field(default_factory=list)
    top_missing: List[TopMissingItem] = Field(default_factory=list)
    preview: PreviewData


# ---------------------------------------------------------------------------
# Charts
# ---------------------------------------------------------------------------

class ChartData(BaseModel):
    type: Literal["bar", "line", "roc", "confusion", "heatmap", "hist", "scatter"]
    labels: Optional[List[str]] = None
    values: Optional[List[float]] = None
    max: Optional[float] = None
    min: Optional[float] = None
    thr: Optional[float] = None
    hl: Optional[int] = None
    # Line chart properties
    x: Optional[List[str]] = None
    s: Optional[List[List[float]]] = None
    n: Optional[List[str]] = None
    # Confusion & Heatmap
    matrix: Optional[List[List[float]]] = None
    x_labels: Optional[List[str]] = None
    y_labels: Optional[List[str]] = None
    # ROC curve points
    fpr: Optional[List[float]] = None
    tpr: Optional[List[float]] = None
    auc: Optional[float] = None
    # Scatter points [{x: ..., y: ..., group: ...}]
    points: Optional[List[Dict[str, Any]]] = None


# ---------------------------------------------------------------------------
# Rounds & Reveals
# ---------------------------------------------------------------------------

class Reveals(BaseModel):
    leaderboard: Optional[bool] = None
    qa: Optional[str] = None


AgentName = Literal["wrangler", "framer", "guardian", "storyteller", "notebook"]
Mood = Literal["calm", "angry", "shock", "happy"]
Stage = Literal["PROBLEM", "DATA", "SPLIT_FE", "MODEL", "EVAL", "INSIGHT", "NOTEBOOK"]


class Round(BaseModel):
    id: int
    agent: AgentName
    title: str = Field(max_length=28)
    mood: Mood
    stage: Stage
    dialog: str = Field(max_length=190)
    evidence: str = Field(max_length=85)
    chart: ChartData
    facts: Dict[str, Any] = Field(default_factory=dict)
    reveals: Optional[Reveals] = None


# ---------------------------------------------------------------------------
# Leaderboard, QA, Notebook Info
# ---------------------------------------------------------------------------

class LeaderboardEntry(BaseModel):
    model: str
    cv_auc: float
    cv_std: float
    test_auc: Optional[float] = None
    champion: bool = False


class QAItem(BaseModel):
    key: str
    label: str
    passed: bool
    round_id: int


class NotebookMeta(BaseModel):
    filename: str = "shadow_arena.ipynb"
    valid: bool = True
    cells_count: int = 0


# ---------------------------------------------------------------------------
# Metadata & Full Debate Document
# ---------------------------------------------------------------------------

class DebateMeta(BaseModel):
    session_id: str
    dataset_name: str
    created_at: str
    mode: Literal["llm", "offline"]
    problem: ProblemSpec
    n_rows: int
    n_cols: int
    n_train: int
    n_test: int


class DebateDocument(BaseModel):
    meta: DebateMeta
    profile: DatasetProfile
    rounds: List[Round]
    leaderboard: List[LeaderboardEntry] = Field(default_factory=list)
    qa: List[QAItem] = Field(default_factory=list)
    notebook: NotebookMeta


# ---------------------------------------------------------------------------
# Session & Job APIs
# ---------------------------------------------------------------------------

class SessionSummary(BaseModel):
    session_id: str
    dataset_name: str
    target: str
    champion: Optional[str] = None
    created_at: str
    n_rows: int
    n_cols: int
    mode: str = "offline"


class JobProgressEvent(BaseModel):
    step: int
    agent: str
    message: str
    pct: int
    done: bool = False
    error: Optional[str] = None
    session_id: Optional[str] = None


class HealthResponse(BaseModel):
    ok: bool = True
    llm: bool = False
    model: str = ""
    offline_reason: Optional[str] = None
