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
]

KEEP_KEYWORDS = {
    "llm", "large-language-model", "ai", "artificial-intelligence", "machine-learning",
    "deep-learning", "reinforcement-learning", "rl", "agent", "agents", "inference",
    "serving", "model-serving", "cuda", "triton", "pytorch", "mlops", "evaluation",
    "benchmark", "rag", "transformer", "alignment", "rlhf", "vllm", "sglang",
}

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

def relevant(r: dict) -> bool:
    text = " ".join([
        r.get("repo") or "",
        r.get("description") or "",
        " ".join(r.get("topics") or []),
    ]).lower()
    return any(k in text for k in KEEP_KEYWORDS)

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
    for query in QUERIES:
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
        "queries": QUERIES,
        "errors": errors,
        "repos": sorted(repos, key=lambda x: x["repo"].lower()),
        "high_star_top10": high_star,
        "growth_top10": growth,
    }
    out_path = state_dir / f"github-stars-{args.date}.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"snapshot": str(out_path), "repos": len(repos), "cold_start": cold_start, "errors": errors[:3]}, ensure_ascii=False))

if __name__ == "__main__":
    main()
