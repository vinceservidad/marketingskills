#!/usr/bin/env python3
"""Visitors per arm for a two-proportion A/B test (two-sided alpha 0.05, power 0.8 by default).

  python3 sample_size.py <baseline_rate> <relative_mde> [daily_visitors] [alpha] [power]
  python3 sample_size.py 0.026 0.20 330
"""
import math
import sys
from statistics import NormalDist

p1 = float(sys.argv[1]); rel = float(sys.argv[2])
daily = float(sys.argv[3]) if len(sys.argv) > 3 else None
alpha = float(sys.argv[4]) if len(sys.argv) > 4 else 0.05
power = float(sys.argv[5]) if len(sys.argv) > 5 else 0.8
p2 = p1 * (1 + rel)
z_a = NormalDist().inv_cdf(1 - alpha / 2); z_b = NormalDist().inv_cdf(power)
pbar = (p1 + p2) / 2
n = ((z_a * math.sqrt(2 * pbar * (1 - pbar)) + z_b * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2) / (p2 - p1) ** 2
n = math.ceil(n)
print(f"baseline {p1:.4%}, target {p2:.4%} (relative {rel:+.0%}), alpha {alpha}, power {power}")
print(f"visitors per arm: {n:,}; total: {2*n:,}")
if daily:
    days = 2 * n / daily
    print(f"at {daily:,.0f} eligible visitors a day: {days:,.0f} days, {math.ceil(days/7)} whole weeks")
