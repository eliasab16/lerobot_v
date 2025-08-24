#!/usr/bin/env python3

"""
Script to change task descriptions in a LeRobot dataset.
Usage: python change_task_description.py <dataset_dir> <new_task> [--backup]

This script updates:
1. meta/episodes.jsonl - Updates the "tasks" field for each episode
2. meta/tasks.jsonl - Updates the "task" field for task definitions
"""

import sys
import json
import shutil
import argparse
from pathlib import Path

def update_episodes_jsonl(episodes_file: Path, new_task: str, create_backup: bool = False):
    """Update task descriptions in episodes.jsonl"""
    
    # Read all episodes
    episodes = []
    with open(episodes_file, 'r') as f:
        for line in f:
            episode = json.loads(line.strip())
            # Update the tasks field (it's a list)
            episode['tasks'] = [new_task]
            episodes.append(episode)
    
    # Create backup if requested
    if create_backup:
        backup_file = episodes_file.with_suffix('.jsonl.backup')
        shutil.copy2(episodes_file, backup_file)
        print(f"Created backup: {backup_file}")
    
    # Write updated episodes
    with open(episodes_file, 'w') as f:
        for episode in episodes:
            f.write(json.dumps(episode) + '\n')
    
    print(f"Updated {len(episodes)} episodes in {episodes_file}")

def update_tasks_jsonl(tasks_file: Path, new_task: str, create_backup: bool = False):
    """Update task descriptions in tasks.jsonl"""
    
    # Read all tasks
    tasks = []
    with open(tasks_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line:  # Skip empty lines
                task = json.loads(line)
                # Update the task field
                task['task'] = new_task
                tasks.append(task)
    
    # Create backup if requested
    if create_backup:
        backup_file = tasks_file.with_suffix('.jsonl.backup')
        shutil.copy2(tasks_file, backup_file)
        print(f"Created backup: {backup_file}")
    
    # Write updated tasks
    with open(tasks_file, 'w') as f:
        for task in tasks:
            f.write(json.dumps(task) + '\n')
    
    print(f"Updated {len(tasks)} tasks in {tasks_file}")

def change_task_description(dataset_dir: str, new_task: str, create_backup: bool = False):
    """Change task descriptions in the dataset"""
    
    dataset_path = Path(dataset_dir)
    
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset directory not found: {dataset_path}")
    
    meta_dir = dataset_path / "meta"
    if not meta_dir.exists():
        raise FileNotFoundError(f"Meta directory not found: {meta_dir}")
    
    episodes_file = meta_dir / "episodes.jsonl"
    tasks_file = meta_dir / "tasks.jsonl"
    
    # Check files exist
    if not episodes_file.exists():
        raise FileNotFoundError(f"Episodes file not found: {episodes_file}")
    
    if not tasks_file.exists():
        raise FileNotFoundError(f"Tasks file not found: {tasks_file}")
    
    print(f"Dataset directory: {dataset_path}")
    print(f"New task description: '{new_task}'")
    if create_backup:
        print("Backup files will be created")
    else:
        print("No backup files will be created")
    print()
    
    # Update both files
    update_episodes_jsonl(episodes_file, new_task, create_backup)
    update_tasks_jsonl(tasks_file, new_task, create_backup)
    
    print()
    print("✅ Task descriptions updated successfully!")
    if create_backup:
        print("Backup files created with .backup extension")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Change task descriptions in a LeRobot dataset",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python change_task_description.py ~/.cache/huggingface/lerobot/eliasab16/dataset "Pick up the red cube"
  python change_task_description.py /path/to/dataset "Insert the wire into the hole" --backup
        """
    )
    
    parser.add_argument("dataset_dir", help="Path to the dataset directory")
    parser.add_argument("new_task", help="New task description")
    parser.add_argument("--backup", action="store_true", default=False, 
                       help="Create backup files (default: False)")
    
    args = parser.parse_args()
    
    try:
        change_task_description(args.dataset_dir, args.new_task, args.backup)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)