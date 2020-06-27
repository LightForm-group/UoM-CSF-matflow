## Running the example workflows

You can run any of the example workflows by calling `matflow go /path/to/profile.yml`. The worflow profile file does not need to be in the current working directory.

For example, you could generate a new directory in your home area for testing and run the demo RVE extrusion workflow which uses DefDAP:

1. `mkdir ~/matflow-workflows`
2. `cd ~/matflow-workflows`
3. `matflow go /mnt/eps-01/jf01/shared/matflow/workflows/DefDAP/RVE_extrusion.yml`

> Note that in general we should not run computationally- or storage-expensive simulations in our home areas (`~/.`).
