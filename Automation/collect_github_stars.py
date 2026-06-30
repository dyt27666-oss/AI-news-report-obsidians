#!/usr/bin/env python3
"""Collect GitHub AI Radar star snapshots for high-star and growth tables."""
from __future__ import annotations

import argparse
import json
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List

QUERIES = [
    "topic:artificial-intelligence stars:>1000",
    "topic:llm stars:>500",
    "topic:machine-learning stars:>1000",
    "topic:reinforcement-learning stars:>100",
    "topic:agents stars:>100",
    "topic:inference stars:>100",
    "topic:cuda stars:>100",
    "topic:triton stars:>50",
    "vllm OR sglang OR tensorrt-llm",
    "grpo OR rlhf OR verl OR openrlhf",
    "point rummy OR indian rummy OR rummy ai",
    "rummy reinforcement learning OR rummy bot OR rummy simulation",
    "loop engineering OR loop engineer OR harness engineering",
    "coding agent loop OR agent loop design OR AGENTS.md harness",
]

THEME_QUERIES = {
    "point_rummy": [
        "point rummy",
        "indian rummy",
        "rummy ai",
        "rummy reinforcement learning",
        "gin rummy ai",
    ],
    "loop_engineer": [
        "loop engineering",
        "loop engineer",
        "harness engineering",
        "coding agent loop",
        "AGENTS.md harness",
    ],
}

KEEP_KEYWORDS = {
    "llm", "large-language-model", "ai", "artificial-intelligence", "machine-learning",
    "deep-learning", "reinforcement-learning", "rl", "agent", "agents", "inference",
    "serving", "model-serving", "cuda", "triton", "pytorch", "mlops", "evaluation",
    "benchmark", "rag", "transformer", "alignment", "rlhf", "vllm", "sglang",
    "rummy", "indian-rummy", "point-rummy", "gin-rummy", "card-game", "mcts", "ismcts",
    "loop-engineering", "loop", "harness", "coding-agent", "agents-md", "context-engineering",
}

POINT_RUMMY_TERMS = ("rummy", "indian rummy", "point rummy", "gin rummy")
LOOP_ENGINEER_TERMS = (
    "loop engineering", "loop-engineering", "loop engineer", "harness engineering",
    "coding agent loop", "agent loop", "agents.md", "context engineering",
)

def fetch_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "ai-radar-github-snapshot"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))

def search_repos(query: str, sort: str, per_page: int = 20) -> List[dict]:
    params = urllib.parse.urlencode({"q": query, "sort": sort, "order": "desc", "per_page": per_page})
    data = fetch_json(f"https://api.github.com/search/repositories?{params}")
    return data.get("items", [])

def normalize(repo: dict, collected_at: str) -> dict:
    return {
        "repo": repo.get("full_name"),
        "stars": repo.get("stargazers_count", 0),
        "forks": repo.get("forks_count", 0),
        "language": repo.get("language") or "Unknown",
        "updated_at": repo.get("updated_at"),
        "pushed_at": repo.get("pushed_at"),
        "topics": repo.get("topics", []),
        "html_url": repo.get("html_url"),
        "description": repo.get("description") or "",
        "collected_at": collected_at,
    }

def repo_text(r: dict) -> str:
    return " ".join([
        r.get("repo") or "",
        r.get("description") or "",
        " ".join(r.get("topics") or []),
    ]).lower()


def relevant(r: dict) -> bool:
    text = repo_text(r)
    return any(k in text for k in KEEP_KEYWORDS)


def tag_themes(item: dict) -> list[str]:
    text = repo_text(item)
    themes = []
    if any(term in text for term in POINT_RUMMY_TERMS):
        themes.append("point_rummy")
    if any(term in text for term in LOOP_ENGINEER_TERMS):
        themes.append("loop_engineer")
    return themes


def theme_top(repos: list[dict], theme: str, limit: int) -> dict:
    items = [r for r in repos if theme in (r.get("themes") or [])]
    high_star = sorted(items, key=lambda x: (x.get("stars") or 0), reverse=True)[:limit]
    growth = sorted(
        items,
        key=lambda x: (x.get("stars_delta") if x.get("stars_delta") is not None else -1, x.get("updated_at") or ""),
        reverse=True,
    )[:limit]
    return {"repos": items, "high_star_top10": high_star, "growth_top10": growth}


def previous_snapshot(state_dir: Path, date: str) -> Dict[str, dict]:
    files = sorted(p for p in state_dir.glob("github-stars-*.json") if date not in p.name)
    if not files:
        return {}
    data = json.loads(files[-1].read_text(encoding="utf-8"))
    return {x.get("repo"): x for x in data.get("repos", []) if x.get("repo")}

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--vault", default=".")
    ap.add_argument("--date", required=True)
    ap.add_argument("--limit", type=int, default=10)
    args = ap.parse_args()

    vault = Path(args.vault)
    state_dir = vault / "Automation" / "state"
    state_dir.mkdir(parents=True, exist_ok=True)
    collected_at = datetime.now(timezone.utc).isoformat()

    by_repo: Dict[str, dict] = {}
    errors = []
    # Theme-specific queries run first so niche business topics are not lost if
    # GitHub's unauthenticated search quota is exhausted by broad AI queries.
    all_queries = []
    for queries in THEME_QUERIES.values():
        all_queries.extend(queries)
    all_queries.extend(QUERIES)

    for query in all_queries:
        for sort in ("stars", "updated"):
            try:
                for repo in search_repos(query, sort):
                    item = normalize(repo, collected_at)
                    if item["repo"] and relevant(item):
                        by_repo[item["repo"]] = item
                time.sleep(0.3)
            except Exception as exc:
                errors.append({"query": query, "sort": sort, "error": str(exc)})

    repos = list(by_repo.values())
    prev = previous_snapshot(state_dir, args.date)
    cold_start = not bool(prev)
    for item in repos:
        old = prev.get(item["repo"])
        item["stars_delta"] = None if old is None else item["stars"] - int(old.get("stars", 0))
        item["growth_basis"] = "historical_snapshot" if old else "cold_start_proxy_updated_or_stars"
        item["themes"] = tag_themes(item)

    theme_sections = {theme: theme_top(repos, theme, args.limit) for theme in THEME_QUERIES}

    high_star = sorted(repos, key=lambda x: (x.get("stars") or 0), reverse=True)[: args.limit]
    if cold_start:
        growth = sorted(repos, key=lambda x: (x.get("updated_at") or "", x.get("stars") or 0), reverse=True)[: args.limit]
    else:
        growth = sorted(repos, key=lambda x: (x.get("stars_delta") if x.get("stars_delta") is not None else -1), reverse=True)[: args.limit]

    out = {
        "date": args.date,
        "collected_at": collected_at,
        "cold_start": cold_start,
        "baseline_available": not cold_start,
        "queries": all_queries,
        "theme_queries": THEME_QUERIES,
        "errors": errors,
        "repos": sorted(repos, key=lambda x: x["repo"].lower()),
        "high_star_top10": high_star,
        "growth_top10": growth,
        "theme_sections": theme_sections,
    }
    out_path = state_dir / f"github-stars-{args.date}.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"snapshot": str(out_path), "repos": len(repos), "cold_start": cold_start, "errors": errors[:3]}, ensure_ascii=False))

if __name__ == "__main__":
    main()
