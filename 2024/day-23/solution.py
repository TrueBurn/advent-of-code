from collections import defaultdict
from typing import Set, Tuple
from time import perf_counter
from tqdm import tqdm

def parse_input(input_text: str) -> Set[Tuple[str, str]]:
    connections = set()
    for line in input_text.strip().splitlines():
        a, b = line.split('-')
        connections.add(tuple(sorted([a, b])))
    return connections

def find_connected_sets(connections: Set[Tuple[str, str]]) -> Set[frozenset]:
    graph = defaultdict(set)
    for a, b in connections:
        graph[a].add(b)
        graph[b].add(a)
    
    connected_sets = set()
    for computer in graph:
        for neighbor in graph[computer]:
            for third in graph[neighbor]:
                if third in graph[computer] and len({computer, neighbor, third}) == 3:
                    connected_sets.add(frozenset({computer, neighbor, third}))
    
    return connected_sets

def find_lan_party(connections: Set[Tuple[str, str]], show_progress: bool = False) -> str:
    graph = defaultdict(set)
    for a, b in connections:
        graph[a].add(b)
        graph[b].add(a)
    
    computers = list(graph.keys())
    total_checks = sum(len(computers) for size in range(len(computers), 2, -1))
    
    with tqdm(total=total_checks, disable=not show_progress, desc="Finding LAN party") as pbar:
        for size in range(len(computers), 2, -1):
            for i in range(len(computers)):
                potential_set = {computers[i]}
                candidates = set(graph[computers[i]])
                
                for computer in computers:
                    if computer == computers[i]:
                        continue
                    if computer in candidates:
                        is_connected = all(other in graph[computer] for other in potential_set)
                        if is_connected:
                            potential_set.add(computer)
                            if len(potential_set) == size:
                                return ",".join(sorted(potential_set))
                pbar.update(1)
    
    return ""

def solve(input_text: str, track_performance: bool = False) -> Tuple[int, str]:
    if track_performance:
        start = perf_counter()
    
    connections = parse_input(input_text)
    
    if track_performance:
        mid = perf_counter()
    
    connected_sets = find_connected_sets(connections)
    part1 = sum(1 for s in connected_sets if any(c.startswith('t') for c in s))
    
    if track_performance:
        mid2 = perf_counter()
    
    part2 = find_lan_party(connections, show_progress=track_performance)
    
    if track_performance:
        end = perf_counter()
        print(f"\nPerformance:")
        print(f"├─ Parsing: {(mid-start):.3f} seconds")
        print(f"├─ Part 1: {(mid2-mid):.3f} seconds")
        print(f"├─ Part 2: {(end-mid2):.3f} seconds")
        print(f"└─ Total:  {(end-start):.3f} seconds")
    
    return part1, part2

def main():
    from unit_tests import run_tests
    
    if run_tests():
        print("\nAll tests passed! Running actual solution...\n")
        with open('input.txt', 'r') as file:
            input_text = file.read()
        part1, part2 = solve(input_text, track_performance=True)
        print(f"Part 1: {part1}")
        print(f"Part 2: {part2}")
    else:
        print("\nTests failed! Please fix the issues before running the actual solution.")

if __name__ == "__main__":
    main()
