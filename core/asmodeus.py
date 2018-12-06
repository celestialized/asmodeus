import argparse
import os
import sys
import multiprocessing as mp
import logging
import time

from core import configuration, dataset, exceptions
from utilities import colour as c

from models.observer import Observer

log = logging.getLogger('root')


class Asmodeus():
    def __init__(self):
        log.info("Initializing {}".format(c.script("asmodeus-{}".format(self.name))))
        self.createArgparser()
        self.args = self.argparser.parse_args()
        self.ok = True

        try:
            self.config = configuration.load(self.args.config)
            self.overrideConfig()

            self.dataset = dataset.Dataset(os.path.splitext(os.path.basename(self.args.config.name))[0], self.config.observations.observers)
            self.configure()
        except exceptions.ConfigurationError as e:
            log.critical("Configuration error \"{}\", terminating".format(e))
            self.ok = False
            sys.exit(-1)
        except exceptions.OverwriteError as e:
            log.critical("Target directory {} already exists, terminating (use --overwrite)".format(e))
            self.ok = False
            sys.exit(-1)
        except exceptions.PrerequisiteError:
            log.critical("Missing prerequisites, aborting")
            self.ok = False
            sys.exit(-1)

    def __del__(self):
        if self.ok:
            log.info("{} finished successfully".format(c.script("asmodeus-{}".format(self.name))))
        log.info("-" * 50)

    def createArgparser(self):
        self.argparser = argparse.ArgumentParser(description = "All-Sky Meteor Observation and Detection Efficiency Simulator")
        self.argparser.add_argument('config',                   type = argparse.FileType('r'))
        self.argparser.add_argument('-d', '--debug',            action = 'store_true')
        self.argparser.add_argument('-p', '--processes',        type = int)
        self.argparser.add_argument('-D', '--dataset',          type = str)
        self.argparser.add_argument('-O', '--overwrite',        action = 'store_true')
        self.argparser.add_argument('-l', '--logfile',          type = argparse.FileType('w'))

    def overrideConfig(self):
        log.setLevel(logging.DEBUG if self.args.debug else logging.INFO)
        if self.args.debug:
            log.warning("Debug output is {}".format(c.over('active')))

        if self.args.overwrite:
            log.warning("Dataset overwrite {}".format(c.over('enabled')))
            self.config.overwrite = True
        else:
            self.config.overwrite = False

        if self.args.logfile:
            log.addHandler(logging.FileHandler(self.args.logfile.name))
            log.warning("Added log output {}".format(c.over(self.args.logfile.name)))

        if self.args.processes:
            self.overrideWarning('process count', self.config.mp.processes, self.args.processes)
            self.config.mp.processes = self.args.processes

        if self.args.dataset:
            self.overrideWarning('dataset', self.config.dataset.name, self.args.dataset)
            self.config.dataset.name = self.args.dataset

    def markTime(self):
        self.startTime = time.time()

    def runTime(self):
        return time.time() - self.startTime

    def loadObservers(self):
        self.observers = []
        for oid, obs in self.config.observations.observers.items():
            self.observers.append(Observer(oid, self.dataset, self.config.statistics.histograms, **obs.toDict()))

        log.info("Loaded {} observer{}:".format(len(self.observers), 's' if len(self.observers) > 1 else ''))
        for o in self.observers:
            log.info("    {}".format(o))

    def overrideWarning(self, parameter, old, new):
        log.warning("Overriding {parameter} ({old} -> {new})".format(
            parameter   = c.param(parameter),
            old         = c.over(old),
            new         = c.over(new),
        ))

    def parallel(self, function, args, *, action, period = 1):
        pool = mp.Pool(processes = self.config.mp.processes)
        manager = mp.Manager()
        queue = manager.Queue()
        total = len(args)

        results = pool.map_async(function, args, 20)
        
        while True:
            if results.ready():
                break
            else:
                log.info("{action}: {count} of {total} ({perc})".format(
                    action      = action,
                    count       = c.num("{:6d}".format(queue.qsize())),
                    total       = c.num("{:6d}".format(total)),
                    perc        = c.num("{:5.2f}%".format(queue.qsize() / total * 100)),
                ))
                time.sleep(period)

        return results.get()

# Old crap below

def createAmosHistograms(file):
    h = config.statistics.histograms
    histograms = {
        'altitude':         Histogram.load(file, 'altitude', h.altitude.min, h.altitude.max, h.altitude.bin, 1).normalize(),
        'azimuth':          Histogram.load(file, 'azimuth', h.azimuth.min, h.azimuth.max, h.azimuth.bin, 2).normalize(),
        'angularSpeed':     Histogram.load(file, 'angularSpeed', h.angularSpeed.min, h.angularSpeed.max, h.angularSpeed.bin, 3).normalize(),
        'magnitude':        Histogram.load(file, 'magnitude', h.magnitude.min, h.magnitude.max, h.magnitude.bin, 4).normalize(),
    }

    for name, histogram in histograms.items():
        histogram.tsv(open(datasetPath('histograms', 'amos-{}.tsv'.format(histogram.name)), 'w'))

    return histograms
