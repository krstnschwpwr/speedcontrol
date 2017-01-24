import time
import sched

from django.core.management import BaseCommand


class Scheduler(object):
    def __init__(self):
        self.scheduler = sched.scheduler(time.time, time.sleep)

    def measure_time(self, method):
        start = time.time()
        method()
        end = time.time()
        return end - start + ((end - start) / 2)

    def __init_workers(self):
        from probe.management.commands.prtg_push import push
        from probe.management.commands.fill_values import fill, calc_qos
        self.scheduler.enter(self.measure_time(fill), 1, fill)
        self.scheduler.enter(self.measure_time(calc_qos), 1, calc_qos)
        self.scheduler.enter(self.measure_time(push), 1, push)

    def start(self):
        self.__init_workers()
        while True:
            self.scheduler.run()
            time.sleep(1)


class Command(BaseCommand):
    def handle(self, *args, **options):
        scheduler = Scheduler()
        scheduler.start()
