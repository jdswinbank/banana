import numpy
import aplpy
from matplotlib import pyplot
from banana.mongo import get_hdu
from banana.convert import deg_to_asec


def image_plot(pyfits_hdu, size=5, sources=[]):
    """
    :param pyfits_hdu: a pyfits file object
    :size: size in inches
    :sources: a list of Extractedsource ORM models

    :returns: a matplotlib canvas which can be used to write the image to
              something (like a django HTTP resonse)
    """
    fig = pyplot.figure(figsize=(size, size))
    plot = aplpy.FITSFigure(pyfits_hdu, figure=fig, subplot=[0, 0, 1, 1],
                            auto_refresh=False)
    plot.show_grayscale()
    plot.axis_labels.hide()
    plot.tick_labels.hide()
    plot.ticks.hide()

    if sources:
       ra = [source.ra for source in sources]
       dec = [source.decl for source in sources]
       semimajor = [source.semimajor / 900 for source in sources]
       semiminor = [source.semiminor / 900 for source in sources]
       pa = [source.pa + 90 for source in sources]
       plot.show_ellipses(ra, dec, semimajor, semiminor, pa, facecolor='none',
                          edgecolor='yellow', linewidth=1)
    return fig.canvas


def scatter_plot(extractedsources, size=5):
    """Plot positions of all counterparts for all (unique) sources for
    the given dataset.

    The positions of all (unique) sources in the running catalog are
    at the centre, whereas the positions of all their associated
    sources are scattered around the central point.  Axes are in
    arcsec relative to the running catalog position.
    """
    figure = pyplot.figure(figsize=(size, size))

    # no list comprehension here since we use raw query
    ra_dist_arcsec= []
    decl_dist_arcsec = []
    ra_err = []
    decl_err = []
    for source in extractedsources:
        ra_dist_arcsec.append(source.ra_dist_arcsec)
        decl_dist_arcsec.append(source.decl_dist_arcsec)
        ra_err.append(deg_to_asec(source.ra_err) / 2)
        decl_err.append(deg_to_asec(source.decl_err) / 2)

    axes = figure.add_subplot(1, 1, 1)
    axes.errorbar(ra_dist_arcsec, decl_dist_arcsec, xerr=ra_err, yerr=decl_err,
                  fmt='+', color='b', label="xtr")
    axes.set_xlabel(r'RA (arcsec)')
    axes.set_ylabel(r'DEC (arcsec)')
    if len(ra_dist_arcsec):
        lim = 1 + max(int(numpy.trunc(max(abs(min(ra_dist_arcsec)),
                                          abs(max(ra_dist_arcsec))))),
                      int(numpy.trunc(max(abs(min(decl_dist_arcsec)),
                                          abs(max(decl_dist_arcsec))))))
    else:
        lim = 1
    axes.set_xlim(xmin=-lim, xmax=lim)
    axes.set_ylim(ymin=-lim, ymax=lim)
    axes.grid(False)
    # Shifts plot spacing to ensure that axes labels are displayed
    figure.tight_layout()
    return figure.canvas


def extracted_sources_pixels(image, size):
    """
    :param image: a banana.models.Image object
    :returns: a list of sources of an image
    """
    hdu = get_hdu(image.url)
    if not hdu:
        return None

    # make an image
    fig = pyplot.figure(figsize=(size, size))
    plot = aplpy.FITSFigure(hdu, figure=fig, subplot=[0, 0, 1, 1],
                            auto_refresh=False)

    # get source info from database
    sources = image.extractedsources.all()
    ids = [source.id for source in sources]
    x_world = numpy.array([source.ra for source in sources])
    y_world = numpy.array([source.decl for source in sources])
    w_world = numpy.array([source.semimajor / 900 for source in sources])
    h_world = numpy.array([source.semiminor / 900 for source in sources])

    # first convert positions to matplotlib image coordinates
    x_plot, y_plot = plot.world2pixel(x_world, y_world)
    arcperpix = aplpy.wcs_util.arcperpix(plot._wcs)
    w_plot = 3600.0 * w_world / arcperpix
    h_plot = 3600.0 * h_world / arcperpix

    # then transform them to true pixel coordinates
    ax = fig.axes[0]
    xy_pixels = ax.transData.transform(numpy.vstack([x_plot, y_plot]).T)
    x_px, y_px = xy_pixels.T

    # In matplotlib, 0,0 is the lower left corner, whereas it's usually the
    # upper right for most image software, so we'll flip the y-coords
    fig_width, fig_height = fig.canvas.get_width_height()
    y_px = fig_height - y_px

    # because of an unknown reason we need to scale the coordinates with 25%
    y_px *= 1.25
    x_px *= 1.25

    # create average size since areamap can only draw circles
    size_px = (w_plot + h_plot) / 4
    return zip(ids, list(x_px), list(y_px), list(size_px))


def extractedsource(hdu, source, size=1):
    fig = pyplot.figure(figsize=(size, size))
    fits = aplpy.FITSFigure(hdu, figure=fig, subplot=[0, 0, 1, 1],
                            auto_refresh=False)
    #fits.show_grayscale()
    fits.show_colorscale()
    fits.axis_labels.hide()
    fits.tick_labels.hide()
    fits.ticks.hide()
    fits.recenter(source.ra, source.decl, width=source.semimajor / 90,
                  height=source.semiminor / 90)
    return fig.canvas
