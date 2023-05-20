from metavision_core.event_io import EventsIterator
from replay_buffer import *


def parse_args():
    import argparse
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Replay Buffer based on Metavision SDK.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-i', '--input-raw-file', dest='input_path', default="",
        help="Path to input RAW file. If not specified, the live stream of the first available camera is used. "
        "If it's a camera serial number, it will try to open that camera instead.")

    parser.add_argument(
        '--rply-time', dest = 'replay_time', default = 2, help = "The time interval of the replay buffer in second."
    )

    parser.add_argument('--slow-scale', dest = 'slow_scale', default = 5, help = "Times to slow down the replay.")
    args = parser.parse_args()
    return args


def main():
    """ Main """
    args = parse_args()

    replay_buffer = Replay_buffer(input_path=args.input_path, replay_time=float(args.replay_time), slow_scale=int(args.slow_scale))
    replay_buffer.run()  # Run the loop

if __name__ == "__main__":
    main()