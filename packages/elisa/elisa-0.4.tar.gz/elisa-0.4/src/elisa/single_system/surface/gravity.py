import numpy as np

from ... import const as c
from ... logger import getLogger
from ... base.surface import gravity as bgravity
from ... utils import is_empty
from ... pulse import pulsations

logger = getLogger("single_system.surface.gravity")


def build_surface_gravity(system_container):
    """
    Function calculates gravity potential gradient magnitude (surface gravity) for each face.
    """
    star_container = system_container.star

    polar_gravity = np.power(10, star_container.polar_log_g)

    star_container.polar_potential_gradient_magnitude = polar_gravity

    logger.debug('computing potential gradient magnitudes distribution on a star')
    points, faces = bgravity.eval_args_for_magnitude_gradient(star_container)

    g_acc_vector = calculate_potential_gradient(points, system_container.angular_velocity, star_container.mass)

    g_acc_vector_spot = dict()
    if star_container.has_spots():
        for spot_index, spot in star_container.spots.items():
            logger.debug(f'calculating surface SI unit gravity of {spot_index} spot')
            logger.debug(f'calculating distribution of potential gradient '
                         f'magnitudes of spot index: {spot_index} component')

            g_acc_vector_spot.update(
                {spot_index:
                     calculate_potential_gradient(spot.points, system_container.angular_velocity, star_container.mass)}
            )

    # TODO: here implement pulsations
    if star_container.has_pulsations():
        g_acc_vector, g_acc_vector_spot = \
            pulsations.incorporate_gravity_perturbation(star_container, g_acc_vector, g_acc_vector_spot,
                                                        phase=system_container.position.phase)

    gravity = np.mean(np.linalg.norm(g_acc_vector, axis=1)[faces], axis=1)
    setattr(star_container, 'potential_gradient_magnitudes', gravity[star_container.face_symmetry_vector]) \
        if star_container.symmetry_test() else setattr(star_container, 'potential_gradient_magnitudes', gravity)
    setattr(star_container, 'log_g', np.log10(star_container.potential_gradient_magnitudes))

    if star_container.has_spots():
        for spot_index, spot in star_container.spots.items():
            setattr(spot, 'potential_gradient_magnitudes',
                    np.mean(np.linalg.norm(g_acc_vector_spot[spot_index], axis=1)[spot.faces], axis=1))
            setattr(spot, 'log_g', np.log10(spot.potential_gradient_magnitudes))

    return system_container


def calculate_polar_potential_gradient_magnitude(polar_radius, mass):
    """
    Returns magnitude of polar gradient of gravitational potential.

    :param polar_radius: float;
    :param mass: float;
    :return: float;
    """
    points_z = polar_radius
    r3 = np.power(points_z, 3)
    domega_dz = c.G * mass * points_z / r3
    return domega_dz


# deprecated
def calculate_face_magnitude_gradient(points, faces, angular_velocity, mass, face_symmetry_vector=None):
    """
    Returns array of absolute values of potential gradients for corresponding faces.

    :param points: numpy.array; points in which to calculate magnitude of gradient, if False/None take star points
    :param faces: numpy.array; faces corresponding to given points
    :param angular_velocity: float;
    :param mass: float;
    :param face_symmetry_vector: Union[numpy.array, None];
    :return: numpy.array;
    """
    point_gradient_magnitudes = np.linalg.norm(calculate_potential_gradient(points, angular_velocity, mass), axis=1)
    face_gradient_magnitudes = np.mean(point_gradient_magnitudes[faces], axis=1)

    return face_gradient_magnitudes if is_empty(face_symmetry_vector) else \
        face_gradient_magnitudes[face_symmetry_vector]


def calculate_potential_gradient(points, angular_velocity, mass):
    """
    Returns array of gravity potential gradients for corresponding faces.

    :param points: numpy.array; (N * 3) array of surface points
    :param angular_velocity: float; angular velocity of rotation
    :param mass: float; stellar mass
    :return: numpy.array; gravity gradients for each face
    """
    r3 = np.power(np.linalg.norm(points, axis=1), 3)
    points_gradients = np.empty(points.shape)
    points_gradients[:, 0] = c.G * mass * points[:, 0] / r3 - np.power(angular_velocity, 2) * points[:, 0]
    points_gradients[:, 1] = c.G * mass * points[:, 1] / r3 - np.power(angular_velocity, 2) * points[:, 1]
    points_gradients[:, 2] = c.G * mass * points[:, 2] / r3

    return - points_gradients
