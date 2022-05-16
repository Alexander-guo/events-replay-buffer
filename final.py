from metavision_core.event_io import EventsIterator
from replay_buffer import *


def parse_args():
    import argparse
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Metavision SDK Get Started sample.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-i', '--input-raw-file', dest='input_path', default="",
        help="Path to input RAW file. If not specified, the live stream of the first available camera is used. "
        "If it's a camera serial number, it will try to open that camera instead.")
    args = parser.parse_args()
    return args


def main():
    """ Main """
    args = parse_args()

    ## Events iterator on Camera or RAW file
    #mv_iterator = EventsIterator(input_path=args.input_path, delta_t=1000, relative_timestamps=True)
    
    #global_counter = 0  # This will track how many events we processed
    #global_max_t = 0  # This will track the highest timestamp we processed

    ## Process events
    #for evs in mv_iterator:
        #print("----- New event buffer! -----")
        #if evs.size == 0:
            #print("The current event buffer is empty.")
        #else:
            #min_t = evs['t'][0]   # Get the timestamp of the first event of this callback
            #max_t = evs['t'][-1]  # Get the timestamp of the last event of this callback
            #global_max_t = max_t  # Events are ordered by timestamp, so the current last event has the highest timestamp

            #counter = evs.size  # Local counter
            #global_counter += counter  # Increase global counter

            #print(f"There were {counter} events in this event buffer.")
            #print(f"There were {global_counter} total events up to now.")
            #print(f"The current event buffer included events from {min_t} to {max_t} microseconds.")
            #print("----- End of the event buffer! -----")


    replay_buffer = Replay_buffer(input_path=args.input_path)
    replay_buffer.run()  # Run the loop

    #height, width = replay_buffer.events_iterator.get_size()  # Camera Geometry

    ## Window - Graphical User Interface
    #with Window(title="Metavision SDK Get Started", width=width, height=height, mode=BaseWindow.RenderMode.BGR) as window:
        #def keyboard_cb(key, scancode, action, mods):
            #if action != UIAction.RELEASE:
                #return
            #if key == UIKeyEvent.KEY_ESCAPE or key == UIKeyEvent.KEY_Q:
                #window.set_close_flag()

        #window.set_keyboard_callback(keyboard_cb)

        ## Event Frame Generator
        #event_frame_gen = PeriodicFrameGenerationAlgorithm(width, height, replay_buffer.accum_time)

        #def on_cd_frame_cb(ts, cd_frame):
            #window.show(cd_frame)

        #event_frame_gen.set_output_callback(on_cd_frame_cb)

        #for evs in replay_buffer.events_iterator:
            ## Dispatch system events to the window
            #EventLoop.poll_and_dispatch()
            #event_frame_gen.process_events(evs)

            #print("----- New Event Buffer -----")
            #if evs.size == 0:
                #print("The current event buffer is empty!")
                #continue
            #else:
                #min_t = evs['t'][0]   # Get the timestamp of the first event of this callback
                #max_t = evs['t'][-1]  # Get the timestamp of the last event of this callback
                #replay_buffer.global_max_t = max_t     
                #counter = evs.size  # Local counter
                #replay_buffer.global_counter += counter  # Increase global counter 
                #print(f"There were {counter} events in this event buffer.")
                #print(f"There were {replay_buffer.global_counter} total events up to now.")
                #print(f"The current event buffer included events from {min_t} to {max_t} microseconds.")
                #print("----- End of the event buffer! -----")

            #if window.should_close():
                #break

    ## Print the global statistics
    #duration_seconds = global_max_t / 1.0e6
    #print(f"There were {global_counter} events in total.")
    #print(f"The total duration was {duration_seconds:.2f} seconds.")
    #if duration_seconds >= 1:  # No need to print this statistics if the video was too short
        #print(f"There were {global_counter / duration_seconds :.2f} events per second on average.")
        
if __name__ == "__main__":
    main()