#!/usr/bin/env python3
"""Overlay G-load data on video"""
# pylint: disable=star-args

from __future__ import print_function
from os import path
from argparse import ArgumentParser
from moviepy.editor import VideoFileClip
from data import from_file
from overlay import make_graph_overlays, render


def get_args():
    """Parse command line arguments"""
    parser = ArgumentParser()
    add = parser.add_argument
    add('-i', '--input_video', action='store', default="GOPR0068.MP4")
    add('-d', '--input_data', action='store', default='Acceleration_data.xlsx')
    add('-o', '--output', action='store', default=None)
    add('-s', '--offset', action='store', type=int, default=0.68,
        help="Offset in seconds from data to video")
    add('-p', '--preview', action='store', nargs=2, type=int, default=None,
        help="Render preview from START to END", metavar=('START', 'END'))
    add('-b', '--bitrate', action='store', type=int, default=30000,
        help="Output bitrate in kbps")
    add('-f', '--fill', action='store', type=float, default=False,
        help="Fill plot to REF", metavar='REF')
    args = parser.parse_args()
    return args


def main():
    """Main interface"""
    args = get_args()
    g_data = from_file(args.input_data,
                       'Corviglia 30.12.')
    g_data[:, 0] += args.offset - g_data[0, 0]
    overlays = make_graph_overlays(g_data, fill=args.fill)
    video = VideoFileClip(args.input_video, audio=True)
    if args.preview is None:
        if args.output is None:
            overlays = overlays.subclip(0, video.duration)
            directory, name = path.split(args.input_video)
            args.output = path.join(directory, "ski-G_" + name)
    else:
        if args.preview[0] < 0:
            args.preview = [args.preview[0] + video.duration,
                            args.preview[1] + video.duration]
        overlays = overlays.subclip(*args.preview)
        video = video.subclip(*args.preview)
        if args.output is None:
            args.output = "ski-G_preview.mp4"
    render([video, overlays], args.output, args.bitrate)

if __name__ == '__main__':
    main()
