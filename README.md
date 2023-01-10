# i18 xrf Notebook

This notebook is used to perform xrf processing of i18 data. This repo follows the bookshelf structure, meaning it will be automatically deployed in three varieties:

1. An interactive - jupyterlab - environment, runnable both locally and hosted on the hosted JupyterLab instance
2. A headless processing image, runnable both locally and as a cluster job
3. A service, which can be hosted on the k8s cluster, and accessed via a REST API

## Releasing a version

Simply "create a release" on github, this will run a set of continious integration (CI) jobs defined in `.github/workflows` to generate the nessacary containers.

To update the versions available via the diamond module system, run the Project General installation jenkins job for the "bookshelf" package;
This will query the GitHub API and catalogue all containers in the DiamondLightSource repository with the nessacary metadata.

## Running the Containers

### Interactive (local)

```
podman run --publish 8888:8888 ghcr.io/diamondlightsource/bookshelf-template/interactive:latest
```
or
```
module load bookshelf/bookshelf-i18-xrf/latest
bookshelf-i18-xrf-interactive
```

### Interactive (hosted)

1.  Go to https://jupyterhub.diamond.ac.uk/hub/home
2.  'Start My Server' with `CONTAINER_IMAGE=ghcr.io/diamondlightsource/bookshelf-i18-xrf/interactive:latest`

### Processing

```
podman run --volume .:/outputs --volume .:/inputs --security-opt=label=type:container_runtime_t ghcr.io/diamondlightsource/bookshelf-template/processing:latest
```
or
```
module load bookshelf/bookshelf-i18-xrf/latest
bookshelf-i18-xrf-processing
```

### Service (local)

```
podman run --publish 8000:8000 ghcr.io/diamondlightsource/bookshelf-template/service:latest
```
