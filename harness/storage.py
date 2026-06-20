from sqlmodel import SQLModel, Field, create_engine, Session
from datetime import datetime
from pathlib import Path
from typing import Optional


class EvalRun(SQLModel, table=True):
    """Represents a single eval run."""
    id: Optional[int] = Field(default=None, primary_key=True)
    run_id: str = Field(index=True)  # e.g., "run_20260426_143022"
    suite_name: str
    model: str
    scorer: str
    timestamp: datetime = Field(default_factory=datetime.now)
    total_cases: int
    passed_cases: int

class CaseResult(SQLModel, table=True):
    """Represents a single test case result."""
    id: Optional[int] = Field(default=None, primary_key=True)
    run_id: str = Field(index=True)
    case_id: str
    prompt: str
    expected: str
    actual: str
    score: float
    passed: bool

DB_PATH = Path.home() / ".harness" / "results.db"
DB_PATH.parent.mkdir(exist_ok=True)

engine = create_engine(f"sqlite:///{DB_PATH}")

def init_db():
    """Create tables if they don't exist."""
    SQLModel.metadata.create_all(engine)