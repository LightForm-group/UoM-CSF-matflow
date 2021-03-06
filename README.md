[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/LightForm-group/UoM-CSF-matflow/HEAD)

This repository contains information about running [MatFlow](https://github.com/LightForm-group/matflow) on the [Computational Shared Facility](http://ri.itservices.manchester.ac.uk/csf3/) (CSF) at the University of Manchester.

Included are:
- A [software definition file](https://github.com/LightForm-group/UoM-CSF-matflow/blob/master/software.yml)
- A set of [example task schemas](https://github.com/LightForm-group/UoM-CSF-matflow/blob/master/task_schemas.yml)
- Some [example workflows](https://github.com/LightForm-group/UoM-CSF-matflow/tree/master/workflows)
- Some [Jupyter notebooks](https://github.com/LightForm-group/UoM-CSF-matflow/tree/master/workflows/jupyter_notebooks) demonstrating use of the MatFlow API on completed workflows. Click the [Binder link above](https://mybinder.org/v2/gh/LightForm-group/UoM-CSF-matflow/HEAD) and navigate to `/workflows/jupyter_notebooks` to explore these.

## Installation of MatFlow on the CSF

1. Add `export HDF5_USE_FILE_LOCKING=FALSE` to your `.bash_profile`. This is to allow MatFlow to work on the scratch filesystem. See [this issue](https://github.com/LightForm-group/UoM-CSF-matflow/issues/3).
2. To allow access to the internet so we can install MatFlow, first load the [proxy module](http://ri.itservices.manchester.ac.uk/csf3/software/tools/proxy/): `module load tools/env/proxy2`. We only need to do this once, when installing Python packages from the web. However, if you want to use MatFlow's cloud archiving facility (i.e. copying your workflow results to Dropbox), you will need to make sure the proxy module is always loaded. You can do this by adding the module load line to a file `.modules` in your home directory.
3. Load [Anaconda](http://ri.itservices.manchester.ac.uk/csf3/software/applications/anaconda-python/) to give us access to `pip`:

    `module load apps/binapps/anaconda3/2019.07`

3. Now install MatFlow and some extensions, using `pip`. This may take several minutes. You may receive a warning about the scripts path not being on your PATH (see next step). 
    
    `pip install --user matflow matflow-damask matflow-formable matflow-mtex matflow-defdap`

4. Make sure the following path is on your `$PATH` environment variable: `~/.local/bin`. This can be done in your `.bash_profile` file like this: `PATH=$PATH:~/.local/bin`.

5. Run `matflow validate` to check the installation (you may get a warning about the MTEX extension - this is fine)

6. Add the `software.yml` and `task_schemas.yml` files from this repository to your MatFlow software sources and task schemas sources respectively. These files are already in the `jf01` group shared RDS space under the path `/mnt/eps01-rds/jf01-home01/shared/matflow`. To register them with MatFlow, edit the MatFlow `config.yml` file, which, after running `matflow validate` for the first time, resides here: `~/.matflow/config.yml` (i.e. in your home directory). Add the following path to the `task_schema_sources` list in the config file:

    `/mnt/eps01-rds/jf01-home01/shared/matflow/task_schemas.yml`

    ...and add the following path to the `software_sources` list in the config file:

    `/mnt/eps01-rds/jf01-home01/shared/matflow/software.yml`
    
7. Now run `matflow validate` again. This time there should be no warnings.

## Setting default scheduler options for preparation/processing jobs

Often, preparation and processing jobs are not computationally expensive, and can be run as serial jobs in the short queue on the CSF. We can set default scheduler options for the preparation and processing jobs by adding this to the MatFlow config file:

```yaml
default_preparation_run_options:
  l: short

default_processing_run_options:
  l: short
  
default_iterate_run_options:
  l: short  
```

In this case, all preparation and processing jobs will use the short queue by default. This can be overidden from within a workflow if necessary.

## Submitting a workflow

Run the command `matflow go workflow.yml` where `workflow.yml` is the name of the workflow file.

## Stopping an active workflow

Run the command `matflow kill workflow/directory/path` where `workflow/directory/path` is the path to the workflow directory that is generated by MatFlow. This command will delete all running and queued jobs associated with the workflow.

## Setting up Dropbox archiving

We can get MatFlow to copy (a subset) of the workflow files to a Dropbox account after the workflow completes. 

1. Add an "archive location" to the MatFlow config file. An archive location looks like this:

    ```yaml
    archive_locations:
      dropbox:
        cloud_provider: dropbox
        path: /sims
    ```
    In this case, this tells MatFlow to use the path `/sims` inside your Dropbox directory structure. The path you specify here must exist.
2. You can then add an extra key to any of your workflow files to tell MatFlow to use this archive location: `archive: dropbox`. If you want to exclude certain files, you can also add a key `archive_excludes` to your workflow, which is a list of glob-style patterns to exclude. Task schemas can also include `archive_exlcudes`.

The first time you submit a workflow that uses this archive location, you will be prompted to authorize hpcflow to connect to your Dropbox account.

