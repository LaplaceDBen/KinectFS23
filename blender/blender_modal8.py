"""
Version 8: mit unlimitierter Queue
"""

import time
import os
import re
import bpy
import math
import threading

log_path = r"C:\Users\rapha\OneDrive\Desktop\CDS_FS23\Projektarbeit\GitHubNew\KinectFS23\blender\qr_codes_test2.log"      # Test-Logfile
# log_path = r"C:\Users\rapha\OneDrive\Desktop\CDS_FS23\Projektarbeit\GitHubNew\KinectFS23\qr_codes.log"                  # Echtes Logfile

object_dict = {
    "Haus_A":"House",
    "Haus_B":"Modern House",
    "Haus_C":"Apartment building",
    "Haus_D":"House.001",
    "Baum"  :"Tree"
}

# Information extrahieren 
def object_handling(log_object):  # Input ist das "log_object", alle Informationen zu einem einzelnen Objekt aus der Zeile im Logfile
    blender_object = bpy.data.objects.get(object_dict.get(log_object[0]))   # Blender Objekt auswählen entsprechend dem Namen
    info = (int(log_object[1]), int(log_object[2]), float(log_object[3]))   # y- und y-Koordinate, Rotation
    return blender_object, info

# Objekte bewegen und rotieren
def move(blender_object, info):
        blender_object.location.x = info[0]*0.3
        blender_object.location.y = info[1]*0.3
        blender_object.rotation_euler.z = math.radians(info[2])

# Klasse, die neue Zeilen aus dem Logfile holt
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
            file.seek(0, os.SEEK_END)   # Zur letzten Zeile springen
            while not self.stopped():
                line = file.readline()
                if not line:            # Falls keine neue Zeile da ist, kurz warten
                    time.sleep(0.001)
                    continue
                self.callback(line)

# Modal Operator (spezieller Operator in Blender für laufende Aktionen und Events)
class OBJECT_OT_modal_operator(bpy.types.Operator):
    bl_idname = "object.modal_operator"
    bl_label = "Move Objects"
    _timer = None

    def __init__(self):
        self.log_line_queue = []
        self.log_line_lock = threading.Lock()   # Nur ein Prozess darf aufs mal auf die log_line zugreifen

    def modal(self, context, event):
        if event.type in {"Q", "LEFTMOUSE", "ESC"}:     # Script stoppen, wenn eine dieser Tasten gedrückt wird
            self.log_thread.stop()
            self.log_thread.join()
            return {"CANCELLED"}
        
        with self.log_line_lock:
            if self.log_line_queue:                     # Wenn etwas in der Queue ist...
                log_line = self.log_line_queue.pop(0)   # Vordeste Zeile nehmen...
                log_objects = re.findall(r"QRCODE:\s([\w]+),\s\(([-]?\d+),\s([-]?\d+)\),\s([\d\.]+)\s\|\s", log_line)   # Mit RegEx die Objekte "trennen"
                # Reihenfolge der Objekte in der log_line ist zufällig, manchmal steht zuerst "Haus_A" und manchmal "Haus_D"

                for log_object in log_objects:                          # Für jedes log_object (für jeden QR-Code in der log_line)...
                    blender_object, info = object_handling(log_object)  # Infos aus dem log_object holen und passendes Blender Objekt auswählen
                    if blender_object:                                  # Falls das Blender Objekt ausgewählt werden konnte
                        move(blender_object, info)                      # Blender Objekt bewegen

                # Blender Layout aktualisieren, "zeichnen"
                bpy.context.view_layer.update()
                bpy.ops.wm.redraw_timer(type="DRAW_WIN_SWAP", iterations=1)
                # current_time = time.strftime("%H:%M:%S")
                # print("Moved Houses, current time:", current_time)
        return {"RUNNING_MODAL"}

    def execute(self, context):
        self._timer = context.window_manager.event_timer_add(0.005, window=context.window)  # Die Funktion "modal" wird in diesem Intervall ständig aufgerufen, solange der Modal Operator aktiv ist
        self.log_thread = FollowLogThread(log_path, self.add_log_line) 
        self.log_thread.start()
        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}

    def add_log_line(self, line):
        with self.log_line_lock:
            self.log_line_queue.append(line)

    def cancel(self, context):
        context.window_manager.event_timer_remove(self._timer)
        self.log_thread.stop()

def register(): # Das wird benötigt, dass die Klasse in Blender als Operator registriert wird.
    bpy.utils.register_class(OBJECT_OT_modal_operator)

def unregister(): # Operator wieder entfernen, potentielle Konflikte entfernen
    bpy.utils.unregister_class(OBJECT_OT_modal_operator)

if __name__ == "__main__":
    register()
    bpy.ops.object.modal_operator()