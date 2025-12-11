# 3D Mesh Normalization and Quantization Pipeline

A reproducible pipeline for normalizing, remeshing, and quantizing 3D meshes.  
Designed for preprocessing datasets, geometric compression experiments, and machine learning workflows involving 3D shape data.

---

## Overview

This project provides tools to:

- Load meshes (.obj, .ply, .stl, etc.)
- Clean and repair invalid geometry (optional)
- Normalize vertex coordinates (centering and scaling)
- Optionally resample or decimate meshes
- Normalize auxiliary attributes such as normals and UVs
- Quantize vertex positions using fixed bit-depth (8, 12, 16, or 24 bits)
- Output metadata for perfect reconstruction of the original scale

---

## Features

- Normalization modes  
  - `unit_sphere`: centers and fits mesh inside a radius-1 sphere  
  - `unit_box`: scales mesh to fit within a 1×1×1 box  

- Quantization  
  - Uniform scalar quantization  
  - Customizable bit depth  
  - Optional quantization of normals  

- Optional remeshing or decimation  
- Python API and command-line interfaces  
- Metadata stored for reconstruction (scale, offset, bit depth)

---

## Repository Structure

.
├── scripts/
│ ├── normalize.py
│ ├── quantize.py
│ └── pipeline.py
├── mesh_utils/
│ ├── io.py
│ ├── clean.py
│ ├── normalize.py
│ ├── remesh.py
│ └── quantize.py
├── data/
├── notebooks/
├── tests/
├── requirements.txt
└── README.md



---

## Installation

```bash
git clone https://github.com/sheebanadeem/3D-Mesh-normalization-and-quantization-pipeline.git
cd 3D-Mesh-normalization-and-quantization-pipeline

python -m venv .venv
source .venv/bin/activate   # macOS / Linux
.venv\Scripts\activate      # Windows

pip install -r requirements.txt
```
### Common dependencies include:

nginx
Copy code
numpy
trimesh
scipy
open3d
tqdm
Usage
Command-line examples
###Normalize mesh:

```bash

python scripts/normalize.py \
    --input data/bunny.obj \
    --output data/bunny_normalized.obj \
    --mode unit_sphere
```
###Quantize mesh:

```bash
Copy code
python scripts/quantize.py \
    --input data/bunny_normalized.obj \
    --output data/bunny_q16.obj \
    --bits 16
```
###Run full pipeline:

```bash

python scripts/pipeline.py \
    --input data/model.obj \
    --out-dir outputs/ \
    --normalize-mode unit_box \
    --target-vertices 10000 \
    --quant-bits 12
```
###Python API
```bash

from mesh_utils.io import load_mesh, save_mesh
from mesh_utils.normalize import normalize_mesh
from mesh_utils.quantize import quantize_mesh

mesh = load_mesh("data/model.obj")
mesh_norm, meta = normalize_mesh(mesh, mode="unit_box")
mesh_q = quantize_mesh(mesh_norm, bits=12)
save_mesh(mesh_q, "outputs/model_q12.obj")
```
###Example Notebooks
See the notebooks/ directory for:

step-by-step mesh normalization

visualization of before/after

quantization error measurement

compression comparisons

###Evaluation Metrics
Common metrics for evaluating quantization:

RMSE between original and dequantized vertices

Maximum deviation or Hausdorff distance

Angular error in normals

Compression ratio and file size savings

###Testing
Run tests using:

```bash

pytest -q
```
Tests may include:

IO round-trip integrity

Correctness of normalization

Quantization/dequantization error thresholds

Contributing
Fork the repository

Create a branch (git checkout -b feature-name)

Add tests for new features

Open a pull request



###Author
Developed by Sheeba Nadeem.












