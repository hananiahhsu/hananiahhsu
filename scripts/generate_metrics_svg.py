#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Self-hosted GitHub metrics SVG (dark dashboard).

- Inspired by "metrics dashboard" style (cards + ring + streaks)
- No third-party SVG render endpoints
- Data source: GitHub GraphQL API
- Update: run in GitHub Actions and commit the generated SVG back to the repo

Usage:
  python scripts/generate_metrics_svg.py --user <login> --out assets/stats/metrics.svg

Env:
  GITHUB_TOKEN (recommended) or METRICS_TOKEN
"""
from __future__ import annotations

import argparse
import datetime as _dt
import math
import os
import sys
from dataclasses import dataclass
from typing import List, Optional, Tuple

import requests

GQL_ENDPOINT = "https://api.github.com/graphql"


@dataclass
class Metrics:
    updated: str
    stars: int
    commits_year: int
    prs_year: int
    issues_year: int
    contrib_year: int
    days_year: List[Tuple[str, int]]
    days_30: List[Tuple[str, int]]


def gql(token: str, query: str, variables: dict) -> dict:
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}
    r = requests.post(GQL_ENDPOINT, json={"query": query, "variables": variables}, headers=headers, timeout=30)
    r.raise_for_status()
    data = r.json()
    if "errors" in data:
        raise RuntimeError(f"GraphQL errors: {data['errors']}")
    return data["data"]


def fetch_contrib_window(token: str, user: str, date_from: str, date_to: str):
    """
    Returns: (totalContrib, commits, prs, issues, [(date,count)...])
    """
    query = r"""
    query($login:String!, $from:DateTime!, $to:DateTime!) {
      user(login:$login) {
        contributionsCollection(from:$from, to:$to) {
          totalCommitContributions
          totalPullRequestContributions
          totalIssueContributions
          contributionCalendar {
            totalContributions
            weeks { contributionDays { date contributionCount } }
          }
        }
      }
    }
    """
    d = gql(token, query, {"login": user, "from": date_from, "to": date_to})
    cc = d["user"]["contributionsCollection"]
    cal = cc["contributionCalendar"]
    days = []
    for w in cal["weeks"]:
        for day in w["contributionDays"]:
            days.append((day["date"], int(day["contributionCount"])))
    days.sort(key=lambda x: x[0])
    return (
        int(cal["totalContributions"]),
        int(cc["totalCommitContributions"]),
        int(cc["totalPullRequestContributions"]),
        int(cc["totalIssueContributions"]),
        days,
    )


def fetch_total_stars(token: str, user: str) -> int:
    total = 0
    after: Optional[str] = None
    query = r"""
    query($login:String!, $after:String) {
      user(login:$login) {
        repositories(first: 100, after: $after, ownerAffiliations: OWNER, isFork:false) {
          pageInfo { hasNextPage endCursor }
          nodes { stargazerCount }
        }
      }
    }
    """
    while True:
        d = gql(token, query, {"login": user, "after": after})
        repos = d["user"]["repositories"]
        for node in repos["nodes"]:
            total += int(node["stargazerCount"])
        pi = repos["pageInfo"]
        if not pi["hasNextPage"]:
            break
        after = pi["endCursor"]
    return total


def _fmt_num(x: Optional[int]) -> str:
    if x is None:
        return "—"
    x = int(x)
    if x < 1000:
        return str(x)
    if x < 1_000_000:
        s = f"{x/1000.0:.1f}k"
        return s.replace(".0k", "k")
    s = f"{x/1_000_000.0:.1f}M"
    return s.replace(".0M", "M")


def compute_streaks(days: List[Tuple[str,int]]):
    if not days:
        return 0, 0, None, None
    cur = 0
    i = len(days) - 1
    while i >= 0 and days[i][1] > 0:
        cur += 1
        i -= 1

    longest = 0
    best_start = None
    best_end = None
    run = 0
    run_start = None
    for d, c in days:
        if c > 0:
            if run == 0:
                run_start = d
            run += 1
            if run > longest:
                longest = run
                best_start = run_start
                best_end = d
        else:
            run = 0
            run_start = None
    return cur, longest, best_start, best_end


def grade_from_signal(active_days_year: int, total_contrib_year: int):
    score = 0.0
    score += min(1.0, active_days_year / 200.0) * 0.60
    score += min(1.0, total_contrib_year / 2000.0) * 0.40
    if score >= 0.90:
        return "A+", score
    if score >= 0.80:
        return "A", score
    if score >= 0.65:
        return "B", score
    if score >= 0.50:
        return "C", score
    return "D", score


def build_svg(m: Metrics) -> str:
    W, H = 1200, 560
    updated = m.updated

    cur_streak, long_streak, long_start, long_end = compute_streaks(m.days_year)
    active_days_year = sum(1 for _,c in m.days_year if c>0)
    grade, score = grade_from_signal(active_days_year, m.contrib_year)

    r = 54
    circ = 2*math.pi*r
    prog = max(0.0, min(1.0, score))
    dash = prog * circ
    gap = circ - dash

    counts_30 = [c for _,c in (m.days_30 or [])][-28:]
    if len(counts_30) < 28:
        counts_30 = [0]*(28-len(counts_30)) + counts_30
    mn0, mx0 = min(counts_30), max(counts_30)
    mn, mx = mn0, mx0
    flat = (mx == mn)
    if flat:
        mx = mn + 1

    sx, sy = 650, 330
    sw, sh = 510, 170
    pad = 18
    x0, y0 = sx + pad, sy + 56
    w, h = sw - 2*pad, sh - 84

    pts = []
    for i, v in enumerate(counts_30):
        x = x0 + (w * (i/(len(counts_30)-1)))
        y = y0 + h - (h*((v-mn)/(mx-mn)))
        if flat:
            y = y0 + h - 1.0
        pts.append((x,y))
    path = "M " + " L ".join([f"{x:.1f},{y:.1f}" for x,y in pts])
    area = path + f" L {pts[-1][0]:.1f},{y0+h:.1f} L {pts[0][0]:.1f},{y0+h:.1f} Z"

    stars = _fmt_num(m.stars)
    commits = _fmt_num(m.commits_year)
    prs = _fmt_num(m.prs_year)
    issues = _fmt_num(m.issues_year)
    contrib = _fmt_num(m.contrib_year)

    active_days = _fmt_num(active_days_year)
    cur_s = _fmt_num(cur_streak)
    long_s = _fmt_num(long_streak)
    long_range = f"{long_start} → {long_end}" if long_start and long_end else ""

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="GitHub Engineering Metrics (self-hosted)">
  <defs>
    <linearGradient id="bg" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0%" stop-color="#0b1220"/>
      <stop offset="100%" stop-color="#0a0f1c"/>
    </linearGradient>
    <linearGradient id="card" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0%" stop-color="#111827"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
    <linearGradient id="accent" x1="0" x2="1" y1="0" y2="0">
      <stop offset="0%" stop-color="#3b82f6"/>
      <stop offset="55%" stop-color="#ff4d8d"/>
      <stop offset="100%" stop-color="#22c55e"/>
    </linearGradient>
    <linearGradient id="sparkFill" x1="0" x2="1" y1="0" y2="0">
      <stop offset="0%" stop-color="#3b82f6" stop-opacity="0.10"/>
      <stop offset="60%" stop-color="#ff4d8d" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#22c55e" stop-opacity="0.18"/>
    </linearGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="10" stdDeviation="18" flood-color="#000000" flood-opacity="0.35"/>
    </filter>
    <style>
      .h1{{font:900 28px -apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif; fill:#e5e7eb}}
      .sub{{font:650 12px -apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif; fill:#9ca3af}}
      .mono{{font:650 11px ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,"Liberation Mono","Courier New",monospace; fill:#9ca3af}}
      .label{{font:650 12px -apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif; fill:#cbd5e1}}
      .value{{font:900 18px -apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif; fill:#e5e7eb}}
      .big{{font:900 34px -apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif; fill:#e5e7eb}}
      .small{{font:650 11px -apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif; fill:#9ca3af}}
      .card{{fill:url(#card); stroke:#1f2937; stroke-width:1}}
      .sep{{stroke:#1f2937; stroke-width:1}}
      .grid{{stroke:#1f2937; stroke-width:1}}
    </style>
  </defs>

  <rect x="0" y="0" width="{W}" height="{H}" fill="url(#bg)"/>

  <g transform="translate(52,44)">
    <text class="h1" x="0" y="0" dominant-baseline="hanging">Hananiah Hsu · Stats</text>
    <text class="sub" x="0" y="38" dominant-baseline="hanging">Self-hosted metrics · generated by GitHub Actions · no third-party render</text>
    <rect x="0" y="68" width="520" height="6" rx="3" fill="url(#accent)"/>
    <text class="mono" x="1096" y="71" text-anchor="end" dominant-baseline="middle">updated {updated}</text>
  </g>

  <g filter="url(#shadow)">
    <rect class="card" x="52" y="140" width="580" height="360" rx="18"/>
  </g>

  <g filter="url(#shadow)">
    <rect class="card" x="650" y="140" width="510" height="170" rx="18"/>
  </g>

  <g filter="url(#shadow)">
    <rect class="card" x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="18"/>
  </g>

  <g transform="translate(84,176)">
    <text class="label" x="0" y="0" dominant-baseline="hanging">Overview (last year)</text>

    <g transform="translate(0,44)">
      <circle cx="10" cy="12" r="5" fill="#ff4d8d"/>
      <text class="label" x="26" y="0" dominant-baseline="hanging">Total Stars Earned</text>
      <text class="value" x="456" y="-2" text-anchor="end" dominant-baseline="hanging">{stars}</text>
    </g>

    <g transform="translate(0,82)">
      <circle cx="10" cy="12" r="5" fill="#3b82f6"/>
      <text class="label" x="26" y="0" dominant-baseline="hanging">Total Commits</text>
      <text class="value" x="456" y="-2" text-anchor="end" dominant-baseline="hanging">{commits}</text>
    </g>

    <g transform="translate(0,120)">
      <circle cx="10" cy="12" r="5" fill="#22c55e"/>
      <text class="label" x="26" y="0" dominant-baseline="hanging">Total PRs</text>
      <text class="value" x="456" y="-2" text-anchor="end" dominant-baseline="hanging">{prs}</text>
    </g>

    <g transform="translate(0,158)">
      <circle cx="10" cy="12" r="5" fill="#f59e0b"/>
      <text class="label" x="26" y="0" dominant-baseline="hanging">Total Issues</text>
      <text class="value" x="456" y="-2" text-anchor="end" dominant-baseline="hanging">{issues}</text>
    </g>

    <g transform="translate(0,196)">
      <circle cx="10" cy="12" r="5" fill="#a78bfa"/>
      <text class="label" x="26" y="0" dominant-baseline="hanging">Total Contributions</text>
      <text class="value" x="456" y="-2" text-anchor="end" dominant-baseline="hanging">{contrib}</text>
    </g>

    <line class="sep" x1="0" y1="250" x2="520" y2="250"/>
    <text class="small" x="0" y="270" dominant-baseline="hanging">Signal grade is derived from active days + total contributions in the last year.</text>
  </g>

  <g transform="translate(520,250)">
    <circle cx="0" cy="0" r="54" fill="none" stroke="#1f2937" stroke-width="10"/>
    <circle cx="0" cy="0" r="54" fill="none" stroke="#ff4d8d" stroke-width="10"
            stroke-linecap="round" transform="rotate(-90)"
            stroke-dasharray="{dash:.2f} {gap:.2f}"/>
    <text class="big" x="0" y="-10" text-anchor="middle" dominant-baseline="middle">{grade}</text>
    <text class="small" x="0" y="26" text-anchor="middle" dominant-baseline="middle">signal</text>
  </g>

  <g transform="translate(682,176)">
    <text class="label" x="0" y="0" dominant-baseline="hanging">Consistency</text>

    <g transform="translate(0,52)">
      <text class="big" x="0" y="0" dominant-baseline="hanging">{active_days}</text>
      <text class="small" x="0" y="44" dominant-baseline="hanging">Active days (1y)</text>
    </g>

    <g transform="translate(180,52)">
      <text class="big" x="0" y="0" dominant-baseline="hanging">{cur_s}</text>
      <text class="small" x="0" y="44" dominant-baseline="hanging">Current streak (days)</text>
    </g>

    <g transform="translate(360,52)">
      <text class="big" x="0" y="0" dominant-baseline="hanging">{long_s}</text>
      <text class="small" x="0" y="44" dominant-baseline="hanging">Longest streak (1y)</text>
      <text class="mono" x="0" y="70" dominant-baseline="hanging">{long_range}</text>
    </g>
  </g>

  <g transform="translate({sx+24},{sy+22})">
    <text class="label" x="0" y="0" dominant-baseline="hanging">Cadence</text>
    <text class="small" x="0" y="22" dominant-baseline="hanging">Daily contributions (last 28 days)</text>
    <text class="mono" x="{sw-48}" y="0" text-anchor="end" dominant-baseline="hanging">min {mn0} · max {mx0}</text>

    <g opacity="0.75">
      <line class="grid" x1="0" y1="76" x2="{sw-48}" y2="76"/>
      <line class="grid" x1="0" y1="106" x2="{sw-48}" y2="106"/>
    </g>

    <path d="{area}" fill="url(#sparkFill)"/>
    <path d="{path}" fill="none" stroke="#e5e7eb" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" opacity="0.95"/>
    <circle cx="{pts[-1][0]:.1f}" cy="{pts[-1][1]:.1f}" r="4.5" fill="#ff4d8d"/>
  </g>
</svg>
"""


def build_metrics(token: str, user: str) -> Metrics:
    now = _dt.datetime.utcnow()
    to = now.isoformat() + "Z"
    from_year = (now - _dt.timedelta(days=365)).isoformat() + "Z"
    from_30 = (now - _dt.timedelta(days=30)).isoformat() + "Z"

    contrib_y, commits_y, prs_y, issues_y, days_y = fetch_contrib_window(token, user, from_year, to)
    contrib_30, _, _, _, days_30 = fetch_contrib_window(token, user, from_30, to)
    stars = fetch_total_stars(token, user)

    return Metrics(
        updated=_dt.date.today().isoformat(),
        stars=stars,
        commits_year=commits_y,
        prs_year=prs_y,
        issues_year=issues_y,
        contrib_year=contrib_y,
        days_year=days_y,
        days_30=days_30,
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--user", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("METRICS_TOKEN")
    if not token:
        print("ERROR: missing GITHUB_TOKEN (or METRICS_TOKEN) in environment.", file=sys.stderr)
        return 2

    m = build_metrics(token, args.user)
    svg = build_svg(m)

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(svg)

    print(f"OK: wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
