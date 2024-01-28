import pygame
import sys
from moviepy.editor import VideoFileClip
import numpy as np
import time

ASCII_CHARS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~i!lI;:,\"^`'. "[::-1]

def gray_to_ascii(gray_val):
    return ASCII_CHARS[int(gray_val / 255 * (len(ASCII_CHARS) - 1))]

def ascii_art(surface, pixel_size, font_size):
    width, height = surface.get_size()
    reduced_width, reduced_height = width // pixel_size, height // pixel_size
    reduced_surface = pygame.transform.scale(surface, (reduced_width, reduced_height))
    pixels = pygame.surfarray.array3d(reduced_surface)
    gray_scale_image = np.dot(pixels[..., :3], [0.2989, 0.5870, 0.1140])
    ascii_surface = pygame.Surface((width, height))
    font = pygame.font.SysFont('Courier', font_size)

    for y in range(reduced_height):
        for x in range(reduced_width):
            average_color = pixels[x, y].astype(int)
            average_gray = int(gray_scale_image[x, y])

            # Enhancing color representation
            ascii_char = gray_to_ascii(average_gray)
            enhanced_color = (average_color[0], average_color[1], average_color[2], 255)
            text_surface = font.render(ascii_char, True, enhanced_color)
            ascii_surface.blit(text_surface, (x * pixel_size, y * pixel_size))

    return ascii_surface

def main(video_path, pixel_size, font_size):
    pygame.init()
    clip = VideoFileClip(video_path, target_resolution=None)
    video_size = (int(clip.size[0]), int(clip.size[1]))
    screen = pygame.display.set_mode(video_size)
    clock = pygame.time.Clock()

    frame_count = 0
    start_time = time.time()

    for frame in clip.iter_frames(fps=clip.fps, dtype="uint8"):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0,1))
        ascii_frame = ascii_art(frame_surface, pixel_size, font_size)
        screen.blit(ascii_frame, (0, 0))
        pygame.display.flip()
        clock.tick(clip.fps)

        frame_count += 1
        elapsed_time = time.time() - start_time
        if elapsed_time > 0:
            fps = frame_count / elapsed_time
            pygame.display.set_caption(f"ASCII Shader - FPS: {fps:.2f}")

if __name__ == "__main__":
    video_path = 'video.mp4'  # Replace with your video path
    pixel_size = 8  # Smaller for more detail
    font_size = 8  # Adjust as needed for clarity
    main(video_path, pixel_size, font_size)
