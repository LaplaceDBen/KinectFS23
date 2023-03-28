import numpy as np
import sys
import vispy
import vispy.scene
from vispy.scene import visuals
from vispy import app
from vispy.io import read_mesh

canvas = vispy.scene.SceneCanvas(keys='interactive', show=True)
view = canvas.central_widget.add_view()
view.camera = 'turntable'

# Load a 3D model from an STL file
mesh_data = read_mesh('Test_scripts\\CatanHouse.STL')
//scale mesh_data faktor 10


vertices = mesh_data[0]
faces = mesh_data[1]

# Create a Mesh object and set its position
mesh = visuals.Mesh(vertices=vertices, faces=faces, color=(0.5, 0.5, 1, 1))
mesh.transform = vispy.visuals.transforms.MatrixTransform()
mesh.transform.translate([0, 0, 0])

# Create a scatter plot visual for the updated data
scatter = visuals.Markers()
view.add(mesh)
view.add(scatter)

# Create XYZ axis
axis = visuals.XYZAxis(parent=view.scene)

# Define function to generate updated data each frame
def solver(t):
    pos = np.array([[0.5 + t/100, 0.5, 0], [0, 0, 0.5], [0, 0.5, 0], [0.5, 0, 0]])
    return pos

# Define function to update data each frame
t = 0.0
def update(ev):
    global scatter
    global t
    t += 1.0
    scatter.set_data(solver(t), edge_color=None, face_color=(1, 1, 1, .5), size=10)

# Start timer for updating data
timer = app.Timer()
timer.connect(update)
timer.start(0)

# Show canvas and start event loop
if __name__ == '__main__':
    canvas.show()
    if sys.flags.interactive == 0:
        app.run()
