# AI-Final

## Python

사용하는 기술

- scikit-learn
- FastAPI

## Web

사용하는 기술

- Next.js
- Plotly

## Requirement

[Bazel](https://bazel.build) 5.3.1

Use [Bazelisk](https://github.com/bazelbuild/bazelisk) for automatic easy installation.

[anaconda](https://docs.anaconda.com/anaconda/install/index.html) or [miniconda](https://docs.conda.io/en/latest/miniconda.html) if you don't want full anaconda environment

## Project Setup

### create and activate conda environment

```bash
conda env create -f="./environment.yml"
conda activate ai-final
```

### Bazel Commands

#### Build whole project

```bash
bazel build //...
```

#### Build individual package

```bash
bazel build //projects/lib
bazel build //projects/backend
bazel build //projects/frontend
```
