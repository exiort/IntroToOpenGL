# CENG 487 Assignment1 by
# Bugrahan Imal
# StudentId: 280201012
# April 2025

import time

class Timer:
    FPS:int
    TPF:float #Time per Frame
    
    last_time:float

    def __init__(self, FPS:int=30) -> None:
        self.FPS = FPS
        self.TPF = 1 / self.FPS
        self.last_time = time.time()

    def delta(self) -> float:
        now = time.time()
        dt = now - self.last_time
        self.last_time = now
        return dt

    def peak(self) -> float:
        return time.time() - self.last_time

    def is_next_frame(self) -> bool:
        if self.TPF > (time.time() - self.peak()):
            return False
        self.delta()
        return True
