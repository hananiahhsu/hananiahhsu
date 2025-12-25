#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate a self-hosted metrics.svg for GitHub README.

- Fetches metrics from GitHub GraphQL API
- Aggregates language sizes across (non-fork) repositories
- Builds an SVG (no external dependencies besides 'requests')
- Intended to run in GitHub Actions on a schedule and commit the result

Usage:
  python scripts/generate_metrics_svg.py --user hananiahhsu --out assets/stats/metrics.svg
Env:
  GITHUB_TOKEN (required)
"""
from __future__ import annotations

import argparse
import datetime as _dt
import os
import sys
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

import requests


GQL_ENDPOINT = "https://api.github.com/graphql"


@dataclass
class Metrics:
    updated: str
    contrib30: int
    commits30: int
    prs30: int
    stars: int
    repos: int
    followers: int
    following: int
    daily: List[int]          # daily contributions (last N days)
    languages: List[Tuple[str, int]]  # (language, bytes)


def gql(token: str, query: str, variables: dict) -> dict:
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }
    r = requests.post(GQL_ENDPOINT, json={"query": query, "variables": variables}, headers=headers, timeout=30)
    if r.status_code != 200:
        raise RuntimeError(f"GraphQL HTTP {r.status_code}: {r.text[:400]}")
    data = r.json()
    if "errors" in data:
        raise RuntimeError(f"GraphQL errors: {data['errors']}")
    return data["data"]


def iso_date(d: _dt.date) -> str:
    return d.isoformat()


def fetch_user_core(token: str, user: str, date_from: str, date_to: str) -> dict:
    query = r"""
    query($login:String!, $from:DateTime!, $to:DateTime!) {
      user(login:$login) {
        followers { totalCount }
        following { totalCount }
        repositories(ownerAffiliations: OWNER, isFork:false) { totalCount }
        contributionsCollection(from:$from, to:$to) {
          totalCommitContributions
          totalPullRequestContributions
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays { date contributionCount }
            }
          }
        }
      }
    }
    """
    return gql(token, query, {"login": user, "from": date_from, "to": date_to})


def fetch_repo_stars_and_langs_page(token: str, user: str, after: Optional[str]) -> dict:
    query = r"""
    query($login:String!, $after:String) {
      user(login:$login) {
        repositories(first: 100, after: $after, ownerAffiliations: OWNER, isFork:false) {
          totalCount
          pageInfo { hasNextPage endCursor }
          nodes {
            stargazerCount
            languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
              edges { size node { name } }
            }
          }
        }
      }
    }
    """
    return gql(token, query, {"login": user, "after": after})


def aggregate_stars_and_languages(token: str, user: str) -> Tuple[int, Dict[str, int], int]:
    stars_total = 0
    lang_bytes: Dict[str, int] = {}
    after = None
    repos_total_count = 0

    while True:
        data = fetch_repo_stars_and_langs_page(token, user, after)
        repos = data["user"]["repositories"]
        repos_total_count = repos.get("totalCount", repos_total_count)
        for node in repos.get("nodes", []) or []:
            stars_total += int(node.get("stargazerCount") or 0)
            langs = node.get("languages", {}).get("edges", []) or []
            for e in langs:
                size = int(e.get("size") or 0)
                name = (e.get("node") or {}).get("name") or "Other"
                lang_bytes[name] = lang_bytes.get(name, 0) + size

        pi = repos.get("pageInfo", {}) or {}
        if not pi.get("hasNextPage"):
            break
        after = pi.get("endCursor")
        if not after:
            break

    return stars_total, lang_bytes, repos_total_count


def build_svg(values: dict, languages: List[Tuple[str, int]], daily_counts: List[int]) -> str:
    # Inline SVG generator kept in python for portability
    W, H = 1200, 600
    today = values.get("updated", _dt.date.today().isoformat())

    # --- Cadence series ---
    if not daily_counts:
        daily_counts = [0] * 28
    n = len(daily_counts)
    mn0, mx0 = min(daily_counts), max(daily_counts)
    mn, mx = mn0, mx0
    flat = (mx == mn)
    if flat:
        mx = mn + 1

    cw, ch = 340, 210
    pad = 18
    x0, y0 = 18, 56
    w, h = cw - 2 * pad, ch - 2 * pad

    pts = []
    for i, v in enumerate(daily_counts):
        x = x0 + (w * i / (n - 1 if n > 1 else 1))
        y = y0 + h - (h * (v - mn) / (mx - mn))
        if flat:
            y = y0 + h - 1.0
        pts.append((x, y))

    path = "M " + " L ".join([f"{x:.1f},{y:.1f}" for x, y in pts])
    area = path + f" L {x0+w:.1f},{y0+h:.1f} L {x0:.1f},{y0+h:.1f} Z"

    # --- Languages: stacked bar + compact legend (top 4) ---
    if not languages:
        languages = [("C++", 73), ("CMake", 15), ("Python", 10), ("Other", 2)]
    langs = sorted(languages, key=lambda kv: kv[1], reverse=True)[:4]
    total = sum(v for _, v in langs) or 1
    langs_pct = [(name, v * 100 / total) for name, v in langs]

    bar_w = 640
    hbar = 14
    seg_opacities = [0.85, 0.65, 0.45, 0.28]

    widths: List[int] = []
    running = 0
    for i, (_, pct) in enumerate(langs_pct):
        if i < len(langs_pct) - 1:
            wi = int(round(bar_w * pct / 100.0))
            widths.append(wi)
            running += wi
        else:
            widths.append(bar_w - running)

    segs = []
    x = 16
    y = 22
    for i, ((name, pct), wi) in enumerate(zip(langs_pct, widths)):
        op = seg_opacities[i % len(seg_opacities)]
        segs.append(f'<rect x="{x}" y="{y}" width="{wi}" height="{hbar}" fill="#0f172a" fill-opacity="{op:.2f}"/>')
        x += wi
    segs_svg = "\n        ".join(segs)

    cols = [16, 340]
    rows = [52, 78]
    legend_items = []
    for i, (name, pct) in enumerate(langs_pct):
        cx = cols[i % 2]
        cy = rows[i // 2]
        op = seg_opacities[i % len(seg_opacities)]
        legend_items.append(
            f'<g transform="translate({cx},{cy})">'
            f'<rect x="0" y="-8" width="12" height="12" rx="3" fill="#0f172a" fill-opacity="{op:.2f}"/>'
            f'<text class="t" x="18" y="-2" dominant-baseline="middle">{name}</text>'
            f'<text class="t muted" x="200" y="-2" dominant-baseline="middle">{pct:.0f}%</text>'
            f'</g>'
        )
    legend_svg = "\n        ".join(legend_items)

    def v(k: str) -> str:
        return str(values.get(k, "—"))

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Engineering Metrics (self-hosted SVG)">
  <defs>
    <linearGradient id="bg" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#f8fafc"/>
    </linearGradient>
    <linearGradient id="accent" x1="0" x2="1" y1="0" y2="0">
      <stop offset="0%" stop-color="#0f172a"/>
      <stop offset="50%" stop-color="#334155"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
    <linearGradient id="area" x1="0" x2="1" y1="0" y2="0">
      <stop offset="0%" stop-color="#0f172a" stop-opacity="0.10"/>
      <stop offset="70%" stop-color="#0f172a" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#0f172a" stop-opacity="0.85"/>
    </linearGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="2" stdDeviation="8" flood-color="#0f172a" flood-opacity="0.10"/>
    </filter>
    <clipPath id="langClip">
      <rect x="16" y="22" width="{bar_w}" height="{hbar}" rx="7" ry="7"/>
    </clipPath>
    <style>
      .title{{font:800 30px -apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif; fill:#0f172a}}
      .sub{{font:600 13px -apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif; fill:#334155}}
      .tiny{{font:600 11px -apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif; fill:#64748b}}
      .h{{font:800 14px -apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif; fill:#0f172a}}
      .t{{font:600 12px -apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif; fill:#334155}}
      .mono{{font:700 11px ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,"Liberation Mono","Courier New",monospace; fill:#334155}}
      .muted{{fill:#64748b}}
      .card{{fill:#ffffff; stroke:#e2e8f0; stroke-width:1}}
      .chip{{fill:#f1f5f9; stroke:#e2e8f0; stroke-width:1}}
      .kpi{{font:900 22px -apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif; fill:#0f172a}}
      .kpiLabel{{font:700 11px -apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif; fill:#64748b}}
      .barbg{{fill:#e2e8f0}}
    </style>
  </defs>

  <rect x="0" y="0" width="{W}" height="{H}" fill="url(#bg)"/>

  <g transform="translate(44,34)">
    <text class="title" x="0" y="0" dominant-baseline="hanging">Hananiah Hsu · Engineering Metrics</text>
    <text class="sub" x="0" y="42" dominant-baseline="hanging">CAD / Simulation / Generative · C++ · Qt · OpenCascade · Persistence</text>
    <g transform="translate(0,78)">
      <rect x="0" y="0" width="640" height="6" rx="3" fill="url(#accent)"/>
      <text class="tiny" x="660" y="3" dominant-baseline="middle">Updated: {today} · Self-hosted SVG</text>
    </g>
  </g>

  <g filter="url(#shadow)">
    <rect class="card" x="44" y="140" width="712" height="416" rx="18"/>
    <rect class="card" x="776" y="140" width="380" height="416" rx="18"/>
  </g>

  <g transform="translate(68,168)">
    <text class="h" x="0" y="0" dominant-baseline="hanging">Key indicators (last 30 days)</text>
    <text class="t" x="0" y="24" dominant-baseline="hanging">Generated by GitHub Actions (no third-party endpoints).</text>

    <g transform="translate(0,58)">
      <rect class="chip" x="0" y="0" width="160" height="78" rx="14"/>
      <text class="kpi" x="16" y="18" dominant-baseline="hanging">{v("contrib30")}</text>
      <text class="kpiLabel" x="16" y="54" dominant-baseline="hanging">Contributions</text>

      <rect class="chip" x="176" y="0" width="160" height="78" rx="14"/>
      <text class="kpi" x="192" y="18" dominant-baseline="hanging">{v("commits30")}</text>
      <text class="kpiLabel" x="192" y="54" dominant-baseline="hanging">Commits</text>

      <rect class="chip" x="352" y="0" width="160" height="78" rx="14"/>
      <text class="kpi" x="368" y="18" dominant-baseline="hanging">{v("prs30")}</text>
      <text class="kpiLabel" x="368" y="54" dominant-baseline="hanging">PRs</text>

      <rect class="chip" x="528" y="0" width="160" height="78" rx="14"/>
      <text class="kpi" x="544" y="18" dominant-baseline="hanging">{v("stars")}</text>
      <text class="kpiLabel" x="544" y="54" dominant-baseline="hanging">Total stars</text>
    </g>

    <g transform="translate(0,156)">
      <text class="h" x="0" y="0" dominant-baseline="hanging">Account scale</text>
      <g transform="translate(0,28)">
        <rect class="chip" x="0" y="0" width="224" height="56" rx="14"/>
        <text class="mono" x="16" y="18" dominant-baseline="hanging">Repos</text>
        <text class="kpi" x="16" y="26" dominant-baseline="hanging">{v("repos")}</text>

        <rect class="chip" x="244" y="0" width="224" height="56" rx="14"/>
        <text class="mono" x="260" y="18" dominant-baseline="hanging">Followers</text>
        <text class="kpi" x="260" y="26" dominant-baseline="hanging">{v("followers")}</text>

        <rect class="chip" x="488" y="0" width="200" height="56" rx="14"/>
        <text class="mono" x="504" y="18" dominant-baseline="hanging">Following</text>
        <text class="kpi" x="504" y="26" dominant-baseline="hanging">{v("following")}</text>
      </g>
    </g>

    <g transform="translate(0,276)">
      <text class="h" x="0" y="0" dominant-baseline="hanging">Language distribution</text>
      <text class="tiny" x="0" y="22" dominant-baseline="hanging">Size-weighted across owned, non-fork repositories.</text>

      <g transform="translate(0,36)">
        <rect class="chip" x="0" y="0" width="688" height="104" rx="16"/>
        <rect class="barbg" x="16" y="22" width="{bar_w}" height="{hbar}" rx="7"/>
        <g clip-path="url(#langClip)">
        {segs_svg}
        </g>
        {legend_svg}
      </g>
    </g>
  </g>

  <g transform="translate(800,168)">
    <text class="h" x="0" y="0" dominant-baseline="hanging">Cadence</text>
    <text class="t" x="0" y="24" dominant-baseline="hanging">Daily contributions (last {n} days)</text>

    <g transform="translate(0,54)">
      <rect x="0" y="0" width="{cw}" height="{ch}" rx="16" fill="#f1f5f9" stroke="#cbd5e1"/>
      <g opacity="0.65">
        <line x1="18" y1="64" x2="{cw-18}" y2="64" stroke="#e2e8f0" stroke-width="1"/>
        <line x1="18" y1="108" x2="{cw-18}" y2="108" stroke="#e2e8f0" stroke-width="1"/>
        <line x1="18" y1="152" x2="{cw-18}" y2="152" stroke="#e2e8f0" stroke-width="1"/>
      </g>
      <path d="{area}" fill="url(#area)"/>
      <path d="{path}" fill="none" stroke="#0f172a" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
      <circle cx="{pts[-1][0]:.1f}" cy="{pts[-1][1]:.1f}" r="4.5" fill="#0f172a"/>
      <text class="tiny" x="18" y="20" dominant-baseline="hanging">min: {mn0} · max: {mx0}</text>
    </g>

    <g transform="translate(0,288)">
      <text class="h" x="0" y="0" dominant-baseline="hanging">Update mode</text>
      <text class="t" x="0" y="24" dominant-baseline="hanging">Scheduled refresh via Actions. No third-party render services.</text>
    </g>
  </g>
</svg>
"""
    return svg
def build_metrics(token: str, user: str, days: int = 30, spark_days: int = 28) -> Metrics:
    today = _dt.date.today()
    date_to = _dt.datetime(today.year, today.month, today.day, 0, 0, 0, tzinfo=_dt.timezone.utc)
    date_from = date_to - _dt.timedelta(days=days)

    core = fetch_user_core(token, user, date_from.isoformat(), date_to.isoformat())
    u = core["user"]
    cc = u["contributionsCollection"]
    cal = cc["contributionCalendar"]

    contrib30 = int(cal.get("totalContributions") or 0)
    commits30 = int(cc.get("totalCommitContributions") or 0)
    prs30 = int(cc.get("totalPullRequestContributions") or 0)

    followers = int(u["followers"]["totalCount"])
    following = int(u["following"]["totalCount"])
    repos_total = int(u["repositories"]["totalCount"])

    stars_total, lang_bytes, repos_total_from_paging = aggregate_stars_and_languages(token, user)
    # trust paging repos_total if it is non-zero
    repos_total = repos_total_from_paging or repos_total

    # daily contributions from calendar weeks/days
    days_list = []
    for w in cal.get("weeks", []) or []:
        for d in w.get("contributionDays", []) or []:
            days_list.append((d["date"], int(d.get("contributionCount") or 0)))
    # take last spark_days
    days_list.sort(key=lambda x: x[0])
    daily = [c for _, c in days_list[-spark_days:]]

    langs_sorted = sorted(lang_bytes.items(), key=lambda kv: kv[1], reverse=True)

    return Metrics(
        updated=today.isoformat(),
        contrib30=contrib30,
        commits30=commits30,
        prs30=prs30,
        stars=stars_total,
        repos=repos_total,
        followers=followers,
        following=following,
        daily=daily,
        languages=langs_sorted,
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--user", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--spark-days", type=int, default=28)
    args = ap.parse_args()

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("METRICS_TOKEN")
    if not token:
        print("ERROR: missing GITHUB_TOKEN (or METRICS_TOKEN) in environment.", file=sys.stderr)
        return 2

    m = build_metrics(token, args.user, days=args.days, spark_days=args.spark_days)

    values = {
        "updated": m.updated,
        "contrib30": m.contrib30,
        "commits30": m.commits30,
        "prs30": m.prs30,
        "stars": m.stars,
        "repos": m.repos,
        "followers": m.followers,
        "following": m.following,
    }

    svg = build_svg(values, m.languages, m.daily)

    out_path = args.out
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)

    print(f"OK: wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
