.. CHAMP documentation master file, created by
   sphinx-quickstart on Tue Jul 11 15:50:43 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

CHAMP (Convex Hull of Admissible Modularity Partitions
=================================================================
A modularity based tool for screening a set of partitions.

.. figure::  docs/sub_docs/images/graphs_all_three.png
   :align:   center
   :figwidth: 95%

The CHAMP python package provides two levels of functionality:

* Identifying the subset of partitions from a group of partitions (regardless of how they were discovered) with optimal modularity. See `Running <docs/sub_docs/running.rst>`_.
* Parallelized implementation of modularity based community detection method, `louvain <https://github.com/vtraag/louvain-igraph>`_ with efficient filtering (*ala* CHAMP), management, and storage of the generated partitions. See `Louvain Parallel Extension <docs/sub_docs/louvain_ext.rst>`_ .

For complete documentation, please visit our ReadTheDocs page: \
 `http://champ.readthedocs.io/en/latest/ <http://champ.readthedocs.io/en/latest/>`_



Download and Installation:
____________________________

The CHAMP module is hosted on `PyPi <https://pypi.python.org/pypi/champ>`_.  The easiest way to install is \
via the pip command::

    pip install champ


For installation from source, the latest version of champ can be downloaded from GitHub\:

    `<https://github.com/wweir827/CHAMP>`_

For basic installation:

.. code-block:: bash

    python setup.py install

Dependencies
***************

Most of the dependencies for CHAMP are fairly standard tools for data analysis in Python, with the exception of
`louvain_igraph <https://github.com/vtraag/louvain-igraph>`_.   They include :

+ `NumPy <https://www.scipy.org/scipylib/download.html>`_ \: Python numerical analysis library.
+ `sklearn <http://scikit-learn.org/stable/install.html>`_ \:Machine learning tools for python.
+ `python-igraph <http://igraph.org/python/#downloads>`_ \:igraph python version for manipulation of networks.
+ `matplotlib <https://matplotlib.org/users/installing.html>`_ \:Python data visualization library.
+ `louvain <https://github.com/vtraag/louvain-igraph>`_ \:Vincent Traag's implementation of louvain algorithm.
+ `h5py <https://pypi.python.org/pypi/h5py>`_ \: HDF5 file format library for python.

These should all be handled automatically if using pip to install.

Citation
___________
Please cite\:

| 1.  William H. Weir, Scott Emmons, Ryan Gibson, Dane Taylor, and Peter J. Mucha. Post-processing partitions to identify domains of modularity optimization. Algorithms, 2017. URL: http://www.mdpi.com/1999-4893/10/3/93, doi:10.3390/a10030093.
|
| 2.  William H. Weir, Ryan Gibson, and Peter J Mucha. Champ package: Convex Hull of Admissible Modularity Partitions in python and matlab. 2017. https://github.com/wweir827/CHAMP.
|

`bibtex <docs/sub_docs/champ.bib>`_

For more details and results see our `preprint <https://arxiv.org/abs/1706.03675>`_


Acknowledgements
_________________

This project was supported by the James S. McDonnell Foundation 21st Century Science Initiative -\
Complex Systems Scholar Award grant #220020315, by the National Institutes of Health through Award \
Numbers R01HD075712, R56DK111930 and T32GM067553, and by the CDC Prevention Epicenter Program. The \
content is solely the responsibility of the authors and does not necessarily represent the official \
views of the funding agencies.