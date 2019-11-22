import datetime
import logging
import math
import io
import os
import numpy as np
import pickle

import models.frame

from physics import atmosphere, coord, radiometry, constants

log = logging.getLogger('root')


class State:
    def __init__(self, position, velocity, mass):
        self.position = position
        self.velocity = velocity
        self.mass = mass

    def __str__(self):
        return f"{self.position} {self.velocity} {self.mass}"


class Diff:
    def __init__(self, drdt, dvdt, dmdt):
        self.drdt = drdt
        self.dvdt = dvdt
        self.dmdt = dmdt


class Meteor:
    def __init__(self, *, mass, density, position, velocity, timestamp, drag_coefficient, **kwargs):
        self.mass               = mass
        self.density            = density
        self.radius             = (3 * self.mass / (self.density * math.pi * 4))**(1 / 3)

        self.position           = position
        self.velocity           = velocity

        self.timestamp          = timestamp
        self.time               = 0.0

        self.drag_coefficient   = drag_coefficient
        self.shape_factor       = kwargs.get('shape_factor', 1.21)
        self.heat_transfer      = kwargs.get('heat_transfer', 0.5)
        self.ablation_heat      = kwargs.get('ablation_heat', 8e6)

        self.luminous_power     = 0

        self.id                 = self.timestamp.strftime("%Y%m%d-%H%M%S-%f")
        self.frames             = []
        self.mass_initial       = self.mass

        log.debug(self.__str__())

    @staticmethod
    def load(filename):
        return Meteor.load_pickle(filename)

    @staticmethod
    def load_pickle(filename):
        return pickle.load(io.FileIO(filename, 'rb'))

    def __str__(self):
        return f"<Meteor {self.id} at {self.position}, velocity {self.velocity} | " \
            f"{self.density:4.0f} kg/m³, Q {self.ablation_heat:8.0f} J/kg, G {self.drag_coefficient:5.3f}, " \
            f"m {self.mass:8.6e} kg, r {self.radius * 1000:10.3f} mm, {len(self.frames)} frames>"

    def save(self, filename):
        pickle.dump(self, io.FileIO(os.path.join(filename, f"{self.id}x{datetime.datetime.now().strftime('%H%M%S%f')}.pickle"), 'wb'))

    def evaluate(self, state, diff, dt, node):
        new_state = State(
            state.position + diff.drdt * dt * node,
            state.velocity + diff.dvdt * dt * node,
            max(state.mass + diff.dmdt * dt * node, 1e-12)
        )
        air_density = atmosphere.air_density(new_state.position.norm() - constants.EARTH_RADIUS)
        speed = new_state.velocity.norm()

        return Diff(
            new_state.velocity,
            -(self.drag_coefficient * self.shape_factor * air_density * speed / (new_state.mass**(1 / 3) * self.density**(2 / 3))) * new_state.velocity
            - constants.GRAVITATIONAL_CONSTANT * constants.EARTH_MASS / new_state.position.norm()**3 * new_state.position,
            -(self.heat_transfer * self.shape_factor * air_density * speed**3 * (new_state.mass / self.density)**(2 / 3) / (2 * self.ablation_heat)),
        )

    def step_RK4(self, state, dt):
        d0 = Diff(coord.Vector3D(0, 0, 0), coord.Vector3D(0, 0, 0), 0.0)
        d1 = self.evaluate(state, d0, dt,   0)
        d2 = self.evaluate(state, d1, dt, 0.5)
        d3 = self.evaluate(state, d2, dt, 0.5)
        d4 = self.evaluate(state, d3, dt,   1)

        drdt = (d1.drdt + 2 * d2.drdt + 2 * d3.drdt + d4.drdt) / 6.0
        dvdt = (d1.dvdt + 2 * d2.dvdt + 2 * d3.dvdt + d4.dvdt) / 6.0
        dmdt = (d1.dmdt + 2 * d2.dmdt + 2 * d3.dmdt + d4.dmdt) / 6.0

        return drdt, dvdt, dmdt

    def fly_RK4(self, fps, spf):
        dt = 1.0 / (fps * spf)
        frame = 0

        while True:
            drdt, dvdt, dmdt = self.step_RK4(State(self.position, self.velocity, self.mass), dt)

            speed = self.velocity.norm()
            air_density = atmosphere.air_density(self.position.elevation())

            self.luminous_power = -(radiometry.luminous_efficiency(speed) * dmdt * speed**2 / 2.0)
            self.absolute_magnitude = radiometry.absolute_magnitude(self.luminous_power)
            #print(-self.position * self.velocity / (self.position.norm() * speed) - 1e-10)
            self.entry_angle = math.degrees(math.asin(-self.position * self.velocity / (self.position.norm() * speed) - 1e-10))
            self.radius = ((3 * self.mass) / (4 * np.pi * self.density))**(1 / 3)

            self.reynolds_number = 2 * self.radius * self.velocity.norm() * air_density / constants.AIR_VISCOSITY

            if (frame % spf == 0):
                self.frames.append(models.frame.Frame(self))
                log.debug(
                    f"{self.time:6.3f} s | "
                    f"{self.position.latitude():6.4f} N, {self.position.longitude():6.4f} E, {self.position.elevation():6.0f} m, "
                    f"{self.entry_angle:6.2f}° | "
                    f"{air_density:9.3e} kg/m³ | "
                    f"{self.velocity.norm():7.1f} m/s, "
                    f"{dvdt.norm():13.3f} m/s², "
                    f"{radiometry.luminous_efficiency(self.velocity.norm()):6.4f} "
                    f"{self.reynolds_number:10.3f} | "
                    f"{self.mass:6.2e} kg, {dmdt:9.3e} kg/s, "
                    f"{self.radius * 1000:7.3f} mm | "
                    f"{self.luminous_power:10.3e} W, "
                    f"{self.absolute_magnitude:6.2f}m"
                )

            frame += 1

            self.position += drdt * dt
            self.velocity += dvdt * dt
            self.mass     += dmdt * dt

            # Advance time by dt
            self.timestamp += datetime.timedelta(seconds = dt)
            self.time += dt

            # If all mass has been ablated away, the particle is pronounced dead
            if self.mass < 0:
                log.debug("Burnt to death")
                break

            # If the particle flew above 400 km, it will likely leave Earth altogether
            if self.position.elevation() > 400000:
                log.debug("Flew away")
                break

            # If the velocity is very low, it is a meteorite
            if self.velocity.norm() < 1:
                log.debug(f"Survived with final mass {self.mass:12.6f} kg")
                break

            # If the elevation is below zero, we have an impact
            if self.position.elevation() < 0:
                log.debug("IMPACT")
                break

        log.debug(f"Meteor generated ({len(self.frames)} frames)")

    def reduce_to_point(self):
        max_light = np.inf

        for frame in self.frames:
            if frame.absolute_magnitude < max_light:
                max_light = frame.absolute_magnitude

        self.frames = [frame]

    def simulate(self):
        self.fly_RK4()
        self.save()
