# from random import randrange
# from copy import deepcopy
# random.seed(1)
# from src.config import OrbitConfig
from typing import Optional, Tuple, Dict, List
import numpy as np




class Game:

    def __init__(self, name, position, velocity, mu, color, radius_ratio):
        r = np.array(position, dtype=float)
        v = np.array(velocity, dtype=float)
        self.mu = mu
        self.M = self.a = self.e = self.omega = self.n = None
        if r[0]:
            self.set_state(r, v)
        self.name = name
        self.color = color
        self.radius_ratio = radius_ratio

    def __str__(self):
        return f"{self.name}"

    def propagate(self, dt):
        """Advance epoch by dt seconds (update mean anomaly only)."""
        self.M = (self.M + self.n * dt) % (2 * np.pi)

    def get_state(self):
        """Return (r, v) from stored orbital elements."""

        # Solve Kepler’s equation
        E = self.solve_kepler(self.M, self.e)

        # True anomaly
        f = 2 * np.arctan(np.sqrt((1 + self.e) / (1 - self.e)) * np.tan(E / 2))

        # Radius
        r_mag = self.a * (1 - self.e * np.cos(E))
        r_pf = np.array([r_mag * np.cos(f), r_mag * np.sin(f)])

        # Velocity in perifocal coords
        rdot = np.sqrt(self.mu * self.a) / r_mag * np.array([-np.sin(E), np.sqrt(1 - self.e ** 2) * np.cos(E)])

        # Rotate by omega
        R = np.array([[np.cos(self.omega), -np.sin(self.omega)],
                      [np.sin(self.omega), np.cos(self.omega)]])

        r = R @ r_pf
        v = R @ rdot
        return r, v

    def set_state(self, r, v):
        # convert Cartesian state -> orbital elements
        rnorm = np.linalg.norm(r)
        vnorm = np.linalg.norm(v)

        # Specific orbital energy → semi-major axis
        energy = vnorm ** 2 / 2 - self.mu / rnorm
        self.a = -self.mu / (2 * energy)

        # Eccentricity vector
        e_vec = (1 / self.mu) * ((vnorm ** 2 - self.mu / rnorm) * r - np.dot(r, v) * v)
        self.e = np.linalg.norm(e_vec)

        # argument of periapsis
        self.omega = np.arctan2(e_vec[1], e_vec[0])

        # true anomaly
        f = np.arctan2(r[1], r[0]) - self.omega

        # eccentric anomaly
        E = 2 * np.arctan(np.tan(f / 2) * np.sqrt((1 - self.e) / (1 + self.e)))
        if E < 0:
            E += 2 * np.pi

        # mean anomaly
        self.M = E - self.e * np.sin(E)

        # Mean motion
        self.n = np.sqrt(self.mu / self.a ** 3)

    @staticmethod
    def solve_kepler(M, e, tol=1e-10, max_iter=50):
        E = M if e < 0.8 else np.pi
        for _ in range(max_iter):
            f = E - e * np.sin(E) - M
            fprime = 1 - e * np.cos(E)
            dE = -f / fprime
            E += dE
            if abs(dE) < tol:
                break
        return E

    def add_delta_v(self, delta_v):
        """Apply instantaneous delta_v (updates elements via set_state)."""
        r, v = self.get_state()
        v_unit_vector = v / np.linalg.norm(v)
        v_new = v + np.array(delta_v) * v_unit_vector
        self.set_state(r, v_new)

    def periapsis(self):
        return self.a * (1 - self.e), self.omega

    def apoapsis(self):
        return self.a * (1 + self.e), (self.omega + np.pi) % (2*np.pi)


class GameModel:

    def __init__(self, config: OrbitConfig = None):
        self.config = config or OrbitConfig()

        self.star = Game("Star", (0.0, 0.0), (0.0, 0.0), self.config.mu,
                         self.config.planet_color, self.config.planet_radius)
        self.ships = \
            [Game("ship1", self.config.ship_position, self.config.ship_velocity, self.config.mu,
                  self.config.ship_color, self.config.ship_radius),
             Game("debris", self.config.debris_position, self.config.debris_velocity, self.config.mu,
                  self.config.debris_color, self.config.debris_radius)]
        self.collided_with_star = False
        self.caught_satellite = False

    def change_orbit(self, is_increase):
        if is_increase:
            self.ships[0].add_delta_v(self.config.delta_v)
        else:
            self.ships[0].add_delta_v(-self.config.delta_v)

    def update(self):
        for ship in self.ships:
            ship.propagate(self.config.dt)
        self.collided_with_star = self.detect_collision([self.ships[0], self.star])
        self.caught_satellite = self.detect_collision([self.ships[0], self.ships[1]])

    @staticmethod
    def extract_orbital_data(planet: 'Game') -> Tuple[Tuple[np.ndarray, np.ndarray], Dict]:
        """
        Extract orbital data from a Planet object for autopilot.

        Args:
            planet: Planet object from GameModel

        Returns:
            ((position, velocity), orbital_elements_dict)
        """
        state = planet.get_state()
        elements = {
            'a': planet.a,
            'e': planet.e,
            'M': planet.M,
            'n': planet.n,
            'omega': planet.omega
        }
        return state, elements

    def detect_collision(self, ships):
        positions = []
        for ship in ships:
            if ship.name == 'Star':
                position = [0.0, 0.0]
            else:
                position = ship.get_state()[0]
            positions.append(position)
        positions = [[axis / self.config.world_radius for axis in position] for position in positions]

        is_collision = ((positions[0][0] - positions[1][0]) ** 2 + (positions[0][1] - positions[1][1]) ** 2 <=
                        (ships[0].radius_ratio + ships[1].radius_ratio) ** 2)
        return is_collision

    def reset(self):
        pass


if __name__ == '__main__':
    model = GameModel()
    for _ in range(100):
        model.update()
