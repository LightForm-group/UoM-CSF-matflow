This repository contains information about running MatFlow on the [Computational Shared Facility](http://ri.itservices.manchester.ac.uk/csf3/) (CSF) at the University of Manchester.

Included are:
- A [software definition file](https://github.com/LightForm-group/UoM-CSF-matflow/blob/master/software.yml)
- A set of [example task schemas](https://github.com/LightForm-group/UoM-CSF-matflow/blob/master/task_schemas.yml)
- Some [example workflows](https://github.com/LightForm-group/UoM-CSF-matflow/tree/master/workflows)

## Installation of MatFlow on the CSF

1. To allow access to the internet so we can install [MatFlow](https://github.com/LightForm-group/matflow), first load the [proxy module](http://ri.itservices.manchester.ac.uk/csf3/software/tools/proxy/): `module load tools/env/proxy2`. We only need to do this once, when installing Python packages from the web. However, if you want to use MatFlow's cloud archiving facility (i.e. copying your workflow results to Dropbox), you will need to make sure the proxy module is always loaded. You can do this by adding the module load line to a file `.modules` in your home directory.
2. Now install MatFlow and some extensions, using `pip`: 
    
    `pip install --user matflow matflow-damask matflow-formable matflow-mtex`

3. Run `matflow validate` to check the installation (you may get an warning about the MTEX extension - this is fine)

4. Add the `software.yml` and `task_schemas.yml` files from this repository to your MatFlow software sources and task schemas sources respectively. These files are already in the `jf01` group shared RDS space under the path `/mnt/eps01-rds/jf01-home01/shared/matflow`. To register them with MatFlow, edit the MatFlow `config.yml` file, which, after running `matflow validate` for the first time), resides here: `~/.matflow/config.yml` (i.e. in your home directory). Add the following path to the `task_schema_sources` list in the config file:

    `/mnt/eps01-rds/jf01-home01/shared/matflow/task_schemas.yml`

    ...and add the following path to the `software_sources` list in the config file:

    `/mnt/eps01-rds/jf01-home01/shared/matflow/software.yml`
    
5. Now run `matflow validate` again. This time there should be no warnings.

## Setting up Dropbox archiving

We can get MatFlow to copy (a subset) of the workflow files to a Dropbox account after the workflow completes. 

1. Firstly, you'll need to generate a Dropbox access token by creating an "app" here: https://www.dropbox.com/developers/apps
2. Then you can add this token to the MatFlow configuration file (in `~/.matflow.config.yml') as a new key called `dropbox_token`.
3. Finally, you need to add one or more "archive locations" to the MatFlow config file. An archive location looks like this:

    ```yaml
    archive_locations:
      dropbox:
        cloud_provider: dropbox
        path: /sims
    ```
    In this case, this tells Matflow to use the path `/sims` inside your dropbox directory structure.
4. You can then add a extra key to any of your workflows to tell MatFlow to use this archive location: `archive: dropbox`. If you want to exclude certain files, you can also add a key `archive_excludes` to your workflow, which is a list of glob-style patterns to exclude.

