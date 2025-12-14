#!/usr/bin/env python3
import os


def parse_disk_map(s: str) -> list[int | None]:
    s = s.strip()
    blocks: list[int | None] = []
    file_id = 0
    for i, ch in enumerate(s):
        length = int(ch)
        if i % 2 == 0:
            blocks.extend([file_id] * length)
            file_id += 1
        else:
            blocks.extend([None] * length)
    return blocks


def compact_blocks(blocks: list[int | None]) -> None:
    left = 0
    right = len(blocks) - 1
    while left < right:
        while left < len(blocks) and blocks[left] is not None:
            left += 1
        while right >= 0 and blocks[right] is None:
            right -= 1
        if left < right:
            blocks[left] = blocks[right]
            blocks[right] = None
            left += 1
            right -= 1


def checksum(blocks: list[int | None]) -> int:
    total = 0
    for i, v in enumerate(blocks):
        if v is not None:
            total += i * v
    return total


def verify_example() -> None:
    example = "2333133121414131402"
    b = parse_disk_map(example)
    compact_blocks(b)
    cs = checksum(b)
    print("=" * 70)
    print("VERIFYING EXAMPLE (Day 9 - Part 1)")
    print("=" * 70)
    print(f"Checksum: {cs}")
    print("Expected: 1928")
    print(f"Match: {cs == 1928}")
    print("=" * 70)


def build_free_spans(blocks: list[int | None]) -> list[tuple[int, int]]:
    spans: list[tuple[int, int]] = []
    i = 0
    n = len(blocks)
    while i < n:
        if blocks[i] is None:
            start = i
            while i < n and blocks[i] is None:
                i += 1
            spans.append((start, i - start))
        else:
            i += 1
    return spans


def find_file_segment(blocks: list[int | None], file_id: int) -> tuple[int, int] | None:
    n = len(blocks)
    i = 0
    while i < n and blocks[i] != file_id:
        i += 1
    if i == n:
        return None
    start = i
    while i < n and blocks[i] == file_id:
        i += 1
    length = i - start
    return start, length


def merge_spans(spans: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if not spans:
        return spans
    spans.sort(key=lambda x: x[0])
    merged: list[tuple[int, int]] = []
    cur_s, cur_l = spans[0]
    for s, l in spans[1:]:
        if cur_s + cur_l == s:
            cur_l += l
        else:
            merged.append((cur_s, cur_l))
            cur_s, cur_l = s, l
    merged.append((cur_s, cur_l))
    return merged


def insert_free_span(spans: list[tuple[int, int]], new_span: tuple[int, int]) -> None:
    spans.append(new_span)
    merged = merge_spans(spans)
    spans.clear()
    spans.extend(merged)


def compact_files_whole(blocks: list[int | None]) -> None:
    spans = build_free_spans(blocks)
    max_id = max(v for v in blocks if v is not None) if blocks else -1
    for fid in range(max_id, -1, -1):
        seg = find_file_segment(blocks, fid)
        if seg is None:
            continue
        start, length = seg
        target_index = None
        for idx, (s, l) in enumerate(spans):
            if s < start and l >= length:
                target_index = idx
                break
        if target_index is None:
            continue
        s, l = spans[target_index]
        for i in range(length):
            blocks[s + i] = fid
            blocks[start + i] = None
        if length == l:
            spans.pop(target_index)
        else:
            spans[target_index] = (s + length, l - length)
        insert_free_span(spans, (start, length))


def verify_example_part2() -> None:
    example = "2333133121414131402"
    b = parse_disk_map(example)
    compact_files_whole(b)
    cs = checksum(b)
    print("=" * 70)
    print("VERIFYING EXAMPLE (Day 9 - Part 2)")
    print("=" * 70)
    print(f"Checksum: {cs}")
    print("Expected: 2858")
    print(f"Match: {cs == 2858}")
    print("=" * 70)


def main() -> None:
    input_path = os.path.join(os.path.dirname(__file__), "day09.txt")
    with open(input_path, "r", encoding="utf-8") as f:
        line = f.read().strip()

    blocks_p1 = parse_disk_map(line)
    compact_blocks(blocks_p1)
    result_p1 = checksum(blocks_p1)

    blocks_p2 = parse_disk_map(line)
    compact_files_whole(blocks_p2)
    result_p2 = checksum(blocks_p2)

    print("=" * 70)
    print("ADVENT OF CODE 2024 - DAY 9: Disk Fragmenter")
    print("=" * 70)
    print(f"Blocks: {len(blocks_p1)}")
    print(f"Part 1 - Filesystem checksum: {result_p1}")
    print(f"Part 2 - Filesystem checksum: {result_p2}")
    print("=" * 70)


if __name__ == "__main__":
    verify_example()
    verify_example_part2()
    main()
