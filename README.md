# Events Replay Buffer

Events are pixel-level brightness changes recorded by DVS (Dynamic Vision Sensor). This buffer is able to replay live events stream or events recordings into super slow motion.

## Requirements

Base system requirements: Linux Ubuntu 20.04 or 22.04 64bit.

[Metavision SDK](https://docs.prophesee.ai/stable/installation/linux.html) is required to run the buffer.

## Run

1. Clone the repository and navigate to the folder
```bash
git clone https://github.com/Alexander-guo/events-replay-buffer.git
cd events-replay-buffer
```
2. Run the buffer
```bash
python final.py \
  --rply-time=2 \
  --slow-scale=10
```
`--rply-time` stands for how long a time interval to replay in seconds, `--slow-scale` is how many times to slow down. Press `SPACE` to start the replay.
