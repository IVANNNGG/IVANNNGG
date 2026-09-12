import cv2
import imageio
from PIL import Image
import numpy as np

def main():
    # 1. Load the background
    bg = Image.open('bottom_scene.png').convert("RGBA")
    
    # Scale background to 600px width to keep file size under 5MB for mobile
    target_w = 600
    target_h = int(bg.height * (target_w / bg.width))
    bg_scaled = bg.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    frames = []
    
    # 2. Open videos
    cap1 = cv2.VideoCapture('kolom1.mp4')
    cap2 = cv2.VideoCapture('kolom2.mp4')
    cap3 = cv2.VideoCapture('kolom3.mp4')
    
    vid_w = 200
    vid1_h = int(186 * (vid_w / 596))
    vid2_h = int(196 * (vid_w / 596))
    vid3_h = int(182 * (vid_w / 596))
    
    x_pos = (target_w - vid_w) // 2
    
    # Y positions scaled accordingly
    y1 = 25
    y2 = y1 + vid1_h + 20
    y3 = y2 + vid2_h + 20
    
    frame_idx = 0
    while True:
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()
        ret3, frame3 = cap3.read()
        
        if not (ret1 and ret2 and ret3):
            break
            
        # Skip every other frame to halve file size
        frame_idx += 1
        if frame_idx % 2 == 0:
            continue
            
        frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
        frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
        frame3 = cv2.cvtColor(frame3, cv2.COLOR_BGR2RGB)
        
        im1 = Image.fromarray(frame1).resize((vid_w, vid1_h), Image.Resampling.LANCZOS)
        im2 = Image.fromarray(frame2).resize((vid_w, vid2_h), Image.Resampling.LANCZOS)
        im3 = Image.fromarray(frame3).resize((vid_w, vid3_h), Image.Resampling.LANCZOS)
        
        canvas = bg_scaled.copy()
        canvas.paste(im1, (x_pos, y1))
        canvas.paste(im2, (x_pos, y2))
        canvas.paste(im3, (x_pos, y3))
        
        # Keep as RGBA for transparency
        frames.append(canvas)
        
    cap1.release()
    cap2.release()
    cap3.release()
    
    print(f"Generated {len(frames)} frames. Saving GIF...")
    # Use PIL to save animated GIF with transparency
    frames[0].save(
        'bottom_animated.gif',
        save_all=True,
        append_images=frames[1:],
        optimize=False,
        duration=int(1000/12), # 12 fps = ~83 ms per frame
        loop=0,
        disposal=2 # clear frame before rendering next (prevents ghosting with transparency)
    )
    print("Done!")

if __name__ == '__main__':
    main()
