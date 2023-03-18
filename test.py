import pyrender
import trimesh
import numpy as np

# Load the OBJ file
filename = 'model.obj'
mesh = trimesh.load(filename)

# Create a scene
scene = pyrender.Scene()

# Create a mesh node and add it to the scene
mesh_node = pyrender.Mesh.from_trimesh(mesh)
scene.add(mesh_node)

# Define the animation function
def animate(mesh_node, phase):
    # Calculate new z-coordinates for each vertex
    z = np.sin(mesh.vertices[:, 0] * 0.1 + phase) * 0.1

    # Update the z-coordinates of the mesh
    mesh.vertices[:, 2] = z

    # Update the mesh node in the scene
    mesh_node.mesh = trimesh.Trimesh(vertices=mesh.vertices, faces=mesh.faces)

# Create a viewer
viewer = pyrender.Viewer(scene, use_raymond_lighting=True)

# Start the animation loop
for i in range(1000):
    phase = i * 0.1
    animate(mesh_node, phase)
    viewer.render()
