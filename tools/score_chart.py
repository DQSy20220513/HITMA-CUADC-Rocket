"""按 CUADC 2026 规则第 6 条生成得分敏感度图。

用法: python tools/score_chart.py [out.png]
"""
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def s_alt(h):
    return np.clip(100.0 - np.abs(h - 50.0) * 3.0, 0.0, None)


def s_load(l):
    return np.clip(80.0 - l * 4.0, 0.0, None)


def s_time(t):
    return np.clip((t - 10.0) * 10.0, 0.0, None)


def main(out="scoring/img/sensitivity.png"):
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.4))

    h = np.linspace(0, 100, 400)
    ax[0].plot(h, s_alt(h), lw=2)
    ax[0].axvline(50, ls="--", c="gray", lw=1)
    ax[0].set_title("altitude score:  100 - 3|H-50|")
    ax[0].set_xlabel("separation altitude H [m]")
    ax[0].set_ylabel("score")
    ax[0].annotate("50 m -> 100", (50, 100), xytext=(58, 88),
                   arrowprops=dict(arrowstyle="->", lw=0.8))
    ax[0].annotate("3 pts / m", (70, s_alt(70)), xytext=(72, 45),
                   arrowprops=dict(arrowstyle="->", lw=0.8))

    l = np.linspace(0, 24, 400)
    ax[1].plot(l, s_load(l), lw=2, color="tab:orange")
    ax[1].axvline(20, ls="--", c="r", lw=1)
    ax[1].set_title("payload score:  80 - 4L")
    ax[1].set_xlabel("landing distance L [m]")
    ax[1].set_ylabel("score")
    ax[1].annotate("20 m -> 0\n(and all glide points lost)", (20, 0), xytext=(6, 30),
                   arrowprops=dict(arrowstyle="->", lw=0.8))
    ax[1].annotate("4 pts / m", (10, s_load(10)), xytext=(11, 55),
                   arrowprops=dict(arrowstyle="->", lw=0.8))

    t = np.linspace(0, 70, 400)
    ax[2].plot(t, s_time(t), lw=2, color="tab:green")
    ax[2].axvline(10, ls="--", c="r", lw=1)
    ax[2].set_title("glide score:  10(T-10), no cap")
    ax[2].set_xlabel("flight time T [s]")
    ax[2].set_ylabel("score")
    ax[2].annotate("10 s -> 0\n(and payload score lost)", (10, 0), xytext=(14, 60),
                   arrowprops=dict(arrowstyle="->", lw=0.8))
    ax[2].annotate("10 pts / s", (40, s_time(40)), xytext=(42, 140),
                   arrowprops=dict(arrowstyle="->", lw=0.8))

    for a in ax:
        a.grid(alpha=0.3)
        a.set_ylim(-10, 320)

    fig.suptitle("CUADC 2026 · rocket launch & return · score sensitivity", fontsize=11)
    fig.tight_layout()
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    fig.savefig(out, dpi=140)
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "scoring/img/sensitivity.png")
