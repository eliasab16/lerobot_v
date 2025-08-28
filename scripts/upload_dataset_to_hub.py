#!/usr/bin/env python3

"""
Script to upload a cached lerobot dataset to Hugging Face Hub.
Usage: python upload_dataset_to_hub.py --dataset_path=<dataset_path> --repo_id=<repo_id>
"""

import argparse
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from lerobot.datasets.lerobot_dataset import LeRobotDataset

def upload_dataset(dataset_path: str, repo_id: str):
    """Upload a cached dataset to Hugging Face Hub"""
    
    dataset_path = Path(dataset_path)
    
    print(f"Loading dataset from: {dataset_path}")
    print(f"Repo ID: {repo_id}")
    
    # Load the dataset from the specific cache path
    dataset = LeRobotDataset(repo_id=repo_id, root=dataset_path)
    
    print(f"Dataset loaded with {len(dataset)} samples")
    print(f"Dataset metadata: {dataset.meta.info}")
    
    # Push to hub (ignore dot files like .DS_Store and images directory)
    print("Uploading to Hugging Face Hub...")
    dataset.push_to_hub(ignore_patterns=[".*", "images/"])
    
    print(f"✅ Successfully uploaded {repo_id} to Hugging Face Hub!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload a cached lerobot dataset to Hugging Face Hub")
    parser.add_argument("--dataset_path", required=True, help="Path to the dataset directory")
    parser.add_argument("--repo_id", required=True, help="Repository ID in format 'user/dataset_name'")
    
    args = parser.parse_args()
    
    upload_dataset(args.dataset_path, args.repo_id)