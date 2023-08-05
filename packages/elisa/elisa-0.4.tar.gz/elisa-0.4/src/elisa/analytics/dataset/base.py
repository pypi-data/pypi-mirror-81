import numpy as np

from abc import ABCMeta
from copy import copy, deepcopy
from . transform import (
    RVDataProperties,
    LCDataProperties
)
from .. dataset.graphic import plot
from .. dataset import utils as dutils
from ... logger import getLogger
from ... import utils, units as u
from ... import settings
from ... utils import is_empty

logger = getLogger('analytics.dataset.base')


class DataSet(metaclass=ABCMeta):
    TRANSFORM_PROPERTIES_CLS = None
    ID = 1

    def __init__(self, name=None, **kwargs):
        # initial kwargs
        self.kwargs = copy(kwargs)
        self.plot = plot.Plot(self)

        if is_empty(name):
            self.name = str(DataSet.ID)
            logger.debug(f"name of class instance {self.__class__.__name__} set to {self.name}")
            DataSet.ID += 1
        else:
            self.name = str(name)

        # initializing parmas to default values
        self.x_data = np.array([])
        self.x_unit = None
        self.y_data = np.array([])
        self.y_err = None

        self.check_data_validity(**kwargs)

    def transform_input(self, **kwargs):
        return self.__class__.TRANSFORM_PROPERTIES_CLS.transform_input(**kwargs)

    def copy(self):
        return deepcopy(self)

    @staticmethod
    def check_data_validity(**kwargs):
        if not np.shape(kwargs['x_data']) == np.shape(kwargs['y_data']):
            raise ValueError('`x_data` and `y_data` are not of the same shape.')
        if 'y_err' in kwargs.keys():
            if not np.shape(kwargs['x_data']) == np.shape(kwargs['y_err']):
                raise ValueError('`y_err` are not of the same shape to `x_data` and `y_data`.')

        # check for nans
        if np.isnan(kwargs['x_data']).any():
            raise ValueError('`x_data` contains NaN')
        if np.isnan(kwargs['y_data']).any():
            raise ValueError('`y_data` contains NaN')
        if 'y_err' in kwargs.keys():
            if np.isnan(kwargs['y_err']).any():
                raise ValueError('`y_err` contains NaN')

    @classmethod
    def load_from_file(cls, filename, x_unit=None, y_unit=None, data_columns=None,
                       delimiter=settings.DELIM_WHITESPACE, **kwargs):
        """
        Function loads a RV/LC measurements from text file.

        :param filename: str; name of the file
        :param x_unit: astropy.unit.Unit;
        :param y_unit: astropy.unit.Unit;
        :param data_columns: Tuple; ordered tuple with column indices of x_data, y_data, y_errors
        :param delimiter: str; regex to define columns separtor
        :param kwargs: Dict;
        :**kwargs options**:
            * **reference_magnitude** * -- float; zero point for magnitude conversion in case of LCData

        :return: Union[RVData, LCData];
        """
        data_columns = (0, 1, 2) if data_columns is None else data_columns
        data = dutils.read_data_file(filename, data_columns, delimiter=delimiter)

        try:
            errs = data[:, 2]
        except IndexError:
            errs = None
        return cls(x_data=data[:, 0],
                   y_data=data[:, 1],
                   y_err=errs,
                   x_unit=x_unit,
                   y_unit=y_unit,
                   **kwargs)

    from_file = load_from_file

    def convert_to_phases(self, period, t0, centre=0.0):
        """
        Function converts DataSet with x_data in time unit to dimensionless phases according to an ephemeris.

        :param period: float;
        :param t0: float;
        :param centre: float; phase curve will be centered around this phase
        :return:
        """
        start_phase = centre - 0.5
        t0 += start_phase * period
        self.x_data = ((self.x_data - t0) / period) % 1.0 + start_phase
        self.x_unit = u.dimensionless_unscaled

    def convert_to_time(self, period, t0, to_unit=u.PERIOD_UNIT):
        """
        Function converts DataSet with x_data in dimensionless phases to time according to an ephemeris.

        :param period:
        :param t0:
        :param to_unit:
        :return:
        """
        self.x_data = self.x_data * period + t0
        self.x_unit = to_unit

    def smooth(self, method='central_moving_average', **kwargs):
        available_methods = ['central_moving_average']
        if method == 'central_moving_average':
            n_bins = kwargs.get('n_bins', 100)
            radius = kwargs.get('radius', 2)
            cyclic_boundaries = kwargs.get('cyclic_boundaries', True)
            dutils.central_moving_average(self, n_bins=n_bins, radius=radius, cyclic_boundaries=cyclic_boundaries)
        else:
            raise NotImplementedError(f'Method {method} is not implemented. Try one of these: {available_methods}')


class RVData(DataSet):
    """
    Child class of elisa.analytics.dataset.base.Dataset class storing radial velocity measurement.

    Input parameters:

    :param x_data: numpy.array; time or observed phases
    :param y_data: numpy.array; radial velocities
    :param y_err: numpy.array; radial velocity errors - optional
    :param x_unit: astropy.unit.Unit; if `None` or `astropy.unit.dimensionless_unscaled` is given,
                                      the `x_data are regarded as phases, otherwise if unit is convertible
                                      to days, the `x_data` are regarded to be in JD
    :param y_unit: astropy.unit.Unit; velocity unit of the observed radial velocities and its errors
    """

    MANDATORY_KWARGS = settings.DATASET_MANDATORY_KWARGS
    OPTIONAL_KWARGS = settings.DATASET_OPTIONAL_KWARGS
    ALL_KWARGS = MANDATORY_KWARGS + OPTIONAL_KWARGS
    TRANSFORM_PROPERTIES_CLS = RVDataProperties

    __slots__ = ALL_KWARGS

    def __init__(self, name=None, **kwargs):
        utils.invalid_kwarg_checker(kwargs, self.__slots__, RVData)
        utils.check_missing_kwargs(self.MANDATORY_KWARGS, kwargs, instance_of=RVData)
        super().__init__(name, **kwargs)

        kwargs = self.transform_input(**kwargs)

        # conversion to base units
        kwargs = self.convert_arrays(**kwargs)
        self.check_data_validity(**kwargs)
        self.init_parameters(**kwargs)

    def init_parameters(self, **kwargs):
        logger.debug(f"initialising properties of class instance {self.__class__.__name__}")
        for kwarg in RVData.ALL_KWARGS:
            if kwarg in kwargs:
                setattr(self, kwarg, kwargs[kwarg])

    @staticmethod
    def convert_arrays(**kwargs):
        """
        Converting data and units to its base counterparts or keeping them dimensionless.

        :param kwargs: Dict;
        :return: Dict;
        """
        # converting x-axis
        kwargs['x_data'] = dutils.convert_data(kwargs['x_data'], kwargs['x_unit'], u.PERIOD_UNIT)
        kwargs['x_unit'] = dutils.convert_unit(kwargs['x_unit'], u.PERIOD_UNIT)

        # converting y-axis
        kwargs['y_data'] = dutils.convert_data(kwargs['y_data'], kwargs['y_unit'], u.VELOCITY_UNIT)

        # convert errors
        if 'y_err' in kwargs.keys():
            kwargs['y_err'] = dutils.convert_data(kwargs['y_err'], kwargs['y_unit'], u.VELOCITY_UNIT)
        kwargs['y_unit'] = dutils.convert_unit(kwargs['y_unit'], u.VELOCITY_UNIT)

        return kwargs


class LCData(DataSet):
    """
        Child class of elisa.analytics.dataset.base.Dataset class storing radial velocity measurement.

        Input parameters:

        :param x_data: numpy.array; time or observed phases
        :param y_data: numpy.array; light curves
        :param y_err: numpy.array; light curve errors - optional
        :param x_unit: astropy.unit.Unit; if `None` or `astropy.unit.dimensionless_unscaled` is given,
                                          the `x_data` are regarded as phases, otherwise if unit is convertible
                                          to days, the `x_data` are regarded to be in JD
        :param y_unit: astropy.unit.Unit; velocity unit of the observed flux and its errors
    """
    MANDATORY_KWARGS = settings.DATASET_MANDATORY_KWARGS
    OPTIONAL_KWARGS = settings.DATASET_OPTIONAL_KWARGS + ['reference_magnitude', 'passband']
    ALL_KWARGS = MANDATORY_KWARGS + OPTIONAL_KWARGS
    TRANSFORM_PROPERTIES_CLS = LCDataProperties

    __slots__ = ALL_KWARGS

    def __init__(self, name=None, **kwargs):
        self.passband = None
        self.reference_magnitude = None

        utils.invalid_kwarg_checker(kwargs, self.__slots__, LCData)
        utils.check_missing_kwargs(self.MANDATORY_KWARGS, kwargs, instance_of=LCData)
        super().__init__(name, **kwargs)
        kwargs = self.transform_input(**kwargs)

        # conversion to base units
        kwargs = self.convert_arrays(**kwargs)
        self.check_data_validity(**kwargs)

        self.init_parameters(**kwargs)

    def init_parameters(self, **kwargs):
        logger.debug(f"initialising properties of class instance {self.__class__.__name__}")
        for kwarg in LCData.ALL_KWARGS:
            if kwarg in kwargs:
                setattr(self, kwarg, kwargs[kwarg])

    @staticmethod
    def convert_arrays(**kwargs):
        """
        Converting data and units to its base counterparts or keeping them dimensionless.

        :param kwargs: Dict;
        :return: Dict;
        """
        # converting x-axis
        kwargs['x_data'] = dutils.convert_data(kwargs['x_data'], kwargs['x_unit'], u.PERIOD_UNIT)
        kwargs['x_unit'] = dutils.convert_unit(kwargs['x_unit'], u.PERIOD_UNIT)
        kwargs['reference_magnitude'] = kwargs.get('reference_magnitude', None)

        # convert errors
        if 'y_err' in kwargs.keys():
            kwargs['y_err'] = dutils.convert_flux_error(kwargs['y_err'], kwargs['y_unit'],
                                                        zero_point=kwargs['reference_magnitude'])

        # converting y-axis
        kwargs['y_data'] = dutils.convert_flux(kwargs['y_data'], kwargs['y_unit'],
                                               zero_point=kwargs['reference_magnitude'])
        kwargs['y_unit'] = dutils.convert_unit(kwargs['y_unit'], u.dimensionless_unscaled)

        return kwargs
