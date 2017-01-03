#!/usr/bin/env python3
"""Overlay data onto video file"""

from __future__ import print_function
from numpy import empty as empty_array
from moviepy.editor import (VideoFileClip, TextClip, CompositeVideoClip,
                            concatenate)


def make_overlays(data, form=lambda x: "Frame #%05d" % int(x)):
    """Make text overlay clips"""
    overlays = []
    for duration, index in data:
        print(duration, index)
        text = form(index)
        overlay = TextClip(text, fontsize=70, color='white',
                           stroke_color='black', stroke_width=2)\
            .set_duration(duration)\
            .set_position('top')
        overlays.append(overlay)

    return concatenate(overlays, method='compose')


def render(clips, file_name="test.mp4"):
    """Composite a stack of clips together and render to file"""
    composite = CompositeVideoClip(clips)
    # TODO: Note the bitrate is fixed here:
    composite.write_videofile(file_name, codec='mpeg4', bitrate="30000000",
                              write_logfile=True)


def demo():
    """Proof of principle"""
    # Snip 5 seconds of video
    video = VideoFileClip("GOPR0068.MP4", audio=True).subclip(0, 5)
    # Find the number of frames in the clip, and the duration of them
    frames = int(video.duration * video.fps)
    frame_time = float(video.duration)/frames
    print("video size: %s px" % str(video.size))
    print("video duration: %s s" % str(video.duration))
    print("video frames: %d" % frames)
    print("video frame length: %d s" % frames)

    numbers = empty_array([frames, 2], dtype=float)
    index = 0
    for number in numbers:
        number[0] = frame_time
        number[1] = index
        index += 2
        print(number)

    # Overlay frame number onto video
    overlays = make_overlays(numbers, lambda x: "Frame #%05d" % int(x))
    render([video, overlays])

if __name__ == '__main__':
    demo()
