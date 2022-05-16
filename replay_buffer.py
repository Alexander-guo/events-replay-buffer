from copy import deepcopy
from metavision_core.event_io import EventsIterator
from metavision_sdk_core import PeriodicFrameGenerationAlgorithm
from metavision_sdk_ui import EventLoop, BaseWindow, Window, UIAction, UIKeyEvent, MTWindow
from time import time, sleep
import _thread

class Replay_buffer():
    def __init__(self, input_path="", start_ts=0, mode="delta_t", delta_t=40000, n_events=1000, 
    max_duration=None, relative_timestamps=False, accum_time=20000, replay_time=2, slow_scale=5):
        self.events_iterator = EventsIterator(input_path=input_path, 
                                            start_ts=start_ts, mode=mode, 
                                            delta_t=delta_t, 
                                            n_events=n_events, 
        max_duration=max_duration, relative_timestamps=relative_timestamps)
        self.accum_time = accum_time
        self.global_counter = 0  # track how many events we processed
        self.global_max_t = 0  # track the highest timestamp we processed
        self.replay_time = replay_time  # time intervel to replay in [s]
        self.rply_buffer = []  # replay buffer to keep the lastest events of an interval
        self.rply_buffer_size = int(replay_time * 1.0e6 / delta_t)  # the number of events slices the replay buffer keeps
        self.height, self.width = self.events_iterator.get_size() # Camera Geometry
        self.should_clear = False
        self.slow_scale = slow_scale

    def run(self):
       
        # Window - Graphical User Interface
        with Window(title="Real-time Play", width=self.width, height=self.height, mode=BaseWindow.RenderMode.BGR) as window:
            def keyboard_cb(key, scancode, action, mods):
                if action != UIAction.RELEASE:
                    return
                if key == UIKeyEvent.KEY_Q or key == UIKeyEvent.KEY_ESCAPE:
                    window.set_close_flag()
                    self.should_clear = True
                if key == UIKeyEvent.KEY_SPACE and len(self.rply_buffer) == self.rply_buffer_size:
                    self.should_clear = False
                    print("--------Open Replay Window--------")
                    t_rply1 = time()
                    self.replay_callback()
                    self.should_clear = True
                    t_rply2 = time()
                    print("replay time: {} s".format(t_rply2 - t_rply1))
                    print("--------Close Replay Window--------")
                    
            window.set_keyboard_callback(keyboard_cb)

            # Event Frame Generator
            event_frame_gen = PeriodicFrameGenerationAlgorithm(self.width, self.height, self.accum_time)

            def on_cd_frame_cb(ts, cd_frame):
                #print("Before window ", time())
                window.show(cd_frame)
                #print("After window ", time())

            event_frame_gen.set_output_callback(on_cd_frame_cb)

            t1 = time()
            t2 = 0
            i = 0

            # evs is a list of tuples, each tuple is an event
            for evs in self.events_iterator:

                # Dispatch system events to the window
                EventLoop.poll_and_dispatch()
                #print("Before processing ", time())
                event_frame_gen.process_events(evs)
                #print("current fps: ", event_frame_gen.get_fps())

                #print("----- New Event Buffer -----")
                if evs.size == 0:
                    #print("The current event buffer is empty!")
                    continue
                else:
                    min_t = evs['t'][0]   # Get the timestamp of the first event of this callback
                    max_t = evs['t'][-1]  # Get the timestamp of the last event of this callback
                    self.global_max_t = max_t     
                    counter = evs.size  # Local counter
                    self.global_counter += counter  # Increase global counter 
                    #print(f"There were {counter} events in this event buffer.")
                    #print(f"There were {self.global_counter} total events up to now.")
                    #print(f"The current event buffer included events from {min_t} to {max_t} microseconds.")
                    #print("----- End of the event buffer! -----")
                    
                    # updata the replay buffer
                    if len(self.rply_buffer) < self.rply_buffer_size:
                        self.rply_buffer.append(evs)
                    else:
                        self.rply_buffer.append(evs)  # add the lastest evs slice
                        popped = self.rply_buffer.pop(0)  # remove the first evs slice
                        del popped
                        #print("replay buffer size: ", len(self.rply_buffer))
                    

                if window.should_close():
                    break
                
                # test the time
                i += 1
                if i % 10 == 0:
                    t3 = time()
                    #print("time to run {} iterations: {} s".format(i, t2 - t1))
                    #print("avg time to run each iteration: {} ms".format((t3 - t2) / 10.0 * 1e3))
                    #print("evs: ", evs)
                    t2 = t3


    def replay_callback(self):
        rply_buffer = deepcopy(self.rply_buffer)

        def make_window():
            with Window(title="Replay Window", width=self.width, height=self.height, mode=BaseWindow.RenderMode.BGR) as rply_window:
                def keyboard_cb(key, scancode, action, mods):
                    if action != UIAction.RELEASE:
                        return
                    if key == UIKeyEvent.KEY_ESCAPE or key == UIKeyEvent.KEY_Q:
                        rply_window.set_close_flag()

                rply_window.set_keyboard_callback(keyboard_cb)

                # Event Frame Generator
                rply_event_frame_gen = PeriodicFrameGenerationAlgorithm(self.width, self.height, int(self.accum_time/self.slow_scale))

                def on_cd_frame_cb(ts, cd_frame):
                    rply_window.show(cd_frame)

                rply_event_frame_gen.set_output_callback(on_cd_frame_cb)

                t_rply1 = time()
                first = True

                last_time = time()
                for evs in rply_buffer:
                    if first:
                        min_t = evs['t'][0]   # Get the timestamp of the first event of this callback
                        first = False
                    # Dispatch system events to the window
                    EventLoop.poll_and_dispatch()
                    rply_event_frame_gen.process_events(evs)

                    cur_time = time()
                    if cur_time - last_time < 0.02:
                        sleep(0.02 - (cur_time - last_time))
                    last_time = cur_time
                        
                    #print("replay fps: ", rply_event_frame_gen.get_fps())
                max_t = evs['t'][-1]   # Get the timestamp of the first event of this callback
                print("Event elapse: ", max_t - min_t)
                t_rply2 = time()
            #print("replay time: {} s".format(t_rply2 - t_rply1))

        _thread.start_new_thread(make_window, ())
