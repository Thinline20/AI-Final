# AI-Final

## Requirement

### Bazel

[Bazel](https://bazel.build) 5.3.1

Use [Bazelisk](https://github.com/bazelbuild/bazelisk) for automatic easy installation.

### Conda

[anaconda](https://docs.anaconda.com/anaconda/install/index.html) or [miniconda](https://docs.conda.io/en/latest/miniconda.html) if you don't want full anaconda environment

You can use [Mamba](https://github.com/mamba-org/mamba), a drop in replacement for conda, which is faster and more efficient than conda.

### node.js

[node.js](https://nodejs.org/)

## Project Setup

### Create and activate conda environment

#### With Anaconda or Miniconda

```bash
conda env create -f="./environment.yml"
conda activate ai-final
```

#### With Mamba

Install mamba if you already have conda installed on your machine

```bash
conda install mamba -c conda-forge
```

Alternatively, you can install [micromamba](https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html) which is still at early stage, but it generally works fine for me. Refer to [mamba installation page](https://mamba.readthedocs.io/en/latest/installation.html#installation) for the installation process for your environment.

Next, create and activate conda virtual environment.

```bash
mamba env create -f="./environment.yml"
conda activate ai-final
```

### Prepare pnpm

```bash
corepack enable
```

## Build project

### Build whole project

```bash
bazel build //...
```

### Build individual package

```bash
bazel build //projects/lib:ai-lib
bazel build //projects/backend:backend
bazel build //projects/frontend:frontend
```

## Run project

```bash
bazel run //projects/backend:backend
```

Open another terminal and run command below

```bash
bazel run //projects/frontend:frontend
```

Now, you're good to go
