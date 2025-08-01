import bpy
import json
import mathutils

# ===== CONFIG =====
POSE_JSON = "pose_data/are_you_free_today.json"  # Change for each animation
ARMATURE_NAME = "Armature"  # Name of your rig in Blender
BONE_MAP = {
    11: "mixamorig:LeftArm",
    13: "mixamorig:LeftForeArm",
    15: "mixamorig:LeftHand",
    12: "mixamorig:RightArm",
    14: "mixamorig:RightForeArm",
    16: "mixamorig:RightHand",
}
# ==================

# Load pose data
with open(POSE_JSON) as f:
    frames_data = json.load(f)

armature = bpy.data.objects[ARMATURE_NAME]
bpy.context.view_layer.objects.active = armature
bpy.ops.object.mode_set(mode="POSE")

for frame_idx, frame_data in enumerate(frames_data, start=1):
    bpy.context.scene.frame_set(frame_idx)

    if "pose" not in frame_data:
        continue

    pose_points = frame_data["pose"]

    for mp_index, bone_name in BONE_MAP.items():
        if bone_name in armature.pose.bones and mp_index < len(pose_points):
            # Convert normalized coordinates to Blender location
            x, y, z = pose_points[mp_index]
            loc = mathutils.Vector((x, y, z))
            armature.pose.bones[bone_name].location = loc
            armature.pose.bones[bone_name].keyframe_insert(data_path="location", frame=frame_idx)

# Set end frame for animation
bpy.context.scene.frame_end = len(frames_data)

print(f"Animation imported from {POSE_JSON}")
