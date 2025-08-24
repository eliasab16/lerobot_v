#!/usr/bin/env python3

"""
Script to upload a cached lerobot dataset to Hugging Face Hub.
Usage: python upload_dataset_to_hub.py <dataset_path>
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from lerobot.datasets.lerobot_dataset import LeRobotDataset

def upload_dataset(dataset_path: str):
    """Upload a cached dataset to Hugging Face Hub"""
    
    dataset_path = Path(dataset_path)
    repo_id = "/".join(dataset_path.parts[-2:])  # Get user/dataset_name from path
    
    print(f"Loading dataset from: {dataset_path}")
    print(f"Repo ID: {repo_id}")
    
    # Load the dataset from the specific cache path
    dataset = LeRobotDataset(repo_id=repo_id, root=dataset_path)
    
    print(f"Dataset loaded with {len(dataset)} samples")
    print(f"Dataset metadata: {dataset.meta.info}")
    
    # Push to hub
    print("Uploading to Hugging Face Hub...")
    dataset.push_to_hub()
    
    print(f"✅ Successfully uploaded {repo_id} to Hugging Face Hub!")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python upload_dataset_to_hub.py <dataset_path>")
        print("Example: python upload_dataset_to_hub.py ~/.cache/huggingface/lerobot/eliasab16/insert_wire_prompt_2")
        sys.exit(1)
    
    dataset_path = sys.argv[1]
    upload_dataset(dataset_path)