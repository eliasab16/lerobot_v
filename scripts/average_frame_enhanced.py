import argparse
import os
import mediapy
import numpy as np
import tqdm
import gc

parser = argparse.ArgumentParser(description='Average frames from videos at specified time/frame')
parser.add_argument('-i', type=str, help='Input directory.', required=True)
parser.add_argument('-o', type=str, help='Output file.', required=True)
parser.add_argument('--frame', type=int, help='Frame number to extract (0-based)', default=0)
parser.add_argument('--time', type=float, help='Time in seconds to extract frame from')
args = parser.parse_args()

frames = []

def get_frame_at_time_or_index(video, frame_idx=None, time_sec=None):
    """Extract frame at specified time or index"""
    if time_sec is not None:
        # Calculate frame index from time and fps
        # Assume 30 fps if metadata not available
        fps = getattr(video, 'fps', 30)
        frame_idx = int(time_sec * fps)
    elif frame_idx is None:
        # Default to first frame if neither time nor frame specified
        frame_idx = 0
    
    # Ensure frame index is within bounds
    frame_idx = max(0, min(frame_idx, len(video) - 1))
    return video[frame_idx].copy()

for file in tqdm.tqdm(os.listdir(args.i)):
    if not file.endswith('.mp4'):
        continue
    video = mediapy.read_video(os.path.join(args.i, file))
    
    if args.time is not None:
        frame = get_frame_at_time_or_index(video, time_sec=args.time)
    else:
        frame = get_frame_at_time_or_index(video, frame_idx=args.frame)
    
    frames.append(frame)
    del video
    gc.collect()

frames = np.array(frames, np.float32)
median_image = np.median(frames.astype(np.uint8), axis=0).astype(np.float32)

avg_image = np.zeros_like(median_image)
for frame in frames:
    frame = np.clip(frame - median_image, 0, 255)
    alpha = (np.max(frame, -1, keepdims=True) / 255)**(0.5)
    avg_image = avg_image * (1 - alpha) + frame * alpha
avg_image = np.clip(median_image + avg_image, 0, 255).astype(np.uint8)

mediapy.write_image(args.o, avg_image.astype(np.uint8))

directory, filename = os.path.split(args.o)
filename, _ = os.path.splitext(filename)
mediapy.write_video(os.path.join(directory, f'video_{filename}.mp4'), frames.astype(np.uint8), fps=20)