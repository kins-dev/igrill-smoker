import logging

import threading

import time

# So I started to build this test script woth the plan to
# cycle the power plug more often to keep at a particular
# temperature.  The problem is the relay is only rated for
# 100,000 cycles.  If I average 1 cycle every 10 seconds,
# that means it is good for only 1,000,000 seconds, or
# 16,666 minutes, or 277 hours, or 11 days.
#
# This is obviously not ideal.
#
# Option 1: Ignore it
# Option 2: Replace the relay
# Option 3: Build a board

# My current plan is to commit what I have for 1.3, 
# test it and start 2.0 with a control board


class ThreadRunner:
    def __init__(self):
        self.m_lastUpdate = 0
        self.m_onTime = 3.5
        self.m_offTime = 6.5
        self._lock = threading.Lock()

    def thread_function(self, name):

        logging.info("Thread %s: starting", name)
        with self._lock:
            self.m_lastUpdate = time.time()
            l_lastUpdate = self.m_lastUpdate
            l_onTime = self.m_onTime
            l_offTime = self.m_offTime
        while (l_onTime > 2 and l_offTime > 2 and l_lastUpdate > (time.time()-30)):
            l_startTime = time.time()
            logging.info("Thread 1: On")
            l_runTime = time.time() - l_startTime
            if (l_runTime < l_onTime):
                time.sleep(l_onTime - l_runTime)
            else:
                logging.error("Thread 1: On time is too short")
            l_startTime = time.time()
            logging.info("Thread 1: Off")
            l_runTime = time.time() - l_startTime
            if (l_runTime < l_offTime):
                time.sleep(l_offTime - l_runTime)
            else:
                logging.error("Thread 1: Off time is too short")
            with self._lock:
                l_lastUpdate = self.m_lastUpdate
                l_onTime = self.m_onTime
                l_offTime = self.m_offTime
        if(l_offTime <= 2):
            logging.info("Thread 1: On")
        logging.info("Thread 1: finishing")


if __name__ == "__main__":

    format = "%(asctime)s: %(message)s"

    logging.basicConfig(format=format, level=logging.INFO)


    logging.info("Main    : before creating thread")
    tr = ThreadRunner()
    x = threading.Thread(target=tr.thread_function, args=(1,), daemon=True)

    logging.info("Main    : before running thread")

    x.start()

    logging.info("Main    : wait for the thread to finish")

    x.join()

    logging.info("Main    : all done")