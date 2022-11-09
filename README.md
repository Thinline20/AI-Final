# AI-Final

## Requirement

### Bazel

[Bazel](https://bazel.build) 5.3.1

Use [Bazelisk](https://github.com/bazelbuild/bazelisk) for automatic easy installation.

### Conda

[anaconda](https://docs.anaconda.com/anaconda/install/index.html) or [miniconda](https://docs.conda.io/en/latest/miniconda.html) if you don't want full anaconda environment

### node.js

[node.js](https://nodejs.org/)

## Project Setup

### Create and activate conda environment

```bash
conda env create -f="./environment.yml"
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
