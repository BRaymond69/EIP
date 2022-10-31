#!/bin/python3

from sys import argv
import open3d as o3d
from PIL import Image

def usage():
    print("""USAGE
    ./modelize.py img_W-H-D.png out.ply [-v | -w]

DESCRIPTION
    img.png    image of a funiture you want to modelize
    W          width of the furniture
    H          height of the furniture
    D          depth of the furniture
    out.ply    output ply file with the 3D mesh
    -v         allow visualisation of the generated mesh
    -w         show wireframe in visualisation

""")

def get_args():
    if "-h" in argv or len(argv) < 3:
        usage()
        exit(0)
    return argv[1:]

def get_coords(filename):
    coords = filename.split('_')[-1].split('.')[0].split('-')
    if len(coords) == 3:
        x, y, z = list(map(int, coords))
    else:
        raise Exception("File format is *_W-H-D.png ((W)idth (H)eight (D)epth)")
    return x, y, z

def get_furniture_color(img, visualisation=False):
    # TODO : Improve this function
    img = Image.open(img, 'r')
    colors = list(set(img.getdata()))
    mr, mg, mb, *_ = colors[0]
    for r, g, b, *_ in colors[1:]:
        mr += r
        mg += g
        mb += b
    nbcols = len(colors)
    mr /= nbcols
    mg /= nbcols
    mb /= nbcols

    if visualisation:
        img.show()

    img.close()
    return mr, mg, mb

def generate_points(width, height, depth):
    points = []
    for z in range(2):
        for y in range(2):
            for x in range(2):
                points += [[-x * width, -y * height, -z * depth]]
    return points

def generate_mesh(points, color=(127, 127, 127), visualisation=False, wireframe=False):
    mesh = o3d.geometry.TriangleMesh.create_box()
    mesh.vertices = o3d.utility.Vector3dVector(points)

    mesh.compute_vertex_normals()
    r, g, b = color
    mesh.paint_uniform_color([r / 255, g / 255, b / 255])

    if visualisation:
        o3d.visualization.draw_geometries([mesh], mesh_show_wireframe=wireframe)
    return mesh

if __name__ == '__main__':
    input_file, output_file, *flags = get_args()
    w, h, d = get_coords(input_file)
    color = get_furniture_color(input_file, "-v" in flags)

    points = generate_points(w, h, d)
    mesh = generate_mesh(points, color, "-v" in flags, "-w" in flags)
    o3d.io.write_triangle_mesh(output_file, mesh)
