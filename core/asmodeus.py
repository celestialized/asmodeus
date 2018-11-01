import argparse
import os
import sys
import logging
import time

from core import configuration, dataset
from utilities import colour as c

from models.observer import Observer

log = logging.getLogger('root')


class Asmodeus():
    def __init__(self):
        self.createArgparser()
        self.args = self.argparser.parse_args()

        self.loadConfig()
        self.overrideConfig()

        self.dataset = dataset.Dataset(self.config.dataset.name, self.config.observers)

    def createArgparser(self):
        self.argparser = argparse.ArgumentParser(description = "All-Sky Meteor Observation and Detection Efficiency Simulator")
        self.argparser.add_argument('config',               type = argparse.FileType('r'))
        self.argparser.add_argument('-d', '--debug',        action = 'store_true')
        self.argparser.add_argument('-p', '--processes',    type = int)
        self.argparser.add_argument('-D', '--dataset',      type = str)
        self.argparser.add_argument('-l', '--logfile',      type = argparse.FileType('w'))

    def loadConfig(self):
        self.config = configuration.load(self.args.config)

    def overrideConfig(self):
        log.setLevel(logging.DEBUG if self.args.debug else logging.INFO)

        if self.args.debug:
            log.warning("Debug output is {}".format(c.over('active')))

        if self.args.logfile:
            log.addHandler(logging.FileHandler(self.args.logfile.name))
            log.warning("Added log output {}".format(c.over(self.args.logfile.name)))

        if self.args.processes:
            self.overrideWarning('process count', self.config.mp.processes, self.args.processes)
            self.config.mp.processes = self.args.processes

        if self.args.dataset:
            self.overrideWarning('dataset', self.config.dataset.name, self.args.dataset)
            self.config.dataset.name = self.args.dataset

        self.config.dataset.path = os.path.join('datasets', self.config.dataset.name)

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

# Old crap below


def buildGnuplotTemplate(template, dataset, context, outputDirectory = None):
    print(
        jinjaEnv('templates').get_template(template).render(context),
        file = sys.stdout if outputDirectory is None else open(os.path.join(outputDirectory, template), 'w')
    )


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
