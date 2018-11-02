#!/usr/bin/env python
"""
    Computes apparent positions and magnitudes for all observers as defined in the configuration file,
    using generated meteors saved in dataset `meteors` directory
    Requires: meteors
    Outputs: sightings
"""

import multiprocessing as mp

from core               import asmodeus, logger
from utilities          import colour as c

from models.meteor import Meteor
from models.sighting import Sighting


class AsmodeusObserve(asmodeus.Asmodeus):
    def __init__(self):
        log.info("Initializing {}".format(c.script("asmodeus-observe")))
        super().__init__()
        self.configure()
    
    def createArgparser(self):
        super().createArgparser()
        self.argparser.add_argument('-s', '--streaks', action = 'store_true')

    def overrideConfig(self):
        super().overrideConfig()
        if (self.args.streaks):
            self.overrideWarning('streaks', self.config.observations.streaks, self.args.streaks)
            self.config.observations.streaks = True

    def configure(self):
        self.loadObservers()
        self.dataset.require('meteors')

        self.dataset.reset('sightings')
        for observer in self.observers:
            self.dataset.create('sightings', observer.id)

    def observe(self):
        self.markTime()
        pool        = mp.Pool(processes = self.config.mp.processes)
        meteorFiles = self.dataset.list('meteors')

        results = [
            pool.apply_async(
                observeMeteor, (
                    observer,
                    self.dataset.path('meteors', meteorFile),
                    self.config.observations.minAltitude,
                    self.dataset.path('sightings', observer.id, meteorFile),
                    self.config.observations.streaks,
                )
            ) for meteorFile in meteorFiles for observer in self.observers
        ]
        out = [result.get() for result in results]

        log.info("{num} observations were processed in {time} seconds ({rate} meteors per second)".format(
            num     = c.num(len(out)),
            time    = c.num("{:.6f}".format(self.runTime())),
            rate    = c.num("{:.3f}".format(len(out) / self.runTime())),
        ))
        log.info("Observations were saved as {target} to {dir}".format(
            target  = c.over('streaks' if self.config.observations.streaks else 'points'),
            dir     = c.path(self.dataset.path('sightings')),
        ))


def observeMeteor(observer, filename, minAlt, out, streaks):
    meteor = Meteor.load(filename)

    sighting = Sighting(observer, meteor)
    if sighting.brightestFrame.altAz.latitude() >= minAlt:
        sighting.save(out, streak = streaks)
        return True
    else:
        return False

if __name__ == "__main__":
    log = logger.setupLog('root')
    asmo = AsmodeusObserve()
    asmo.observe()
    log.info("---------------------")
