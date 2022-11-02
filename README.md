# AI-Final

## Requirement

### Bazel

[Bazel](https://bazel.build) 5.3.1

Use [Bazelisk](https://github.com/bazelbuild/bazelisk) for automatic easy installation.

[anaconda](https://docs.anaconda.com/anaconda/install/index.html) or [miniconda](https://docs.conda.io/en/latest/miniconda.html) if you don't want full anaconda environment

### node.js

[node.js](https://nodejs.org/)

## Project Setup

### Conda

#### Create conda environment

```bash
conda env create -f="./environment.yml"
```

#### activate conda environment

```bash
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
bazel build //projects/lib
bazel build //projects/backend
bazel build //projects/frontend
```
