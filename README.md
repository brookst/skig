## Ski-G

Overlay acceleration data onto video of an activity.
Made in response to a [post][reddit] by [u/Warp_11].

[u/Warp_11]: https://www.reddit.com/user/Warp_11
[reddit]: https://www.reddit.com/r/Physics/comments/5lm0l9/skiing_gforce_animation/

## Use

Video and data files can be passed in on the command line. The location of data within the spreadsheet is currently hardcoded in `data.py`. The output bitrate is 30000 kbps by default - hopefully this can be read from the input video in the future.

    usage: skig.py [-h] [-i INPUT_VIDEO] [-d INPUT_DATA] [-o OUTPUT] [-s OFFSET]
                   [-p START END] [-b BITRATE] [-f REF]
    
    optional arguments:
      -h, --help            show this help message and exit
      -i INPUT_VIDEO, --input_video INPUT_VIDEO
      -d INPUT_DATA, --input_data INPUT_DATA
      -o OUTPUT, --output OUTPUT
      -s OFFSET, --offset OFFSET
                            Offset in seconds from data to video
      -p START END, --preview START END
                            Render preview from START to END
      -b BITRATE, --bitrate BITRATE
                            Output bitrate in kbps
      -f REF, --fill REF    Fill plot to REF

## Setup

Ski-G is written in [Python3] and requires [MoviePy] and [OpenPyXL] along with [NumPy].
These are listed in `reqirements.txt` so setup should be easy with Pip:

    pip install -r reqirements.txt

[Python3]: https://www.python.org/downloads/
[MoviePy]: http://zulko.github.io/moviepy/
[OpenPyXL]: https://openpyxl.readthedocs.io/en/default/
[NumPy]: http://www.numpy.org/
