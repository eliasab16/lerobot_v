#!/usr/bin/env python3
import json
import sys

# This script helps recalculate the episode stats when modifying the dataset.
# The stats should be updated in info.json

def count_episode_lengths(file_path):
    total_length = 0
    episode_count = 0
    
    with open(file_path, 'r') as f:
        for line in f:
            data = json.loads(line.strip())
            if 'length' in data:
                total_length += data['length']
                episode_count += 1
    
    print(f"Episodes in  {file_path}:\n")
    print(f"Total length: {total_length}\n")
    print(f"Total episodes: {episode_count}\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <path_to_episodes.jsonl>")
        sys.exit(1)

    file_path = sys.argv[1]
    count_episode_lengths(file_path)