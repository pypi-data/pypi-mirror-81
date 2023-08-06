============
Installation
============

SICOR depends on some open source packages which are usually installed without problems by the automatic install
routine. However, for some projects, we strongly recommend resolving the dependency before the automatic installer
is run. This approach avoids problems with conflicting versions of the same software.
Using conda_, the recommended approach is:

 .. code-block:: bash

    # create virtual environment for sicor, this is optional
    conda create -y -q -c conda-forge --name sicor python=3
    source activate sicor
    conda config --add channels conda-forge
    conda install --yes -q gdal numpy scikit-image matplotlib pyproj rasterio shapely geopandas pyresample pytables h5py llvmlite pyfftw scikit-learn numba arosics

Install SICOR via pip (recommended):

  .. code-block:: bash

    pip install sicor

Alternatively you can install SICOR by cloning the following repository:

 .. code-block:: bash

    git clone https://gitext.gfz-potsdam.de/EnMAP/sicor.git
    cd sicor
    python setup.py install

If you like to run SICOR in multispectral mode for Sentinel-2, you need to install the ECMWF API client:

 .. code-block:: bash

    pip install ecmwf-api-client


.. _conda: https://conda.io/docs/
.. _git-lfs: https://git-lfs.github.com/
