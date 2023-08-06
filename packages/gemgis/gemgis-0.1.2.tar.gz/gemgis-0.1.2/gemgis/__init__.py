"""Top-level package for GemGIS."""

__title__ = 'GeoPyGeographic - GemGIS: Geographic information processing for geomodeling'

__abstract__ = 'GemGIS is a Python-based, open-source geographic information processing library.\n' \
               'It is capable of preprocessing spatial data such as vector data (shape files, geojson files, \n' \
               'geopackages), \n'\
               'raster data, data obtained from WMS services or XML/KML files. \n' \
               'Preprocessed data can be stored in a dedicated Data Class to be passed to the geomodeling package GemPy \n' \
               'in order to accelerate to model building process. \n'

__authors__ = """Alexander Jüstel, Arthur Endlein Correia, Florian Wellmann"""

__correspondence_email__ = 'alexander.juestel@rwth-aachen.de'

__affiliations__ = 'CGRE - RWTH Aachen University'

__version_date__ = '05.10.2020'

__version__ = '0.1.2'

__changelog__ = 'What is new in version 0.1.2: \n' \
                '- Minor changes to API - additional attributes for GemPy Data Class  \n' \
                '- Added plotting function for input data \n' \
                '- Reworking all tutorials and examples for new API\n' \
                '- Adding Tutorial 9 and 10\n' \
                '- Adding Docstrings, documentation and tests for existing and new methods \n' \
                '- Adding misc methods and notebooks for specialized tasks \n' \
                '- Bug fixes on existing functions'

__previous_versions__ = '0.1.1'

__changelog_previous_version__ =  'What is new in version 0.1.1: \n' \
                '- Introducing a GemPyData class to store objects like interfaces df, extent, resolution, etc. \n' \
                '- Extracting XY Coordinates from vector data (lines, points of shape files, geojsons and gpkg) \n' \
                '- Interpolate rasters from contour lines \n'\
                '- Extracting Z values from interpolated rasters and .tif-files \n' \
                '- Creating GemPy section_dicts from Point and Line Shape Files \n' \
                '- Calculating slope and aspect of rasters including sampling orientations from rasters \n' \
                '- Sampling interfaces from rasters \n' \
                '- Clipping vector and raster data by extents and shapes \n' \
                '- Rescaling and saving rasters as georeferenced .tif-files\n' \
                '- Wrapper functions to plot spatial data in PyVista \n' \
                '- Extracting data from WMS Services \n'\
                '- Plotting of stereonets for orientation data using mplstereonet \n'\
                '- Parsing of QGIS Style Files (.qml) to create colors lists for plotting and surface_color_dicts\n'\
                '- Calculating orientations based on strike lines for layers and faults \n'\
                '- Export of GemPy geological map as vector data \n'\
                '- Added extensive testing for all functions and methods \n'\
                '- Detailed tutorials and examples to demonstrate functionality of GemGIS \n'

from gemgis.gemgis import *
import gemgis.vector as vector
import gemgis.raster as raster
import gemgis.utils as utils
import gemgis.visualization as visualization
import gemgis.wms as wms
import gemgis.postprocessing as post
import gemgis.misc as misc
