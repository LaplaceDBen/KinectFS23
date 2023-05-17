bl_info = {
    "name": "Kinect Project",
    "author": "Raphael Brunold, Benito Rusconi",
    "version": (1, 0),
    "blender": (3, 5, 0),
    "location": "View3D > Object > Default Locations",
    "description": "Changing the location of objects based on contents of a logfile",
    "category": "Object",
}

import time
import os
import re
import bpy
import math
import threading

logPath = r"C:\Users\rapha\OneDrive\Desktop\CDS_FS23\Projektarbeit\GitHubNew\KinectFS23\blender\qr_codes_test2.log"      # Test-Logfile
# logPath = r"C:\Users\rapha\OneDrive\Desktop\CDS_FS23\Projektarbeit\GitHubNew\KinectFS23\qr_codes.log"                # Echtes Logfile

class KinectProjectPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_kinect_project"
    bl_label = "Kinect Project"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Kinect Project"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator(OBJECT_OT_modal_operator.bl_idname)
        

object_dict = {
    "Haus_A":"House",
    "Haus_B":"Modern House",
    "Haus_C":"Apartment building",
    "Haus_D":"House.001",
    "Baum"  :"Tree"
}

def object_handling(log_object):
    blender_object = bpy.data.objects.get(object_dict.get(log_object[0]))
    info = (int(log_object[1]), int(log_object[2]), float(log_object[3]))
    return blender_object, info

def move(blender_object, info):
        blender_object.location.x = info[0]*0.3
        blender_object.location.y = info[1]*0.3
        blender_object.rotation_euler.z = math.radians(info[2])


class FollowLogThread(threading.Thread):
    def __init__(self, path, callback):
        super().__init__()
        self.path = path
        self.callback = callback
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        with open(self.path, "r", encoding="utf8") as file:
            file.seek(0, os.SEEK_END)
            while not self.stopped():
                line = file.readline()
                if not line:
                    time.sleep(0.005)
                    continue
                self.callback(line)

class OBJECT_OT_modal_operator(bpy.types.Operator):
    """Modal Operator"""
    bl_idname = "object.modal_operator"
    bl_label = "Move Objects"
    _timer = None

    def __init__(self):
        self.log_line_queue = []
        self.log_line_lock = threading.Lock()

    def modal(self, context, event):
        if event.type in {'Q', 'LEFTMOUSE', 'ESC'}:
            self.log_thread.stop()
            self.log_thread.join()
            return {'CANCELLED'}
        
        with self.log_line_lock:
            if self.log_line_queue:
                log_line = self.log_line_queue.pop(0)
                log_objects = re.findall(r"QRCODE:\s([\w]+),\s\(([-]?\d+),\s([-]?\d+)\),\s([\d\.]+)\s\|\s", log_line)

                for log_object in log_objects:
                    blender_object, info = object_handling(log_object)
                    if blender_object:
                        move(blender_object, info)

                # Call view_layer.update() and wm.redraw_timer() outside the loop
                bpy.context.view_layer.update()
                bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
                current_time = time.strftime("%H:%M:%S")
                print("Moved Houses, current time:", current_time)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        self._timer = context.window_manager.event_timer_add(0.01, window=context.window)
        self.log_thread = FollowLogThread(logPath, self.add_log_line)
        self.log_thread.start()
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def add_log_line(self, line):
        with self.log_line_lock:
            self.log_line_queue.append(line)

    def cancel(self, context):
        context.window_manager.event_timer_remove(self._timer)
        self.log_thread.stop()

def register():
    bpy.utils.register_class(OBJECT_OT_modal_operator)
    bpy.utils.register_class(KinectProjectPanel)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_modal_operator)
    bpy.utils.unregister_class(KinectProjectPanel)

if __name__ == "__main__":
    register()
    bpy.ops.object.modal_operator()