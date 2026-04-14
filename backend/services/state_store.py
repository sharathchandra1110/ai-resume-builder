import json
from pathlib import Path
from threading import Lock
from typing import Any, Dict, Optional

from backend.models.jd_models import JobDescription
from backend.models.profile_models import UserProfile


DATA_DIR = Path(__file__).resolve().parents[1] / "data"
STATE_FILE = DATA_DIR / "app_state.json"


def _model_dump(model: Any) -> Dict[str, Any]:
    if hasattr(model, "model_dump"):
        return model.model_dump()
    return model.dict()


class AppStateStore:
    def __init__(self, state_file: Path = STATE_FILE):
        self.state_file = state_file
        self._lock = Lock()
        self.state_file.parent.mkdir(parents=True, exist_ok=True)

    def _read_state(self) -> Dict[str, Any]:
        if not self.state_file.exists():
            return {}

        try:
            return json.loads(self.state_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}

    def _write_state(self, state: Dict[str, Any]) -> None:
        self.state_file.write_text(
            json.dumps(state, indent=2, ensure_ascii=True),
            encoding="utf-8",
        )

    def save_profile(self, profile: UserProfile) -> None:
        with self._lock:
            state = self._read_state()
            state["profile"] = _model_dump(profile)
            self._write_state(state)

    def get_profile(self) -> Optional[UserProfile]:
        state = self._read_state()
        profile_data = state.get("profile")
        if not profile_data:
            return None
        return UserProfile(**profile_data)

    def save_job_description(self, job_description: JobDescription) -> None:
        with self._lock:
            state = self._read_state()
            state["job_description"] = _model_dump(job_description)
            self._write_state(state)

    def get_job_description(self) -> Optional[JobDescription]:
        state = self._read_state()
        job_description_data = state.get("job_description")
        if not job_description_data:
            return None

        if isinstance(job_description_data, str):
            return JobDescription(jd_text=job_description_data)

        return JobDescription(**job_description_data)

    def clear(self) -> None:
        with self._lock:
            self._write_state({})

    def snapshot(self) -> Dict[str, bool]:
        state = self._read_state()
        return {
            "profile_loaded": bool(state.get("profile")),
            "job_description_loaded": bool(state.get("job_description")),
        }
