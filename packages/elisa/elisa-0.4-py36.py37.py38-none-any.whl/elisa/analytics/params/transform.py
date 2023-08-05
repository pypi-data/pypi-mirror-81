"""
Transform to default float like units.
"""


import numpy as np

from .. params import conf
from ... import units as u
from ... base.transform import (
    TransformProperties,
    WHEN_FLOAT64,
    StarProperties, SpotProperties
)
from ... binary_system.transform import (
    BinarySystemProperties,
    RadialVelocityObserverProperties
)
from ... pulse.transform import PulsationModeProperties


def angular(value):
    """
    Transform all angular units to elisa default float expected unit.

    :param value: Union[(numpy.)float, (numpy.)int, astropy.units.quantity.Quantity]
    :return: float;
    """
    if isinstance(value, u.Quantity):
        value = np.float64(value.to(conf.DEFAULT_FLOAT_ANGULAR_UNIT))
    elif isinstance(value, WHEN_FLOAT64):
        value = np.float64(value)
    else:
        raise TypeError('Input of variable is not (numpy.)int or (numpy.)float '
                        'nor astropy.unit.quantity.Quantity instance.')
    return value


class BinaryInitialProperties(TransformProperties):
    @staticmethod
    def semi_major_axis(value):
        if isinstance(value, u.Quantity):
            value = np.float64(value.to(u.solRad))
        elif isinstance(value, WHEN_FLOAT64):
            value = np.float64(value)
        else:
            raise TypeError('Input of variable `semi_major_axis` is not (numpy.)int or (numpy.)float '
                            'nor astropy.unit.quantity.Quantity instance.')
        if value < 0:
            raise ValueError('Value of `semi_major_axis` cannot be negative.')
        return value

    @staticmethod
    def mass(value):
        if isinstance(value, u.Quantity):
            value = np.float64(value.to(conf.DEFAULT_FLOAT_MASS_UNIT))
        elif isinstance(value, WHEN_FLOAT64):
            value = np.float64(value)
        else:
            raise TypeError('User input is not (numpy.)int or (numpy.)float '
                            'nor astropy.unit.quantity.Quantity instance.')
        if value <= 0:
            raise ValueError("Invalid mass, use value > 0!")
        return value

    eccentricity = BinarySystemProperties.eccentricity
    argument_of_periastron = angular
    inclination = angular
    gamma = BinarySystemProperties.gamma
    period = BinarySystemProperties.period
    mass_ratio = RadialVelocityObserverProperties.mass_ratio
    asini = RadialVelocityObserverProperties.asini
    additional_light = BinarySystemProperties.additional_light
    primary_minimum_time = BinarySystemProperties.primary_minimum_time


class StarInitialProperties(StarProperties):
    mass = BinaryInitialProperties.mass


class SpotInitialProperties(SpotProperties):
    latitude = angular
    longitude = angular
    angular_radius = angular


class PulsationModeInitialProperties(PulsationModeProperties):
    mode_axis_theta = angular
    mode_axis_phi = angular
