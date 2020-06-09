This repository contains information about running MatFlow on the [Computational Shared Facility](http://ri.itservices.manchester.ac.uk/csf3/) (CSF) at the University of Manchester.

Included are:
- A [software definition file](https://github.com/LightForm-group/UoM-CSF-matflow/blob/master/software.yml)
- A set of [example task schemas](https://github.com/LightForm-group/UoM-CSF-matflow/blob/master/task_schemas.yml)
- Some example workflows

## Installation of MatFlow on the CSF

1. To allow access to the internet so we can install MatFlow, first load the [proxy module](http://ri.itservices.manchester.ac.uk/csf3/software/tools/proxy/): `module load tools/env/proxy2`. We only need to do this once, when installing Python packages from the web. However, if you want to use MatFlow's cloud archiving facility (i.e. copying your workflow results to Dropbox), you will need to make sure the proxy module is always loaded. You can do this by adding the module load line to a file `.modules` in your home directory.
2. Now install MatFlow and some extensions, using `pip`: 
    
    `pip install --user matflow matflow-damask matflow-formable matflow-mtex`

3. Run `matflow validate` to check the installation (you may get an warning about the MTEX extension - this is fine)

4. Add the `software.yml` and `task_schemas.yml` files from this repository to your MatFlow software sources and task schemas sources respectively. These files are already in the `jf01` group shared RDS space under the path `/mnt/eps01-rds/jf01-home01/shared/matflow`. To register them with MatFlow, edit the MatFlow `config.yml` file, which, after running `matflow validate` for the first time), resides here: `~/.matflow/config.yml` (i.e. in your home directory). Add the following path to the `task_schema_sources` list in the config file:

    `mnt/eps01-rds/jf01-home01/shared/matflow/task_schemas.yml`

    ...and add the following path to the `software_sources` list in the config file:

    `mnt/eps01-rds/jf01-home01/shared/matflow/software.yml`.
