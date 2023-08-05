=====
SICOR
=====
.. image:: http://enmap.gitext.gfz-potsdam.de/sicor/doc/_images/sicor_logo_lr.png
   :width: 300px
   :alt: SICOR Logo

Sensor Independent Atmospheric Correction of optical Earth Observation (EO) data from both multispectral and
hyperspectral instruments. Currently, SICOR can be applied to Sentinel-2 and EnMAP data but the implementation of
additional space- and airborne sensors is under development. As a unique feature for the processing of hyperspectral
data, SICOR incorporates a three phases of water retrieval based on Optimal Estimation (OE) including the calculation of
retrieval uncertainties. The atmospheric modeling in case of hyperspectral data is based on the MODTRAN radiative
transfer code whereas the atmospheric correction of multispectral data relies on the MOMO code. The MODTRAN trademark is
being used with the express permission of the owner, Spectral Sciences, Inc. Please check the documentation_ for usage,
examples and in depth information.

Get It
------


SICOR depends on some open source packages which are usually installed without problems by the automatic install
routine. However, for some projects, we strongly recommend resolving the dependency before the automatic installer
is run. This approach avoids problems with conflicting versions of the same software.
Using conda_, the recommended approach is:

 .. code-block:: bash

    # create virtual environment for sicor, this is optional
    conda create -y -q -c conda-forge --name sicor python=3
    source activate sicor
    conda config --add channels conda-forge
    conda install --yes -q gdal numpy scikit-image matplotlib pyproj rasterio shapely geopandas pyresample pytables h5py llvmlite pyfftw scikit-learn numba

Install SICOR via pip (recommended). This may take a while since some needed tables are downloaded:

  .. code-block:: bash

    pip install sicor

Alternatively you can install SICOR by cloning the following repository:

 .. code-block:: bash

    git clone https://gitext.gfz-potsdam.de/EnMAP/sicor.git
    cd sicor
    python setup.py install

In case you installed SICOR from Git you need to install Git Large File Storage (git-lfs_) to download some additional
LFS files from the repository. You can install Git LFS on your MacOS/Linux computer using a package manager such as
Homebrew or MacPorts:

 .. code-block:: bash

    brew install git-lfs
    git lfs install

After installation, some needed LFS files have to be downloaded:

 .. code-block:: bash

    git lfs pull

If you installed SICOR from Git and like to run it in multispectral mode for Sentinel-2, several additional tables have
to be downloaded (using pip, these tables are downloaded automatically). In this case, you also need to install the
ECMWF API client:

 .. code-block:: bash

    pip install ecmwf-api-client
    make download-tables


SICOR repository operations can be started using make, available options are:

 .. code-block:: console

    $ make

    make options: (run make [option] to perform action):

    clean:
        Remove all build, test, coverage and Python artifacts.

    clean-build:
        Remove build artifacts including build/ dist/ and .eggs/ folders.

    clean-pyc:
        Remove Python file artifacts, e.g. pyc files.

    clean-test:
        Remove test and coverage artifacts.

    convert_examples_to_doc:
        Use nbconvert to convert jupyter notebooks in examples to doc/examples.
        Links to internal images are adjusted such that SPHINX documentation
        can be build.

    coverage:
        Use coverage to run tests and to produce a coverage report.

    coverage_view:
        Open default browser to check coverage report.

    docs:
        Generate HTML documentation using SPHINX. If example jupyer notebooks
        should be updated, run the target 'convert_examples_to_doc'
        first.

    download-tables (currently, only needed for multispectral case):
        Download tables for atmospheric correction and scene classification
        from google drive if not found locally (anywhere in $PATH). Gdrive
        might be unreliable and fail. Just try again later. Files are
        checked for their hash before continuing here.

    download-tables-all (currently, only needed for multispectral case):
        Download ALL tables for atmospheric correction and scene classification.

    examples_notebooks:
        Start a jupyter notebook server in the examples directory and
        open browser.

    gitlab_CI_docker:
        Build a docker image for CI use within gitlab. This is based
        on docker and required sudo access to docker. Multiple images
        are build, the 'sicor:latest' includes a working environment
        for SICOR and is used to run the tests. SICOR is not included
        in this image and it is cloned and installed for each test run.

    install:
        Install the package to the active Python site-packages.

    lint:
        Check style and pep8 conformity using multiple pep8 and style
        checkers. Flake8 and pycodestyle need to complete without error
        to not fail here. For now, pylint and pydocstyle are included,
        but their results are ignored. The target 'test' depends on 'lint'
        which means that testing can only be a success when linting was
        run without errors. Run this before any commit!

    nose2:
        Run all tests using nose2. Coverage and other plugins are included
        in the ini settings file.

    nose2_debug:
        Run a single test using nose2. This is useful for debugging.
        Change this if needed.

    requirements:
        Install requirements as defined in requirements.txt using pip.

    test:
        Run tests quickly with the default Python interpreter and without
        coverage.

    test_single:
        Run a single test quickly with the default Python interpreter and without
        coverage. This is useful for debugging errors and feel free to
        change the considered test case to your liking.



Quickstart
----------
Usage from python:

 .. code-block:: python

    from sicor import AC
    AC()

 .. code-block:: python

    from sicor.sicor_enmap import sicor_ac_enmap
    enmap_l2a_vnir, enmap_l2a_swir, cwv_model, cwc_model, ice_model, toa_model, se, scem, srem = sicor_ac_enmap(data_l1b, options, logger)

From command line (currently, only applicable to multispectral case):

 .. code-block:: console

    sicor_ecmwf.py --help
    sicor_ac.py --help

Features
--------

* Sentinel-2 L1C to L2A processing
* EnMAP L1B to L2A processing
* generic atmospheric correction for hyperspectral airborne and spaceborne data
* retrieval of the three phases of water from hyperspectral data
* calculation of various retrieval uncertainties
  (including a posteriori errors, averaging kernels, gain matrices, degrees of freedom, information content)
* atmospheric correction for Landsat-8: work in progress
* CH4 retrieval from hyperspectral data: work in progress


.. _coverage: http://enmap.gitext.gfz-potsdam.de/sicor/coverage/
.. _test_report: http://enmap.gitext.gfz-potsdam.de/sicor/coverage/report.html
.. _documentation: http://enmap.gitext.gfz-potsdam.de/sicor/doc/
.. _conda: https://conda.io/docs/
.. _git-lfs: https://git-lfs.github.com/

Credits
--------

This software was developed within the context of the EnMAP project supported by the DLR Space Administration with
funds of the German Federal Ministry of Economic Affairs and Energy (on the basis of a decision by the German
Bundestag: 50 EE 1529) and contributions from DLR, GFZ and OHB System AG. The MODTRAN trademark is being used with the
express permission of the owner, Spectral Sciences, Inc.
