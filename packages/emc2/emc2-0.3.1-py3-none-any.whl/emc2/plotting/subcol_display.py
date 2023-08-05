import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors

from act.plotting import Display


class SubcolumnDisplay(Display):
    """
    This class contains modules for displaying the generated subcolumn parameters as quicklook
    plots. It is inherited from `ACT <https://arm-doe.github.io/ACT>`_'s Display object. For more
    information on the Display object and its attributes and parameters, click `here
    <https://arm-doe.github.io/ACT/API/generated/act.plotting.plot.Display.html>`_. In addition to the
    methods in :code:`Display`, :code:`SubcolumnDisplay` has the following attributes and methods:

    Attributes
    ----------
    model: emc2.core.Model
        The model object containing the subcolumn data to plot.

    Examples
    --------
    This example makes a four panel plot of 4 subcolumns of EMC^2 simulated reflectivity::

    $ model_display = emc2.plotting.SubcolumnDisplay(my_model, subplot_shape=(2, 2), figsize=(30, 20))
    $ model_display.plot_subcolumn_timeseries('sub_col_Ze_cl_strat', 1, subplot_index=(0, 0))
    $ model_display.plot_subcolumn_timeseries('sub_col_Ze_cl_strat', 2, subplot_index=(1, 0))
    $ model_display.plot_subcolumn_timeseries('sub_col_Ze_cl_strat', 3, subplot_index=(0, 1))
    $ model_display.plot_subcolumn_timeseries('sub_col_Ze_cl_strat', 4, subplot_index=(1, 1))

    """
    def __init__(self, model, **kwargs):
        """

        Parameters
        ----------
        model: emc2.core.Model
            The model containing the subcolumn data to plot.

        Additional keyword arguments are passed into act.plotting.plot.Display's constructor.
        """
        if 'ds_name' not in kwargs.keys():
            ds_name = model.model_name
        else:
            ds_name = kwargs.pop('ds_name')
        super().__init__(model.ds, ds_name=ds_name, **kwargs)
        self.model = model

    def _switch_model(self, model):
        """

        Parameters
        ----------
        model: emc2.core.Model
            A model containing the subcolumn data to relpace the current model data.

        """
        self._arm.pop(self.model.model_name)
        self.model = model
        self._arm.update({self.model.model_name: self.model.ds})

    def set_yrng(self, subplot_index, y_range):
        """
        Set the Y axes limits of the subplot

        Parameters
        ----------
        subplot_index: tuple
            The index of the subplot to set the y axes limits to.
        y_range: tuple
            The y range of the plot.

        Returns
        -------

        """
        self.axes[subplot_index].set_ylim(y_range)

    def set_xrng(self, subplot_index, x_range):
        """
        Set the Y axes limits of the subplot

        Parameters
        ----------
        subplot_index: tuple
            The index of the subplot to set the y axes limits to.
        x_range: tuple
            The y range of the plot.

        Returns
        -------

        """
        self.axes[subplot_index].set_xlim(x_range)

    def plot_subcolumn_timeseries(self, variable,
                                  column_no, pressure_coords=True, title=None,
                                  subplot_index=(0, ), colorbar=True, cbar_label=None,
                                  log_plot=False, Mask_array=None, x_range=None, y_range=None,
                                  **kwargs):
        """
        Plots timeseries of subcolumn parameters for a given variable and subcolumn.

        Parameters
        ----------
        variable: str
            The subcolumn variable to plot.
        column_no: int
            The subcolumn number to plot.
        pressure_coords: bool
            Set to true to plot in pressure coordinates, false to height coordinates.
        title: str or None
            The title of the plot. Set to None to have EMC^2 generate a title for you.
        subplot_index: tuple
            The index of the subplot to make the plot in.
        colorbar: bool
            If true, plot the colorbar.
        cbar_label: None or str
            The colorbar label. Set to None to provide a default label.
        log_plot: bool
            Set to true to plot variable in logarithmic space.
        Mask_array: bool, int, or float (same dims as "variable")
            Set to true or to other values greater than 0 in grid cells to make them transparent.
        x_range: tuple, list, or None
            The x range of the plot (also accepts datetime64 format).
        y_range: tuple, list, or None
            The y range of the plot.
        Additional keyword arguments are passed into matplotlib's matplotlib.pyplot.pcolormesh.

        Returns
        -------
        axes: Matplotlib axes handle
            The matplotlib axes handle of the plot.
        cbar: Matplotlib axes handle
            The matplotlib colorbar handle of the plot.
        """
        ds_name = [x for x in self._arm.keys()][0]
        my_ds = self._arm[ds_name].sel(subcolumn=column_no)
        x_variable = self.model.time_dim
        if pressure_coords:
            y_variable = self.model.height_dim
        else:
            y_variable = self.model.z_field

        x_label = 'Time [UTC]'
        if "long_name" in my_ds[y_variable].attrs and "units" in my_ds[y_variable].attrs:
            y_label = '%s [%s]' % (my_ds[y_variable].attrs["long_name"],
                                   my_ds[y_variable].attrs["units"])
        else:
            y_label = y_variable

        if cbar_label is None:
            cbar_label = '%s [%s]' % (my_ds[variable].attrs["long_name"], my_ds[variable].attrs["units"])

        if pressure_coords:
            x = my_ds[x_variable].values
            y = my_ds[y_variable].values
            x, y = np.meshgrid(x, y)
        else:
            x = my_ds[x_variable].values
            y = my_ds[y_variable].values.T
            p = my_ds[self.model.height_dim].values
            x, p = np.meshgrid(x, p)

        var_array = my_ds[variable].values.T
        if Mask_array is not None:
            Mask_array = Mask_array.T
            if Mask_array.shape == var_array.shape:
                var_array = np.where(Mask_array <= 0, var_array, np.nan)
            else:
                print("Mask dimensions " + str(Mask_array.shape) +
                      " are different than in the requested field " +
                      str(var_array.shape) + " - ignoring mask")
        if y_range is not None:
            self.axes[subplot_index].set_ylim(y_range)
        if x_range is not None:
            self.axes[subplot_index].set_xlim(x_range)

        if log_plot is True:
            mesh = self.axes[subplot_index].pcolormesh(x, y, var_array, norm=colors.LogNorm(), **kwargs)
        else:
            mesh = self.axes[subplot_index].pcolormesh(x, y, var_array, **kwargs)

        if title is None:
            self.axes[subplot_index].set_title(self.model.model_name + ' ' +
                                               np.datetime_as_string(self.model.ds[x_variable][0].values))
        else:
            self.axes[subplot_index].set_title(title)

        if pressure_coords:
            self.axes[subplot_index].invert_yaxis()
        self.axes[subplot_index].set_xlabel(x_label)
        self.axes[subplot_index].set_ylabel(y_label)
        if colorbar:
            cbar = plt.colorbar(mesh, ax=self.axes[subplot_index])
            cbar.set_label(cbar_label)
        return self.axes[subplot_index], cbar

    def plot_instrument_timeseries(self, instrument, variable, title=None,
                                   subplot_index=(0, ), colorbar=True, cbar_label=None,
                                   log_plot=False, Mask_array=None, x_range=None, y_range=None,
                                   **kwargs):
        """
        Plots timeseries of a given instrument variable.

        Parameters
        ---------
        instrument: :py:mod:`emc2.core.Instrument`
            The Instrument class that you wish to plot.
        variable: str
            The variable to plot.
        title: str or None
            The title of the plot. Set to None to have EMC^2 generate a title for you.
        subplot_index: tuple
            The index of the subplot to make the plot in.
        colorbar: bool
            If true, plot the colorbar.
        cbar_label: None or str
            The colorbar label. Set to None to provide a default label.
        log_plot: bool
            Set to true to plot variable in logarithmic space.
        Mask_array: bool, int, or float (same dims as "variable")
            Set to true or to other values greater than 0 in grid cells to make them transparent.
        x_range: tuple, list, or None
            The x range of the plot (also accepts datetime64 format).
        y_range: tuple, list, or None
            The y range of the plot.
        Additional keyword arguments are passed into matplotlib's matplotlib.pyplot.pcolormesh.

        Returns
        -------
        axes: Matplotlib axes handle
            The matplotlib axes handle of the plot.
        cbar: Matplotlib axes handle
            The matplotlib colorbar handle of the plot.
        """
        my_ds = instrument.ds
        x_variable = "time"
        if 'range' in my_ds.keys():
            y_variable = "range"
        elif 'altitude' in my_ds.keys():
            y_variable = "altitude"
        elif 'height' in my_ds.keys():
            y_variable = "height"

        x_label = 'Time [UTC]'
        if "long_name" in my_ds[y_variable].attrs and "units" in my_ds[y_variable].attrs:
            y_label = '%s [%s]' % (my_ds[y_variable].attrs["long_name"],
                                   my_ds[y_variable].attrs["units"])
        else:
            y_label = y_variable

        if cbar_label is None:
            cbar_label = '%s [%s]' % (my_ds[variable].attrs["long_name"], my_ds[variable].attrs["units"])

        x = my_ds[x_variable].values
        y = my_ds[y_variable].values
        x, y = np.meshgrid(x, y)
        var_array = my_ds[variable].values.T
        if Mask_array is not None:
            Mask_array = Mask_array.T
            if Mask_array.shape == var_array.shape:
                var_array = np.where(Mask_array <= 0, var_array, np.nan)
            else:
                print("Mask dimensions " + str(Mask_array.shape) +
                      " are different than in the requested field " +
                      str(var_array.shape) + " - ignoring mask")
        if y_range is not None:
            self.axes[subplot_index].set_ylim(y_range)
        if x_range is not None:
            self.axes[subplot_index].set_xlim(x_range)

        if log_plot is True:
            mesh = self.axes[subplot_index].pcolormesh(x, y, var_array, norm=colors.LogNorm(), **kwargs)
        else:
            mesh = self.axes[subplot_index].pcolormesh(x, y, var_array, **kwargs)
        if title is None:
            self.axes[subplot_index].set_title(instrument.instrument_str + ' ' +
                                               np.datetime_as_string(my_ds.time[0].values))
        else:
            self.axes[subplot_index].set_title(title)

        self.axes[subplot_index].set_xlabel(x_label)
        self.axes[subplot_index].set_ylabel(y_label)
        if colorbar:
            cbar = plt.colorbar(mesh, ax=self.axes[subplot_index])
            cbar.set_label(cbar_label)
        return self.axes[subplot_index], cbar

    def plot_single_profile(self, variable, time, pressure_coords=True, title=None,
                            subplot_index=(0,), colorbar=True, cbar_label=None,
                            log_plot=False, Mask_array=None, x_range=None, y_range=None, **kwargs):
        """
        Plots the single profile of subcolumns for a given time period.

        Parameters
        ----------
        variable: str
            The subcolumn variable to plot.
        time: tuple of Datetime or str
            The time step to plot. If a string, specify in the format '%Y-%m-%dT%H:%M:%S'
        pressure_coords: bool
            Set to true to plot in pressure coordinates, false to height coordinates.
        title: str or None
            The title of the plot. Set to None to have EMC^2 generate a title for you.
        subplot_index: tuple
            The index of the subplot to make the plot in.
        colorbar: bool
            If true, then plot the colorbar.
        cbar_label: None or str
            The colorbar label. Set to None to provide a default label.
        log_plot: bool
            Set to true to plot variable in logarithmic space.
        Mask_array: bool, int, or float (same dims as "variable")
            Set to true or to other values greater than 0 in grid cells to make them transparent.
        x_range: tuple, list, or None
            The x range of the plot (also accepts datetime64 format).
        y_range: tuple, list, or None
            The y range of the plot.
        Additional keyword arguments are passed into matplotlib's matplotlib.pyplot.pcolormesh.

        Returns
        -------
        axes: Matplotlib axes handle
            The matplotlib axes handle of the plot.
        cbar: Matplotlib axes handle
            The matplotlib colorbar handle of the plot.
        """
        ds_name = [x for x in self._arm.keys()][0]
        my_ds = self._arm[ds_name].sel({self.model.time_dim: time}, method='nearest')

        if pressure_coords:
            y_variable = self.model.height_dim
        else:
            y_variable = self.model.z_field

        x_label = 'Subcolumn #'
        if "long_name" in my_ds[y_variable].attrs and "units" in my_ds[y_variable].attrs:
            y_label = '%s [%s]' % (my_ds[y_variable].attrs["long_name"],
                                   my_ds[y_variable].attrs["units"])
        else:
            y_label = y_variable

        if cbar_label is None:
            variables = ['Ze', 'Vd', 'sigma_d', 'od', 'beta', 'alpha']
            hyd_met = ''
            hyd_types = ['cl', 'ci', 'pl', 'pi', 'tot']
            for hyd in hyd_types:
                if hyd in variable:
                    hyd_met = hyd

            for var in variables:
                if var in variable:
                    if var == 'Ze':
                        cbar_label = '$Z_{e, %s}$ [dBZ]' % hyd_met
                    elif var == 'Vd':
                        cbar_label = '$V_{d, %s}$ [m/s]' % hyd_met
                    elif var == 'sigma_d':
                        cbar_label = '$\sigma_{d, %s}$ [m/s]' % hyd_met
                    elif var == 'od':
                        cbar_label = '$\tau_{%s}$' % hyd_met
                    elif var == 'beta':
                        cbar_label = '$\beta_{%s}$ [$m^{-2}$]' % hyd_met
                    elif var == 'alpha':
                        cbar_label = '$\alpha_{%s}$ [$m^{-2}$]' % hyd_met

        if pressure_coords:
            x = np.arange(0, self.model.num_subcolumns, 1)
            y = my_ds[y_variable].values
            x, y = np.meshgrid(x, y)
        else:
            x = np.arange(0, self.model.num_subcolumns, 1)
            y = my_ds[y_variable].values.T
            p = my_ds[self.model.height_dim].values
            x, p = np.meshgrid(x, p)

        var_array = my_ds[variable].values.T
        if Mask_array is not None:
            Mask_array = Mask_array.T
            if Mask_array.shape == var_array.shape:
                var_array = np.where(Mask_array <= 0, var_array, np.nan)
            else:
                print("Mask dimensions " + str(Mask_array.shape) +
                      " are different than in the requested field " +
                      str(var_array.shape) + " - ignoring mask")
        if y_range is not None:
            self.axes[subplot_index].set_ylim(y_range)
        if x_range is not None:
            self.axes[subplot_index].set_xlim(x_range)
        if log_plot is True:
            mesh = self.axes[subplot_index].pcolormesh(x, y, var_array, norm=colors.LogNorm(), **kwargs)
        else:
            mesh = self.axes[subplot_index].pcolormesh(x, y, var_array, **kwargs)
        if title is None:
            time_title = ""
            if isinstance(time, str):
                time_title = time
            elif isinstance(time, np.datetime64):
                time_title = np.datetime_as_string(time)

            self.axes[subplot_index].set_title(self.model.model_name + ' ' +
                                               time_title)
        else:
            self.axes[subplot_index].set_title(title)

        if pressure_coords:
            self.axes[subplot_index].invert_yaxis()

        self.axes[subplot_index].set_xlabel(x_label)
        self.axes[subplot_index].set_ylabel(y_label)
        if colorbar:
            cbar = plt.colorbar(mesh, ax=self.axes[subplot_index])
            cbar.set_label(cbar_label)

        return self.axes[subplot_index], cbar

    def plot_subcolumn_mean_profile(self, variable, time, pressure_coords=True, title=None,
                                    subplot_index=(0,), log_plot=False, plot_SD=True, Xlabel=None,
                                    Mask_array=None, x_range=None, y_range=None, **kwargs):
        """
        This function will plot a mean vertical profile of a subcolumn variable for a given time period. The
        thick line will represent the mean profile along the subcolumns, and the shading represents one
        standard deviation about the mean.

        Parameters
        ----------
        variable: str
            The name of the variable to plot.
        time: tuple of Datetime or str
            The time period to plot. If a string, specify in the format '%Y-%m-%dT%H:%M:%S'
            If a 2-element array using the values within range.
        pressure_coords: bool
            Set to true to plot in pressure coordinates.
        title: str or None
            Set the title of the plot to this string. Set to None to provide a default title
        subplot_index: tuple
            The index of the subplot to make the plot in.
        log_plot: bool
            Set to true to plot variable in logarithmic space.
        plot_SD: bool
            Set to  True (default) in order to plot a shaded patch for mean +- SD.
        Xlabel: None or str
            X-axis label. Set to None to provide a default label.
        Mask_array: bool, int, or float (same dims as "variable")
            Set to true or to other values greater than 0 in grid cells to exclude them from
            mean and SD calculations.
        x_range: tuple, list, or None
            The x range of the plot.
        y_range: tuple, list, or None
            The y range of the plot.
        kwargs

        Returns
        -------
        axes: Matplotlib axes handle
            The matplotlib axes handle of the plot.

        """

        ds_name = [x for x in self._arm.keys()][0]
        x_variable = self.model.time_dim
        if np.logical_or(type(time) is tuple, type(time) is str):
            time = np.array(time)
        if time.size == 1:
            my_ds = self._arm[ds_name].sel({x_variable: time}, method='nearest')
        else:
            time_ind = np.logical_and(self._arm[ds_name][x_variable] >= time[0],
                                      self._arm[ds_name][x_variable] < time[1])
            my_ds = self._arm[ds_name].isel({x_variable: time_ind})

        if pressure_coords:
            y_variable = my_ds[self.model.p_field]
            y_label = 'Pressure [hPa]'
        else:
            y_variable = my_ds[self.model.z_field]
            y_label = 'Height [m]'
        if my_ds[x_variable].size > 1:
            y_variable = np.nanmean(y_variable, axis=0)

        x_variable = my_ds[variable].values
        x_variable = np.ma.masked_where(~np.isfinite(x_variable), x_variable)
        if Mask_array is not None:
            if Mask_array.shape == x_variable.shape:
                x_variable = np.where(Mask_array <= 0, x_variable, np.nan)
            else:
                print("Mask dimensions " + str(Mask_array.shape) +
                      " are different than in the requested field " +
                      str(x_variable.shape) + " - ignoring mask")

        if 'Ze' in variable:
            # Use SD as a relative error considering the dBZ units
            if time.size == 1:
                x_var = np.nanmean(10**(x_variable / 10), axis=0)
                x_err = np.nanstd(10**(x_variable / 10), ddof=0, axis=0)
            else:
                x_var = np.nanmean(10**(x_variable / 10), axis=(0, 1))
                x_err = np.nanstd(10**(x_variable / 10), ddof=0, axis=(0, 1))
            x_label = ''
            Xscale = 'linear'  # treating dBZ as linear for plotting
            x_fill = np.array(10 * np.log10([x_var - x_err, x_var + x_err]))
            x_fill[0] = np.where(x_var > x_err, x_fill[0], 10 * np.log10(np.finfo(float).eps))
        else:
            if time.size == 1:
                x_var = np.nanmean(x_variable, axis=0)
                x_err = np.nanstd(x_variable, ddof=0, axis=0)
            else:
                x_var = np.nanmean(x_variable, axis=(0, 1))
                x_err = np.nanstd(x_variable, ddof=0, axis=(0, 1))
            x_fill = np.array([x_var - x_err, x_var + x_err])
            if log_plot:
                x_label = 'log '
                Xscale = 'log'
            else:
                x_label = ''
                Xscale = 'linear'
        x_lim = np.array([np.nanmin(x_fill[0]) * 0.95,
                          np.nanmax(x_fill[1] * 1.05)])

        # Choose label based on variable
        hyd_met = ''
        hyd_types = ['cl', 'ci', 'pl', 'pi', 'tot']
        for hyd in hyd_types:
            if hyd in variable:
                hyd_met = hyd

        if Xlabel is None:
            variables = ['Ze', 'Vd', 'sigma_d', 'od', 'beta', 'alpha', 'LDR_strat']

            for var in variables:
                if var in variable:
                    if var == 'Ze':
                        x_label += '$Z_{e, %s}$ [dBZ]' % hyd_met
                    elif var == 'Vd':
                        x_label += '$V_{d, %s}$ [m/s]' % hyd_met
                    elif var == 'sigma_d':
                        x_label += '$\\sigma_{d, %s}$ [m/s]' % hyd_met
                    elif var == 'od':
                        x_label += '$\\tau_{%s}$' % hyd_met
                    elif var == 'beta':
                        x_label += '$\\beta_{%s}$ [$m^{-1} sr^{-1}$]' % hyd_met
                    elif var == 'alpha':
                        x_label += '$\\alpha_{%s}$ [$m^{-1}$]' % hyd_met
                    elif var == 'LDR_strat':
                        x_label += 'LDR'

            if x_label == '' or x_label == 'log ':
                x_label = variable
        else:
            x_label = Xlabel

        if plot_SD is True:
            self.axes[subplot_index].fill_betweenx(y_variable, x_fill[0], x_fill[1],
                                                   **kwargs)
        if 'alpha' in kwargs.keys():
            kwargs['alpha'] = 1
        if 'Ze' in variable:
            self.axes[subplot_index].plot(10 * np.log10(x_var), y_variable, **kwargs)
        else:
            self.axes[subplot_index].plot(x_var, y_variable, **kwargs)

        if title is None:
            self.axes[subplot_index].set_title(time)
        else:
            self.axes[subplot_index].set_title(title)

        self.axes[subplot_index].set_xlabel(x_label)
        self.axes[subplot_index].set_ylabel(y_label)
        if pressure_coords:
            self.axes[subplot_index].invert_yaxis()
        self.axes[subplot_index].set_xscale(Xscale)
        if y_range is not None:
            self.axes[subplot_index].set_ylim(y_range)
        if x_range is not None:
            self.axes[subplot_index].set_xlim(x_range)
        else:
            self.axes[subplot_index].set_xlim(x_lim)

        return self.axes[subplot_index]

    def plot_instrument_mean_profile(self, instrument, variable, time_range=None, pressure_coords=True,
                                     title=None, subplot_index=(0,), log_plot=False, plot_SD=True,
                                     Xlabel=None, Mask_array=None, x_range=None, y_range=None, **kwargs):
        """
        This function will plot a mean vertical profile of an instrument variable averaged over a given
        time period. The thick line will represent the mean profile along the given period, and the
        shading represents one standard deviation about the mean.

        Parameters
        ----------
        instrument: :py:mod:`emc2.core.Instrument`
            The Instrument class that you wish to plot.
        variable: str
            The name of the variable to plot.
        time_range: datetime64 or None
            Two-element array with starting and ending of time range; use the full data range when None.
        pressure_coords: bool
            Set to true to plot in pressure coordinates.
        title: str or None
            Set the title of the plot to this string. Set to None to provide a default title
        subplot_index: tuple
            The index of the subplot to make the plot in.
        log_plot: bool
            Set to true to plot variable in logarithmic space.
        plot_SD: bool
            Set to  True (default) in order to plot a shaded patch for mean +- SD.
        Xlabel: None or str
            X-axis label. Set to None to provide a default label.
        Mask_array: bool, int, or float (same dims as "variable")
            Set to true or to other values greater than 0 in grid cells to exclude them from
            mean and SD calculations.
        x_range: tuple, list, or Non
            The x range of the plot.
        y_range: tuple, list, or None
            The y range of the plot.
        kwargs

        Returns
        -------
        axes: Matplotlib axes handle
            The matplotlib axes handle of the plot.
        """

        my_ds = instrument.ds
        if 'range' in my_ds.keys():
            y_variable = "range"
        elif 'altitude' in my_ds.keys():
            y_variable = "altitude"
        elif 'height' in my_ds.keys():
            y_variable = "height"
        y_variable = my_ds[y_variable]
        y_label = 'Height [m]'

        if time_range is None:
            x_variable = my_ds[variable].values
        else:
            time_ind = np.logical_and(my_ds.time >= time_range[0], my_ds.time < time_range[1])
            x_variable = my_ds[variable].isel(time=time_ind)
        x_variable = np.ma.masked_where(~np.isfinite(x_variable), x_variable)
        if Mask_array is not None:
            if Mask_array.shape == x_variable.shape:
                x_variable = np.where(Mask_array <= 0, x_variable, np.nan)
            else:
                print("Mask dimensions " + str(Mask_array.shape) +
                      " are different than in the requested field " +
                      str(x_variable.shape) + " - ignoring mask")

        if 'Ze' in variable:
            # Use SD as a relative error considering the dBZ units
            x_var = np.nanmean(10**(x_variable / 10), axis=0)
            x_err = np.nanstd(10**(x_variable / 10), ddof=0, axis=0)
            x_label = ''
            Xscale = 'linear'  # treating dBZ as linear for plotting
            x_fill = np.array(10 * np.log10([x_var - x_err, x_var + x_err]))
            x_fill[0] = np.where(x_var > x_err, x_fill[0], 10 * np.log10(np.finfo(float).eps))
        else:
            x_var = np.nanmean(x_variable, axis=0)
            x_err = np.nanstd(x_variable, ddof=0, axis=0)
            x_fill = np.array([x_var - x_err, x_var + x_err])
            if log_plot:
                x_label = 'log '
                Xscale = 'log'
            else:
                x_label = ''
                Xscale = 'linear'
        x_lim = np.array([np.nanmin(x_fill[0]) * 0.95,
                          np.nanmax(x_fill[1] * 1.05)])

        # Choose label based on variable
        hyd_met = ''
        hyd_types = ['cl', 'ci', 'pl', 'pi', 'tot']
        for hyd in hyd_types:
            if hyd in variable:
                hyd_met = hyd

        if Xlabel is None:
            variables = ['Ze', 'Vd', 'sigma_d', 'od', 'beta', 'alpha', 'LDR_strat']

            for var in variables:
                if var in variable:
                    if var == 'Ze':
                        x_label += '$Z_{e, %s}$ [dBZ]' % hyd_met
                    elif var == 'Vd':
                        x_label += '$V_{d, %s}$ [m/s]' % hyd_met
                    elif var == 'sigma_d':
                        x_label += '$\\sigma_{d, %s}$ [m/s]' % hyd_met
                    elif var == 'od':
                        x_label += '$\\tau_{%s}$' % hyd_met
                    elif var == 'beta':
                        x_label += '$\\beta_{%s}$ [$m^{-1} sr^{-1}$]' % hyd_met
                    elif var == 'alpha':
                        x_label += '$\\alpha_{%s}$ [$m^{-1}$]' % hyd_met
                    elif var == 'LDR_strat':
                        x_label += 'LDR'

            if x_label == '' or x_label == 'log ':
                x_label = variable
        else:
            x_label = Xlabel

        if plot_SD is True:
            self.axes[subplot_index].fill_betweenx(y_variable, x_fill[0], x_fill[1],
                                                   **kwargs)
        if 'alpha' in kwargs.keys():
            kwargs['alpha'] = 1
        if 'Ze' in variable:
            self.axes[subplot_index].plot(10 * np.log10(x_var), y_variable, **kwargs)
        else:
            self.axes[subplot_index].plot(x_var, y_variable, **kwargs)

        if title is None:
            self.axes[subplot_index].set_title('%s' % time_range)
        else:
            self.axes[subplot_index].set_title(title)

        self.axes[subplot_index].set_xlabel(x_label)
        self.axes[subplot_index].set_ylabel(y_label)
        if pressure_coords:
            self.axes[subplot_index].invert_yaxis()
        self.axes[subplot_index].set_xscale(Xscale)
        if y_range is not None:
            self.axes[subplot_index].set_ylim(y_range)
        if x_range is not None:
            self.axes[subplot_index].set_xlim(x_range)
        else:
            self.axes[subplot_index].set_xlim(x_lim)

        return self.axes[subplot_index]
