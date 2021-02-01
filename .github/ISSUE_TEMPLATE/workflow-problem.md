---
name: Workflow problem
about: For general problems with workflows
title: ''
labels: workflow-problem
assignees: ''

---

**Describe the problem**
A clear and concise description of what the problem is.

**Expected behavior**
A clear and concise description of what you expected to happen.

**Output from `matflow validate`**
Please paste here the output from running the command `matflow-validate`.

**Workflow directory and/or profile location**
Please copy the whole workflow directory (that created by `matflow go ...`) into a shareable location on the CSF or Dropbox. Share a link or CSF path to that location here.

E.g. to copy to the shared LightForm RDS space, use this command:

`cp -r /path/to/workflow/directory/ /mnt/eps01-rds/Fonseca-Lightform/shared/matflow-debugging`

If the profile YAML file does not run, please just share the profile file.


**MatFlow and extension package versions**
If your problem is on the CSF, please paste below the output from the following commands on the CSF:

```bash
module load apps/anaconda3/5.2.0/bin
pip list --user | grep "matflow\|damask\|formable"
```

If your problem is on your local computer, please paste below the output from the following command on your local computer:

- For a Mac or Linux computer: `pip list | grep "matflow\|damask\|formable"`
- For a Windows computer: `pip list | findstr "matflow damask formable"`
