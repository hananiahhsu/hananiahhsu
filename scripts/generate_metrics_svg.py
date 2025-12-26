#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate a self-hosted metrics SVG for GitHub README (minimal + creative).

- No language section
- No repo list
- No contribution map clone
- Uses GitHub GraphQL only
"""

from __future__ import annotations

import argparse
import datetime as _dt
import os
import sys
from dataclasses import dataclass
from typing import List, Optional

import requests

GQL_ENDPOINT = "https://api.github.com/graphql"


@dataclass
class Metrics:
    updated: str
    contrib30: int
    commits30: int
    prs30: int
    stars: int
    daily: List[int]


def gql(token: str, query: str, variables: dict) -> dict:
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}
    r = requests.post(GQL_ENDPOINT, json={"query": query, "variables": variables}, headers=headers, timeout=30)
    r.raise_for_status()
    data = r.json()
    if "errors" in data:
        raise RuntimeError(f"GraphQL errors: {data['errors']}")
    return data["data"]


def fetch_user_contrib(token: str, user: str, date_from: str, date_to: str):
    query = r"""
    query($login:String!, $from:DateTime!, $to:DateTime!) {
      user(login:$login) {
        contributionsCollection(from:$from, to:$to) {
          totalCommitContributions
          totalPullRequestContributions
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
    return int(cal["totalContributions"]), int(cc["totalCommitContributions"]), int(cc["totalPullRequestContributions"]), days


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


def _fmt_num(x: int) -> str:
    if x is None:
        return "—"
    if x < 1000:
        return str(x)
    if x < 1_000_000:
        v = x / 1000.0
        s = f"{v:.1f}k"
        return s.replace(".0k", "k")
    v = x / 1_000_000.0
    s = f"{v:.1f}M"
    return s.replace(".0M", "M")


def build_svg(m: Metrics) -> str:
    W, H = 1200, 460
    updated = m.updated

    daily_counts = m.daily or [0] * 28
    n = len(daily_counts)
    mn0, mx0 = min(daily_counts), max(daily_counts)
    mn, mx = mn0, mx0
    flat = (mx == mn)
    if flat:
        mx = mn + 1

    sx, sy = 80, 270
    sw, sh = 1040, 120
    pad = 18
    x0, y0 = sx + pad, sy + 34
    w, h = sw - 2 * pad, sh - 52

    pts = []
    for i, v in enumerate(daily_counts):
        x = x0 + (w * (i / (n - 1 if n > 1 else 1)))
        y = y0 + h - (h * ((v - mn) / (mx - mn)))
        if flat:
            y = y0 + h - 1.0
        pts.append((x, y))

    path = "M " + " L ".join([f"{x:.1f},{y:.1f}" for x, y in pts])
    area = path + f" L {pts[-1][0]:.1f},{y0+h:.1f} L {pts[0][0]:.1f},{y0+h:.1f} Z"

    # decorative wireframe
    wire = []
    cx, cy = 1000, 170
    rx, ry = 150, 90
    for a in [0, 20, 40, 60, 80, 100, 120, 140, 160]:
        wire.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" transform="rotate({a} {cx} {cy})" />')
    for k in [0.25, 0.5, 0.75]:
        wire.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx*(1-k*0.35):.1f}" ry="{ry*(1-k*0.6):.1f}" />')
    wire_svg = "\n        ".join(wire)

    c30 = _fmt_num(m.contrib30)
    cm30 = _fmt_num(m.commits30)
    pr30 = _fmt_num(m.prs30)
    st = _fmt_num(m.stars)

    return f"""<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"{W}\" height=\"{H}\" viewBox=\"0 0 {W} {H}\" role=\"img\" aria-label=\"Engineering Signal (self-hosted SVG)\">
  <defs>
    <linearGradient id=\"bg\" x1=\"0\" x2=\"1\" y1=\"0\" y2=\"1\">
      <stop offset=\"0%\" stop-color=\"#ffffff\"/>
      <stop offset=\"100%\" stop-color=\"#f8fafc\"/>
    </linearGradient>
    <linearGradient id=\"ink\" x1=\"0\" x2=\"1\" y1=\"0\" y2=\"0\">
      <stop offset=\"0%\" stop-color=\"#0f172a\" stop-opacity=\"0.92\"/>
      <stop offset=\"50%\" stop-color=\"#334155\" stop-opacity=\"0.92\"/>
      <stop offset=\"100%\" stop-color=\"#0f172a\" stop-opacity=\"0.92\"/>
    </linearGradient>
    <linearGradient id=\"area\" x1=\"0\" x2=\"1\" y1=\"0\" y2=\"0\">
      <stop offset=\"0%\" stop-color=\"#0f172a\" stop-opacity=\"0.06\"/>
      <stop offset=\"70%\" stop-color=\"#0f172a\" stop-opacity=\"0.20\"/>
      <stop offset=\"100%\" stop-color=\"#0f172a\" stop-opacity=\"0.34\"/>
    </linearGradient>
    <filter id=\"shadow\" x=\"-20%\" y=\"-20%\" width=\"140%\" height=\"140%\">
      <feDropShadow dx=\"0\" dy=\"2\" stdDeviation=\"10\" flood-color=\"#0f172a\" flood-opacity=\"0.10\"/>
    </filter>
    <style>
      .title{{font:900 28px -apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif; fill:#0f172a}}
      .sub{{font:650 12px -apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif; fill:#475569}}
      .meta{{font:650 11px ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,\"Liberation Mono\",\"Courier New\",monospace; fill:#64748b}}
      .k{{font:900 34px -apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif; fill:#0f172a}}
      .kl{{font:750 11px -apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif; fill:#64748b; letter-spacing:0.2px}}
      .card{{fill:#ffffff; stroke:#e2e8f0; stroke-width:1}}
      .soft{{fill:#f1f5f9; stroke:#e2e8f0; stroke-width:1}}
      .grid{{stroke:#e2e8f0; stroke-width:1}}
    </style>
  </defs>

  <rect x=\"0\" y=\"0\" width=\"{W}\" height=\"{H}\" fill=\"url(#bg)\"/>

  <g filter=\"url(#shadow)\">
    <rect class=\"card\" x=\"40\" y=\"40\" width=\"1120\" height=\"380\" rx=\"24\"/>
  </g>

  <g opacity=\"0.12\" stroke=\"#0f172a\" stroke-width=\"1.4\" fill=\"none\">
        {wire_svg}
  </g>

  <g transform=\"translate(70,78)\">
    <text class=\"title\" x=\"0\" y=\"0\" dominant-baseline=\"hanging\">Engineering signal</text>
    <text class=\"sub\" x=\"0\" y=\"38\" dominant-baseline=\"hanging\">CAD · Simulation · Generative · C++ / Qt / OpenCascade · Persistence</text>
    <rect x=\"0\" y=\"68\" width=\"520\" height=\"6\" rx=\"3\" fill=\"url(#ink)\"/>
    <text class=\"meta\" x=\"1040\" y=\"71\" text-anchor=\"end\" dominant-baseline=\"middle\">updated {updated}</text>
  </g>

  <g transform=\"translate(70,160)\">
    <g>
      <text class=\"k\" x=\"0\" y=\"0\" dominant-baseline=\"hanging\">{c30}</text>
      <text class=\"kl\" x=\"0\" y=\"46\" dominant-baseline=\"hanging\">CONTRIBUTIONS (30D)</text>
    </g>
    <g transform=\"translate(270,0)\">
      <text class=\"k\" x=\"0\" y=\"0\" dominant-baseline=\"hanging\">{cm30}</text>
      <text class=\"kl\" x=\"0\" y=\"46\" dominant-baseline=\"hanging\">COMMITS (30D)</text>
    </g>
    <g transform=\"translate(540,0)\">
      <text class=\"k\" x=\"0\" y=\"0\" dominant-baseline=\"hanging\">{pr30}</text>
      <text class=\"kl\" x=\"0\" y=\"46\" dominant-baseline=\"hanging\">PULL REQUESTS (30D)</text>
    </g>
    <g transform=\"translate(850,0)\">
      <text class=\"k\" x=\"0\" y=\"0\" dominant-baseline=\"hanging\">{st}</text>
      <text class=\"kl\" x=\"0\" y=\"46\" dominant-baseline=\"hanging\">TOTAL STARS</text>
    </g>
  </g>

  <g>
    <rect class=\"soft\" x=\"{sx}\" y=\"{sy}\" width=\"{sw}\" height=\"{sh}\" rx=\"18\"/>
    <text class=\"kl\" x=\"{sx+18}\" y=\"{sy+18}\" dominant-baseline=\"hanging\">CADENCE (LAST {n} DAYS)</text>
    <text class=\"meta\" x=\"{sx+sw-18}\" y=\"{sy+18}\" text-anchor=\"end\" dominant-baseline=\"hanging\">min {mn0} · max {mx0}</text>

    <g opacity=\"0.85\">
      <line class=\"grid\" x1=\"{sx+18}\" y1=\"{sy+52}\" x2=\"{sx+sw-18}\" y2=\"{sy+52}\"/>
      <line class=\"grid\" x1=\"{sx+18}\" y1=\"{sy+88}\" x2=\"{sx+sw-18}\" y2=\"{sy+88}\"/>
      <line class=\"grid\" x1=\"{sx+18}\" y1=\"{sy+124}\" x2=\"{sx+sw-18}\" y2=\"{sy+124}\"/>
    </g>

    <path d=\"{area}\" fill=\"url(#area)\"/>
    <path d=\"{path}\" fill=\"none\" stroke=\"#0f172a\" stroke-width=\"3\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/>
    <circle cx=\"{pts[-1][0]:.1f}\" cy=\"{pts[-1][1]:.1f}\" r=\"5\" fill=\"#0f172a\"/>
  </g>

</svg>
"""


def build_metrics(token: str, user: str, days: int, spark_days: int) -> Metrics:
    today = _dt.datetime.utcnow()
    date_to = today.isoformat() + "Z"
    date_from = (today - _dt.timedelta(days=days)).isoformat() + "Z"

    total_contrib, commit_contrib, pr_contrib, days_list = fetch_user_contrib(token, user, date_from, date_to)
    stars = fetch_total_stars(token, user)

    tail = days_list[-spark_days:] if spark_days > 0 else days_list
    daily = [c for _, c in tail]
    if spark_days > 0 and len(daily) < spark_days:
        daily = [0] * (spark_days - len(daily)) + daily

    return Metrics(
        updated=_dt.date.today().isoformat(),
        contrib30=int(total_contrib),
        commits30=int(commit_contrib),
        prs30=int(pr_contrib),
        stars=int(stars),
        daily=daily,
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

    m = build_metrics(token, args.user, args.days, args.spark_days)
    svg = build_svg(m)

    out_path = args.out
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)

    print(f"OK: wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
