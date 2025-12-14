#!/usr/bin/env python3
"""
Advent of Code 2024 - Día 22: Monkey Market

- Part 1:
    For each buyer, generate 2000 secrets and add up secret no. 2000.
- Part 2:
    With prices (last digit of the secret) and changes between consecutive prices,
    find the best pattern of 4 changes that maximizes the sum of first sales for everyone.
"""

import os
from typing import Dict, List, Tuple

MOD = 16777216


def next_secret(secret: int) -> int:
    """
    Calculate the next secret number from the current one.
    Transformation:
    - Mix (XOR) with `secret * 64` and reduce modulo `MOD`.
    - Mix (XOR) with `secret // 32` and reduce modulo `MOD`.
    - Mix (XOR) with `secret * 2048` and reduce modulo `MOD`.

    Args:
        secret: Current secret number.
    Returns:
        New secret number (integer in [0, MOD)).
    """
    secret = (secret ^ (secret * 64)) % MOD
    secret = (secret ^ (secret // 32)) % MOD
    secret = (secret ^ (secret * 2048)) % MOD
    return secret


def simulate_nth(initial: int, n: int) -> int:
    """
    Apply `next_secret` n times and return the resulting secret.

    Args:
        initial: Initial secret of the buyer.
        n: Number of iterations to apply.
    Returns:
        Secret after n iterations.
    """
    s = initial
    for _ in range(n):
        s = next_secret(s)
    return s


def parse_input(text: str) -> List[int]:
    """
    Parse initial secrets (one integer per non-empty line).

    Args:
        text: Content of the input file.
    Returns:
        List of integers with the initial secrets.
    """
    secrets = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        secrets.append(int(line))
    return secrets


def best_bananas_for_all(initials: List[int]) -> Tuple[int, Tuple[int, int, int, int]]:
    """
    Calculate the maximum total of bananas using a single pattern of 4 price changes.
    Procedure:
    - For each buyer, simulate 2000 secrets; the price is `secret % 10`.
    - Changes are differences between consecutive prices.
    - Record for each 4-change pattern the first sale (price) where it appears.
    - Sum those first sales between buyers and choose the pattern with the highest sum.

    Args:
        initials: List of initial secrets per buyer.
    Returns:
        A tuple with:
        - `best_total`: maximum sum reached.
        - `best_pat`: 4-change pattern that reaches `best_total`.
        - `ranking`: top-10 patterns with their sums.
    """
    global_sum: Dict[Tuple[int, int, int, int], int] = {}
    for initial in initials:
        s = initial
        prev_price = s % 10
        # per-buyer first-occurrence map
        first_sale: Dict[Tuple[int, int, int, int], int] = {}
        # simulate 2000 steps -> 2000 changes
        changes: List[int] = []
        for step in range(1, 2001):
            s = next_secret(s)
            price = s % 10
            delta = price - prev_price
            changes.append(delta)
            prev_price = price
            if len(changes) >= 4:
                pat = (changes[-4], changes[-3], changes[-2], changes[-1])
                if pat not in first_sale:
                    first_sale[pat] = price
        # accumulate to global sums
        for pat, sale_price in first_sale.items():
            global_sum[pat] = global_sum.get(pat, 0) + sale_price
    # find best
    best_total = 0
    best_pat = (0, 0, 0, 0)
    ranking = sorted(global_sum.items(), key=lambda x: x[1], reverse=True)
    for pat, tot in ranking:
        if tot > best_total:
            best_total = tot
            best_pat = pat
    return best_total, best_pat, ranking[:10]


def main():
    """
    Entry point:
    - Reads `day22.txt`.
    - Executes Part 1 (sum of 2000th secrets).
    - Executes Part 2 (best 4-change pattern and top-10).
    - Prints results.
    """
    input_path = os.path.join(os.path.dirname(__file__), "day22.txt")
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()
    initial_secrets = parse_input(content)
    total = 0
    for s in initial_secrets:
        total += simulate_nth(s, 2000)
    best_total, best_pat, top10 = best_bananas_for_all(initial_secrets)
    print("=" * 70)
    print("ADVENT OF CODE 2024 - DAY 22: Monkey Market")
    print("=" * 70)
    print(f"Part 1 - Sum of 2000th secrets: {total}")
    print(f"Part 2 - Max bananas: {best_total} using pattern {best_pat}")
    print("Top 10 patterns:")
    for pat, val in top10:
        print(f"  {pat}: {val}")
    print("=" * 70)


if __name__ == "__main__":
    main()
