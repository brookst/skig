#!/usr/bin/env python3
"""Overlay G-load data on video"""

from __future__ import print_function
from data import from_file, differentiate
from overlay import make_overlays, render
from moviepy.editor import VideoFileClip


def demo():
    """Proof of principle"""
    g_data = differentiate(from_file('Acceleration_data.xlsx',
                                     'Corviglia 30.12.'))
    # TODO: Ask for the time offset of data to video
    g_data[0, 0] += 0.68
    overlays = make_overlays(g_data, lambda x: "%4.2f g" % x)
    video = VideoFileClip("GOPR0068.MP4", audio=True)
    render([video, overlays], "output2.mp4")

if __name__ == '__main__':
    demo()
