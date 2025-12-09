import open3d as o3d
import numpy as np
import pandas as pd
import os
import argparse


def render_and_save(mesh, filename, width=1920, height=1080, bg_color=[1, 0.9, 0.95]):
    """Render the mesh beautifully and save an HD screenshot."""
    vis = o3d.visualization.Visualizer()
    vis.create_window(visible=False, width=width, height=height)
    vis.add_geometry(mesh)

    opt = vis.get_render_option()
    opt.background_color = np.asarray(bg_color)  # soft pinkish tone 🌸
    opt.light_on = True
    opt.mesh_show_back_face = True
    opt.point_size = 2.0
    opt.show_coordinate_frame = False
    opt.mesh_color_option = o3d.visualization.MeshColorOption.Color

    ctr = vis.get_view_control()
    ctr.set_zoom(0.8)

    vis.poll_events()
    vis.update_renderer()
    vis.capture_screen_image(filename)
    vis.destroy_window()


def process_mesh(mesh_path, output_dir, bins=256, visualize=True):
    print(f"\n🔹 Processing {os.path.basename(mesh_path)}")

    mesh = o3d.io.read_triangle_mesh(mesh_path)
    if mesh.is_empty():
        print("⚠️ Mesh is empty or unreadable, skipping.")
        return None

    vertices = np.asarray(mesh.vertices)
    print(f"✅ Loaded with {len(vertices)} vertices")

    # Normalize and quantize
    norm_vertices = (vertices - vertices.mean(axis=0)) / vertices.std(axis=0)
    quant_vertices = np.floor(
        (norm_vertices - norm_vertices.min()) /
        (norm_vertices.max() - norm_vertices.min()) * bins
    )

    # Reconstruct new meshes
    mesh_norm = o3d.geometry.TriangleMesh(
        vertices=o3d.utility.Vector3dVector(norm_vertices),
        triangles=mesh.triangles
    )
    mesh_quant = o3d.geometry.TriangleMesh(
        vertices=o3d.utility.Vector3dVector(quant_vertices),
        triangles=mesh.triangles
    )

    mesh_norm.compute_vertex_normals()
    mesh_quant.compute_vertex_normals()

    # Save processed versions
    name = os.path.splitext(os.path.basename(mesh_path))[0]
    norm_path = os.path.join(output_dir, f"{name}_normalized.ply")
    quant_path = os.path.join(output_dir, f"{name}_quantized.ply")

    o3d.io.write_triangle_mesh(norm_path, mesh_norm)
    o3d.io.write_triangle_mesh(quant_path, mesh_quant)

    print(f"💾 Saved normalized & quantized meshes for {name}")

    # Render HD screenshots
    render_and_save(mesh_norm, os.path.join(output_dir, f"{name}_normalized.png"))
    render_and_save(mesh_quant, os.path.join(output_dir, f"{name}_quantized.png"))
    print(f"📸 Saved HD screenshots for {name}")

    # Optional: interactive 3D view
    if visualize:
        print("🌀 Opening interactive 3D window — rotate/zoom and close to continue...")
        o3d.visualization.draw_geometries([mesh_norm], window_name=f"{name} - Normalized Mesh 🌸")
        o3d.visualization.draw_geometries([mesh_quant], window_name=f"{name} - Quantized Mesh 💖")

    return {
        "name": name,
        "num_vertices": len(vertices),
        "min_x": vertices[:, 0].min(),
        "max_x": vertices[:, 0].max(),
        "min_y": vertices[:, 1].min(),
        "max_y": vertices[:, 1].max(),
        "min_z": vertices[:, 2].min(),
        "max_z": vertices[:, 2].max(),
    }


def main():
    parser = argparse.ArgumentParser(description="3D Mesh Preprocessing with Visualization 🌸")
    parser.add_argument("--input_dir", type=str, required=True, help="Folder containing mesh files")
    parser.add_argument("--output_dir", type=str, required=True, help="Folder to save processed meshes")
    parser.add_argument("--bins", type=int, default=256, help="Quantization bins")
    parser.add_argument("--no_vis", action="store_true", help="Disable interactive 3D visualization")
    args = parser.parse_args()

    input_dir = args.input_dir
    output_dir = args.output_dir
    visualize = not args.no_vis

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    summary = []

    # Process all supported mesh files
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.obj', '.ply', '.stl', '.fbx', '.glb')):
            mesh_path = os.path.join(input_dir, filename)
            print(f"\n🔹 Now processing: {filename}")
            result = process_mesh(mesh_path, output_dir, bins=args.bins, visualize=visualize)
            if result:
                summary.append(result)
        else:
            print(f"⚪ Skipping non-mesh file: {filename}")

    # Save CSV summary
    if summary:
        df = pd.DataFrame(summary)
        csv_path = os.path.join(output_dir, "summary.csv")
        df.to_csv(csv_path, index=False)
        print(f"\n✅ All meshes processed successfully! Summary saved to {csv_path}")
    else:
        print("\n⚠️ No valid meshes found in input directory.")


if __name__ == "__main__":
    main()
