import argparse
import os
import mediapy
import numpy as np
import tqdm
import gc

parser = argparse.ArgumentParser()
parser.add_argument('-i', type=str, help='Input directory.', required=True)
parser.add_argument('-o', type=str, help='Output file.', required=True)
args = parser.parse_args()

frames = []

for file in tqdm.tqdm(os.listdir(args.i)):
    if not file.endswith('.mp4'):
        continue
    video = mediapy.read_video(os.path.join(args.i, file))
    frames.append(video[0].copy())
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

#avg_image = np.clip(median_image + avg_image, 0, 255).astype(np.uint8)
#avg_image = np.clip((frames - median_image).sum(0), 0, 255)
#avg_image = np.clip(median_image + (frames - median_image).mean(0), 0, 255)

#avg_image = frames.mean(0).astype(np.uint8)

mediapy.write_image(args.o, avg_image.astype(np.uint8))

directory, filename = os.path.split(args.o)
filename, _ = os.path.splitext(filename)
mediapy.write_video(os.path.join(directory, f'video_{filename}.mp4'), frames.astype(np.uint8), fps=20)