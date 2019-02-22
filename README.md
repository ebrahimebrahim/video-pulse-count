This will help to count red pulses in a video recording that contains a bright red pulse.

Dependencies: python3 with numpy, scipy, matplotlib, and opencv.

For help on usage:
```
count_pulses.py -h
```

Here is a suggested usage:
- First use `count_pulses.py --showframe 1 --window 40 vid.mp4`
and keep adjusting the 40 until you get the red pulse cropped nicely so that it pretty much fills the cropped image.
Here vid.mp4 is the path to the video file.
- Then use `count_pulses.py --window W --prominence 10 --frames 1000 vid.mp4`
and keep adjusting the 10 until it looks like you're picking out the right peaks in your count.
Here W is the value you found in the previous step.
- Finally, run `count_pulses.py --window W --prominence P vid.mp4` to get a peak count.
Here W and P are the values you found in the previous steps.
Inspect output graph to make sure it's working properly.
