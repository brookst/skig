#!/usr/bin/env python3
"""Overlay data onto video file"""

from __future__ import print_function
import matplotlib.pyplot as plt
import numpy as np
from numpy import empty as empty_array
from moviepy.editor import (VideoFileClip, VideoClip, TextClip, ImageClip,
                            CompositeVideoClip, concatenate)
from moviepy.video.io.bindings import mplfig_to_npimage


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


def mplfig_to_mask(fig):
    """Extract alpha channel of fig"""
    fig.canvas.draw()
    width, height = fig.canvas.get_width_height()
    # Get alpha and RGB data
    buf = fig.canvas.tostring_argb()
    image = +np.fromstring(buf, dtype=np.uint8)
    # Rescale image to float in range [0, 1]
    return image.reshape(height, width, 4)[:, :, 0].astype(float) * (1/255)


def make_graph_overlays(data, fill=False, ylim=None):
    """Make overlay plot"""
    window_size = 5
    if ylim is None:
        ylim = (0, np.max(data))
    time = data[:, 0]
    index = np.sum(data[:, 0] < window_size)
    figure, axis = plt.subplots(1, figsize=(4, 2.5), facecolor=(1, 1, 1))
    series, = axis.plot(data[:index, 0], data[:index, 1],
                        lw=2, c='k')
    axis.set_xlim(-window_size, 0)
    axis.set_ylim(0, 3)
    axis.set_ylabel("Acceleration [g]")
    axis.legend(loc=2)
    figure.tight_layout()

    figure.patch.set_facecolor('none')
    mask = ImageClip(mplfig_to_mask(figure), ismask=True)
    figure.patch.set_facecolor('white')

    if fill:
        reference = np.ones(time.size) * fill

    duration = data[-1, 0]
    series.set_ydata(data[:, 1])

    def plot(timestamp):
        """make_frame function for VideoClip"""
        offset_time = data[:, 0] - timestamp
        series.set_xdata(offset_time)

        # Remove the fill_between patches. See:
        # http://stackoverflow.com/questions/16120801/matplotlib-animate-fill-between-shape
        if fill:
            for coll in axis.collections:
                axis.collections.remove(coll)
            axis.fill_between(offset_time, data[:, 1], reference,
                              interpolate=True,
                              where=data[:, 1] >= reference,
                              facecolor='red')
            axis.fill_between(offset_time, data[:, 1], reference,
                              interpolate=True,
                              where=data[:, 1] <= reference,
                              facecolor='blue')
        return mplfig_to_npimage(figure)

    return VideoClip(plot, duration=duration).set_mask(mask)


def render(clips, file_name="test.mp4", bitrate=30000):
    """Composite a stack of clips together and render to file"""
    composite = CompositeVideoClip(clips)
    composite.write_videofile(file_name, codec='mpeg4',
                              bitrate=str(bitrate * 1000), write_logfile=True)


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
    for index, number in enumerate(numbers):
        number[0] = frame_time * index
        number[1] = index

    # Overlay frame number onto video
    # overlays = make_overlays(numbers, lambda x: "Frame #%05d" % int(x))
    overlays = make_graph_overlays(numbers)
    render([video, overlays])

if __name__ == '__main__':
    demo()
