import bpy

# Delete everything in the scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Create a human meta-rig using Rigify
bpy.ops.object.armature_human_metarig_add()
rig = bpy.context.object
rig.name = "AvatarRig"

# Scale and move the rig to match average human size
rig.scale = (1.0, 1.0, 1.0)
rig.location = (0, 0, 0)

# Switch to Object Mode
bpy.ops.object.mode_set(mode='OBJECT')

# Generate the full Rigify rig
bpy.ops.pose.rigify_generate()

# Hide the metarig
rig.hide_set(True)

# Create a basic human mesh (placeholder body)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(0, 0, 1.7))
head = bpy.context.object
head.name = "AvatarHead"

bpy.ops.mesh.primitive_cube_add(size=0.5, location=(0, 0, 1.0))
body = bpy.context.object
body.name = "AvatarBody"

# Join head and body into one mesh
bpy.ops.object.select_all(action='DESELECT')
head.select_set(True)
body.select_set(True)
bpy.context.view_layer.objects.active = body
bpy.ops.object.join()
avatar_mesh = bpy.context.object
avatar_mesh.name = "AvatarMesh"

# Parent the mesh to the generated rig
bpy.ops.object.select_all(action='DESELECT')
avatar_mesh.select_set(True)
generated_rig = bpy.data.objects["rig"]
generated_rig.select_set(True)
bpy.context.view_layer.objects.active = generated_rig
bpy.ops.object.parent_set(type='ARMATURE_AUTO')

print("✅ Avatar created with rig successfully!")
