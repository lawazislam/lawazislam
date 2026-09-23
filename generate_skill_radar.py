"""
generate_skill_radar.py

Regenerates skill-radar.svg from the data below. This script is the
source of truth for the chart, kept in the repo so the chart can always
be rebuilt or adjusted without starting from scratch.

Level scale (ordinal, low to high):
    1 = Graduate coursework
    2 = Project level
    3 = Internship level
    4 = Deployed and tested
    5 = Working professionally

Run with: python generate_skill_radar.py
"""

import numpy as np
import matplotlib.pyplot as plt

# --- Data: skill area -> level (1-5), with the evidence behind each ---
SKILLS = {
    "Data analysis": 4,      # Deployed: IoT dashboard pipeline, verified end-to-end
    "IT support": 3,         # Internship: City of Windsor, ServiceNow KB rebuild
    "Full-stack web": 4,     # Deployed: job-tracker and SlickScores, both live with tests
    "Control systems": 2,    # Project: PHEV controller, ELEC8900 grad course project
    "Digital design": 3,     # Internship: Jadavpur VLSI training, Grade A, real FPGA hardware
    "Embedded/IoT": 2,       # Project: coursework, projects, and certifications
}

LEVEL_LABELS = {
    1: "Graduate coursework",
    2: "Project level",
    3: "Internship level",
    4: "Deployed and tested",
    5: "Working professionally",
}

BG = "#0d1117"
GREEN = "#08872b"
GREEN_LIGHT = "#5fed83"
TEXT = "#a4aea6"
WHITE = "#ffffff"
GRID = "#21262d"


def build_chart(out_path="skill-radar.svg"):
    categories = list(SKILLS.keys())
    values = list(SKILLS.values())
    n = len(categories)

    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    values_closed = values + values[:1]
    angles_closed = angles + angles[:1]

    fig = plt.figure(figsize=(6.2, 7.6), facecolor=BG)
    # Leave real room below the polar axes for the level legend, this is
    # the fix for the cramped spacing: axes stop at 78% of figure height
    # instead of running almost to the bottom edge.
    ax = fig.add_axes([0.12, 0.24, 0.76, 0.68], polar=True)
    ax.set_facecolor(BG)

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    ax.set_ylim(0, 5)
    ax.set_yticks([1, 2, 3, 4, 5])
    # Radial scale numbers placed directly on the chart, in the gap between
    # the "Control systems" and "Digital design" spokes (210 degrees), the
    # part of the chart with the lowest values, so the numbers sit clear of
    # the filled shape instead of running along its edge.
    ax.set_rlabel_position(210)
    ax.set_yticklabels(["1", "2", "3", "4", "5"], color=WHITE, fontsize=8.5,
                        fontfamily="monospace", fontweight="bold")
    for label in ax.get_yticklabels():
        label.set_bbox(dict(boxstyle="round,pad=0.15", facecolor=BG,
                             edgecolor=GRID, linewidth=0.6, alpha=0.92))

    ax.set_xticks(angles)
    ax.set_xticklabels(categories, color=TEXT, fontsize=10.5, fontfamily="monospace")

    ax.grid(color=GRID, linewidth=0.8)
    ax.spines["polar"].set_color(GRID)

    ax.plot(angles_closed, values_closed, color=GREEN, linewidth=1.6)
    ax.fill(angles_closed, values_closed, color=GREEN, alpha=0.35)

    for angle, value in zip(angles, values):
        ax.plot(angle, value, "o", color=GREEN_LIGHT, markersize=4, zorder=5)

    # --- Legend: the five ordinal levels, low to high, with clear spacing ---
    # Laid out as two explicit rows rather than one auto-wrapped string,
    # so a level name never gets split awkwardly across lines.
    row1 = "1  Graduate coursework      2  Project level      3  Internship level"
    row2 = "4  Deployed and tested      5  Working professionally"

    fig.text(
        0.5, 0.145,
        "Level scale (low to high)",
        color=WHITE,
        fontsize=9.5,
        fontfamily="monospace",
        ha="center",
        va="center",
    )
    fig.text(
        0.5, 0.095,
        row1,
        color=TEXT,
        fontsize=8.3,
        fontfamily="monospace",
        ha="center",
        va="center",
    )
    fig.text(
        0.5, 0.055,
        row2,
        color=TEXT,
        fontsize=8.3,
        fontfamily="monospace",
        ha="center",
        va="center",
    )

    fig.savefig(out_path, facecolor=BG, format="svg")
    print(f"written: {out_path}")


if __name__ == "__main__":
    build_chart()
