Installation
============

There are three different ways to install UROPA. We recommend to install UROPA using the conda package manager.

Conda package manager
---------------------
Make sure to have `conda` installed, e.g. via

- `Miniconda`_
	- download the Miniconda installer for **Python 3**
	- run ``bash Miniconda3-latest-Linux-x86_64.sh`` to install Miniconda
	- Answer the question "Do you wish the installer to prepend the Miniconda install location to PATH in your /home/.../.bashrc ?" with yes
		OR do ``export PATH=dir/to/miniconda3:$PATH`` after installation process

The UROPA installation is now as easy as 

``conda create --name uropa``

``conda activate uropa``

``conda install python uropa``.

Biocontainers / Docker
----------------------

If you have a running `Docker`_ environment, you can pull a biocontainer with UROPA and all dependencies via

- ``docker pull quay.io/biocontainers/uropa:latest_tag`` using the latest tag from the `taglist`_, e.g. ``1.2.1--py27r3.3.2_0``
- ``docker pull loosolab/uropa``

Installation from source
------------------------

You can also install UROPA from the source PyPI package. Note that this comes without the R dependencies for auxillary scripts:

``pip install uropa``

To fulfill all other dependencies, `R/Rscript`_, v3.3.0 or higher (follow the instructions on url) is needed. 
Futhermore, follow the subsequent instructions within R environment to install mandatory packages:

	- ``install.packages(c("ggplot2","devtools","gplots","gridExtra","jsonlite", "VennDiagram","snow","getopt","tidyr","UpSetR"))``
	- ``source("https://bioconductor.org/biocLite.R")``
	- ``biocLite(c("RBGL","graph"))``
	- further package infos can be found at `CRAN`_ and `Bioconductor`_
	- In order to visualize the Chow-Ruskey plot with uropa_summary.R, install the modified Vennerable package from our fork:
		- ``library(devtools)``
		- ``install_github("jenzopr/Vennerable")``


.. _Miniconda: https://conda.io/miniconda.html
.. _Docker: http://www.docker.com
.. _taglist: https://quay.io/repository/biocontainers/uropa?tab=tags
.. _R/Rscript: http://www.r-project.org/
.. _CRAN: https://cran.r-project.org/web/packages/
.. _Bioconductor: http://bioconductor.org/
