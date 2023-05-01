import time
import os
import re
import bpy
import math
import threading

logPath = r"C:\Users\rapha\OneDrive\Desktop\CDS_FS23\Projektarbeit\GitHubNew\KinectFS23\raffi\qr_codes_test.log"
house_A_object_name = "House"
house_B_object_name = "Modern_house"
house_C_object_name = "Apartment building"
house_D_object_name = "House.001"
tree_object_name = "Tree"

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
                    time.sleep(0.01)
                    continue
                self.callback(line)

class OBJECT_OT_modal_operator(bpy.types.Operator):
    """Modal Operator"""
    bl_idname = "object.modal_operator"
    bl_label = "Modal Operator"
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
                objects = re.findall(r"QRCODE:\s([\w]+),\s\((\d+),\s(\d+)\),\s([\d\.]+)\s\|\s", log_line)
                for obj in objects:
                    if obj[0] == 'Haus_A':
                        house_A = (int(obj[1]), int(obj[2]), float(obj[3]))
                        obj = bpy.data.objects.get(house_A_object_name)
                        if obj:
                            obj.location.x = house_A[0]*0.04
                            obj.location.y = house_A[1]*0.04
                            obj.rotation_euler.z = math.radians(house_A[2])
                    elif obj[0] == 'Haus_B':
                        house_B = (int(obj[1]), int(obj[2]), float(obj[3]))
                        obj = bpy.data.objects.get(house_B_object_name)
                        if obj:
                            obj.location.x = house_B[0]*0.04
                            obj.location.y = house_B[1]*0.04
                            obj.rotation_euler.z = math.radians(house_B[2])

                    elif obj[0] == 'Haus_C':
                        house_C = (int(obj[1]), int(obj[2]), float(obj[3]))
                    elif obj[0] == 'Haus_D':
                        house_D = (int(obj[1]), int(obj[2]), float(obj[3]))
                    elif obj[0] == 'Baum':
                        tree = (int(obj[1]), int(obj[2]), float(obj[3]))

        # Call view_layer.update() and wm.redraw_timer() outside the loop
        bpy.context.view_layer.update()
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
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

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_modal_operator)

if __name__ == "__main__":
    register()
    bpy.ops.object.modal_operator()