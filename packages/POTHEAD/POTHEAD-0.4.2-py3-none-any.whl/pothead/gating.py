from time import sleep, time
from math import ceil

from psutil import Process, cpu_count, cpu_times

# How often to poll the CPU, compared to the moving-average of the job-start-interval
CPU_IDLE_POLL_DIVISOR = 20

# Polling the cpu-idle more often than this is bound to give noisy results
# If your application consumes jobs more often than this, pothead probably is not for you
CPU_IDLE_POLL_MIN_INTERVAL = 0.050

__all__ = ["wait_for_idle_cpus"]


class MovingAverage:
    def __init__(self, init=0, inertia=0.6):
        self.value = init
        self.speed = 1 - inertia
        self.inertia = inertia

    def update(self, value):
        self.value = (self.value * self.inertia) + (value * self.speed)
        return self.value


class WorkersRunning:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1
        return self

    def done(self):
        self.count -= 1


"""Timed measurement on an incrementing counter

Reads the counter, divides with time passed since last reading, and smooths the value using a moving average
"""


class InertialTimeDerivate:
    def __init__(self, func, initial, inertia):
        self.func = func
        self.last_value = self.func()
        self.last_check = time()
        self.inertial_value = MovingAverage(initial, inertia)

    def update(self):
        new_value = self.func()
        this_check = time()
        elapsed = this_check - self.last_check
        delta = new_value - self.last_value
        self.last_check = this_check
        self.last_value = new_value
        return self.inertial_value.update(delta / elapsed)


"""CPU-gated wait_for_slot implementation

Creates a wait_for_slot-callable that will let through at least one concurrent job, and additional jobs as
long as `count` cpu:s are idle. It is cgroup-aware, and will not allow current process and subprocesses to
consume more CPU than configured cgroup-limit.
"""


def wait_for_idle_cpus(required, *, max_concurrent=None, fixed_delay=0.2, inertia=0.7):
    workers = WorkersRunning()
    cpu_poll_interval = MovingAverage(1, 0.7)

    process = Process()

    def cpu_used_in_process():
        times = process.cpu_times()
        return times.user + times.system + times.children_user + times.children_system

    with open("/sys/fs/cgroup/cpu/cpu.cfs_quota_us", "rt") as quota, open(
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us", "rt"
    ) as period:
        quota = int(quota.read())
        if quota > 0:
            cpu_quota = quota / int(period.read())
            if not max_concurrent:
                max_concurrent = ceil(cpu_quota / required)

            # Precalculate the quota with headroom for a new job
            cpu_quota -= required
        else:
            cpu_quota = None
            if not max_concurrent:
                max_concurrent = ceil(cpu_count() / required)

    def wait_for_slot(halt):
        if workers.count > 0:
            sleep(fixed_delay)

        start_time = time()

        idle = InertialTimeDerivate(lambda: cpu_times().idle, 0, inertia)
        if cpu_quota:
            cpu_used = InertialTimeDerivate(cpu_used_in_process, cpu_count(), inertia)
        update_interval = max(cpu_poll_interval.value, CPU_IDLE_POLL_MIN_INTERVAL)
        while workers.count > 0 and not halt():
            sleep(update_interval)

            if (
                workers.count < max_concurrent
                and idle.update() >= required
                and (cpu_quota is None or cpu_used.update() <= cpu_quota)
            ):
                cpu_poll_interval.update((time() - start_time) / 20)
                break

        return workers.increment()

    return wait_for_slot
