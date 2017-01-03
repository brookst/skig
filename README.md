## Ski-G

Overlay acceleration data onto video of an activity.
Made in response to a [post][reddit] by [u/Warp_11].

[u/Warp_11]: https://www.reddit.com/user/Warp_11
[reddit]: https://www.reddit.com/r/Physics/comments/5lm0l9/skiing_gforce_animation/

## Use

Currently everything is hard coded so must be adjusted to work.
Paths to files need to be set, along with the data location within the spreadsheet set in `data.py`.
The time offset of data to video is added to the first frame in `skig.py`.
Also the output bitrate is fixed in `overlay.py` - this ought pick up the bitrate of the input video.

## Setup

Ski-G requires [MoviePy] and [OpenPyXL] along with [NumPy].
These are listed in `reqirements.txt` so you should be able to setup with Pip:

    pip install -r reqirements.txt

[MoviePy]: http://zulko.github.io/moviepy/
[OpenPyXL]: https://openpyxl.readthedocs.io/en/default/
[NumPy]: http://www.numpy.org/
