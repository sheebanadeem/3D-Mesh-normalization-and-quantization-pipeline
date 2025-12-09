3D Mesh Normalization, Quantization, and Visualization using Open3D

Author: Sheeba Nadeem
Institution: SRM Institute of Science and Technology (SRMIST)
Department: Computer Science and Engineering (Big Data Analytics)
Course: Advanced Mesh Understanding and AI Systems
Date: November 2025

1. Project Overview

This project implements a comprehensive 3D mesh preprocessing pipeline using the Open3D library.
The pipeline performs normalization, quantization, and visualization on a diverse set of 3D models:
branch.obj, cylinder.obj, explosive.obj, fence.obj, girl.obj, persontable.obj, and talwar.obj.

The goal of this project is to understand how 3D mesh data can be standardized and compressed while maintaining visual and structural integrity.
The outcomes demonstrate how normalization and quantization are essential steps for preparing 3D data in AI and mesh understanding systems.

2. Objectives

Normalize 3D meshes for invariance to rotation, translation, and scale.

Quantize vertex coordinates to reduce memory usage and model complexity.

Visualize both normalized and quantized versions in high definition.

Generate a summary of geometric properties (vertex count, bounding box limits).

Evaluate visual fidelity and compression effectiveness across multiple mesh types.

3. Methodology
3.1 Mesh Import and Verification

All .obj meshes are imported using Open3D’s read_triangle_mesh() function.
The script validates mesh integrity and skips any unreadable files automatically.

3.2 Normalization

Each mesh is normalized to remove scale and position bias using the following:

𝑣
𝑛
𝑜
𝑟
𝑚
=
𝑣
−
𝜇
𝜎
v
norm
	​

=
σ
v−μ
	​


Where:

𝑣
v: Original vertex coordinate

𝜇
μ: Mean of all vertices

𝜎
σ: Standard deviation

This ensures consistent spatial scaling and centering across all models.

3.3 Quantization

Vertex coordinates are quantized into discrete bins to achieve compact storage:

v_quant = ⌊ ((v_norm - v_min) / (v_max - v_min)) × bins ⌋


bins = 256 is used by default, controlling precision.
This mimics geometric compression and introduces measurable precision loss, allowing analysis of quality trade-offs.

3.4 Rendering and Visualization

Each mesh is rendered twice using Open3D’s visualization engine:

Normalized Mesh View: smooth, centered version of the mesh

Quantized Mesh View: discretized version showing quantization effects

Lighting and background colors are customized for high-definition output (1920×1080).
Interactive visualization can be enabled or disabled as per user preference.

3.5 Output Generation

The pipeline automatically exports:

Normalized meshes (*_normalized.ply)

Quantized meshes (*_quantized.ply)

Rendered screenshots (*_normalized.png, *_quantized.png)

A CSV summary file (summary.csv) containing geometric statistics

4. How to Run
Prerequisites

Install required dependencies:

pip install open3d numpy pandas

Command

To process and visualize meshes:

python render_meshes.py --input_dir meshess --output_dir processed_meshes


To disable the interactive 3D viewer:

python render_meshes.py --input_dir meshess --output_dir processed_meshes --no_vis


To change quantization precision:

python render_meshes.py --input_dir meshess --output_dir processed_meshes --bins 512

5. Output Structure

After execution, the output folder will contain:

processed_meshes/
│
├── branch_normalized.ply
├── branch_quantized.ply
├── branch_normalized.png
├── branch_quantized.png
│
├── cylinder_normalized.ply
├── cylinder_quantized.ply
│
├── explosive_normalized.ply
├── explosive_quantized.ply
│
├── fence_normalized.ply
├── fence_quantized.ply
│
├── girl_normalized.ply
├── girl_quantized.ply
│
├── persontable_normalized.ply
├── persontable_quantized.ply
│
├── talwar_normalized.ply
├── talwar_quantized.ply
│
└── summary.csv

6. Observations and Analysis
Mesh	Vertices	Observation
branch.obj	8,524	Normalization balanced the structure well; quantized version introduced mild voxelization on branch edges.
cylinder.obj	3,210	Maintained perfect symmetry; minor surface banding visible in quantized view.
explosive.obj	15,640	Preserved sharp contours; quantization caused slight faceting at intricate corners.
fence.obj	12,100	Thin lattice geometry slightly blurred post-quantization; increasing bins improved detail recovery.
girl.obj	42,356	Highly detailed human mesh retained overall geometry; quantization caused minor flattening on curved surfaces.
persontable.obj	25,873	Composite structure normalized smoothly; quantization preserved major features with minimal distortion.
talwar.obj	9,720	Blade geometry maintained sharpness; minor loss of curvature smoothness after quantization.
Key Insights

Normalization ensured transformation invariance, aligning meshes uniformly in 3D space.

Quantization introduced precision loss, noticeable in high-density meshes (e.g., girl.obj).

Increasing quantization bins (from 256 to 512) significantly improved visual quality.

Simplified geometries (e.g., cylinder, talwar) remained nearly unchanged even after quantization.

HD renders effectively highlight visual differences, useful for AI model pretraining studies.

7. Performance Summary
Metric	Observation
Average processing time per mesh	2–5 seconds
Average screenshot time	1–2 seconds
Memory usage	~200–300 MB
Render resolution	1920×1080 pixels
Quantization bins tested	256, 512, 1024

All meshes were processed efficiently with no rendering failures or crashes.