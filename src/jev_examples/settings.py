"""Load API keys and call Jev or OpenAI from the notebooks."""

from __future__ import annotations

import os
import warnings
from pathlib import Path

from dotenv import load_dotenv

_BLANK_KEYS = (
    "TYPESAFE_API_KEY",
    "TYPESAFE_BASE_URL",
    "OPENAI_API_KEY",
    "JEV_MODEL",
    "OPENAI_MODEL",
)


def repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "pyproject.toml").exists() and (parent / "data").exists():
            return parent
    raise FileNotFoundError("Could not find the JEV project root.")


def load_env() -> None:
    # override=True so a notebook kernel picks up .env edits without a restart.
    load_dotenv(repo_root() / ".env", override=True)
    for key in _BLANK_KEYS:
        if os.environ.get(key, None) == "":
            os.environ.pop(key, None)


def typesafe_base_url() -> str:
    """Host only. The SDK appends /v1/systemone itself."""
    load_env()
    url = os.environ.get("TYPESAFE_BASE_URL", "https://api.typesafe.ai").strip().rstrip("/")
    if not url:
        url = "https://api.typesafe.ai"
    changed = True
    while changed:
        changed = False
        for suffix in ("/v1/systemone", "/v1"):
            if url.lower().endswith(suffix):
                url = url[: -len(suffix)].rstrip("/")
                changed = True
                break
    return url or "https://api.typesafe.ai"


def jev_model() -> str:
    load_env()
    return os.environ.get("JEV_MODEL", "jev-latest")


def typesafe_ready() -> bool:
    load_env()
    return bool(os.environ.get("TYPESAFE_API_KEY"))


def openai_ready() -> bool:
    load_env()
    return bool(os.environ.get("OPENAI_API_KEY"))


def _classifier():
    load_env()
    if not typesafe_ready():
        print("skipped: set TYPESAFE_API_KEY in .env")
        return None
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=Warning, message=".*beta.*")
        from langchain_typesafe import TypeSafeClassifier
        return TypeSafeClassifier(model=jev_model(), base_url=typesafe_base_url())


def ask(state, questions):
    """One Jev call. Questions share the same state and run together."""
    classifier = _classifier()
    if classifier is None:
        return None
    return classifier.invoke({"state": state, "questions": questions})


def ask_many(requests: list[dict]):
    """Several Jev calls. Each item is {"state": ..., "questions": ...}."""
    classifier = _classifier()
    if classifier is None:
        return None
    return classifier.batch(requests)


def show(response) -> None:
    """Print Choice, Score, and Noul answers in a few lines."""
    if response is None:
        return
    print(f"model: {response.model}")
    for name, answer in response.nouls.items():
        print(f"  noul   {name}: {answer.noul:.2f}")
    for name, answer in response.choices.items():
        print(f"  choice {name}: {answer.choice}  (confidence {answer.confidence:.2f})")
    for name, answer in response.scores.items():
        print(f"  score  {name}: {answer.score:.2f}{_score_label(answer)}")


def _score_label(answer) -> str:
    legend = getattr(answer, "legend", None) or {}
    if not legend:
        return ""
    keys = sorted(legend)
    index = int(round(answer.score))
    index = min(max(index, keys[0]), keys[-1])
    text = legend.get(index, "")
    if isinstance(text, dict):
        text = text.get("summary") or text.get("level") or str(text)
    return f"  ~ {text}"


def draft(prompt: str) -> str | None:
    """Ask OpenAI to write text. Decision cells should not call this."""
    load_env()
    if not openai_ready():
        print("skipped: set OPENAI_API_KEY in .env (this step writes text)")
        return None
    from langchain_openai import ChatOpenAI

    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    reply = ChatOpenAI(model=model, temperature=0).invoke(prompt)
    return reply.content
