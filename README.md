This repository contains information about running MatFlow on the [Computational Shared Facility](http://ri.itservices.manchester.ac.uk/csf3/) (CSF) at the University of Manchester.

Included are:
- A [software definition file](https://github.com/LightForm-group/UoM-CSF-matflow/blob/master/software.yml)
- A set of example task schemas
- Some example workflows

## Installation of MatFlow on the CSF

1. To allow access to the internet so we can install MatFlow, first load the [proxy module](http://ri.itservices.manchester.ac.uk/csf3/software/tools/proxy/): `module load tools/env/proxy2`. We only need to do this once, when installing Python packages from the web. However, if you want to use MatFlow's cloud archiving facility (i.e. copying your workflow results to Dropbox), you will need to make sure the proxy module is always loaded. You can do this by adding the module load line to a file `.modules` in your home directory.
2. Now install MatFlow and some extensions, using `pip`: 
    
    `pip install --user matflow matflow-damask matflow-formable matflow-mtex`
