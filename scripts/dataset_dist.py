#!/usr/bin/env python3
"""
Usage: python dataset_dist.py --dataset_path=/path/to/episodes.jsonl
"""
import argparse
import json
from collections import defaultdict


def main():
    parser = argparse.ArgumentParser(description="Analyze task distribution in a dataset")
    parser.add_argument("--dataset_path", required=True, help="Path to the episodes.jsonl file")
    args = parser.parse_args()
    
    task_counts = defaultdict(int)
    total_episodes = 0
    
    with open(args.dataset_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            episode_data = json.loads(line)
            tasks = episode_data.get('tasks', [])
            total_episodes += 1
            
            # Track which tasks appear in this episode (avoid double counting if task appears multiple times)
            unique_tasks_in_episode = set(tasks)
            for task in unique_tasks_in_episode:
                task_counts[task] += 1
    
    print(f"Task Distribution Analysis")
    print(f"Total episodes: {total_episodes}")
    print(f"Unique tasks: {len(task_counts)}")
    print("-" * 50)
    
    print("Task Name:    Count    (Percentage)")
    print("-" * 50)
    for task, count in sorted(task_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_episodes) * 100
        print(f'"{task}": {count} ({percentage:.2f}%)')


if __name__ == "__main__":
    main()