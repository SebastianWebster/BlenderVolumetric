import bpy
import os

def create_material_with_textures(layer_index, color_folder, depth_folder,depth_amount=0.2):
    # Create a new material
    material = bpy.data.materials.new(name=f"Material_Layer_{layer_index}")
    material.use_nodes = True

    # Get the material node tree
    nodes = material.node_tree.nodes
    links = material.node_tree.links

    # Clear default nodes
    nodes.clear()

    # Add Material Output node
    output_node = nodes.new(type="ShaderNodeOutputMaterial")
    output_node.location = (700, 200)

    # Add Color Texture Image node
    color_texture_node = nodes.new(type="ShaderNodeTexImage")
    color_texture_node.location = (-600, 200)
    color_texture_node.interpolation = 'Linear'
    color_texture_node.extension = 'EXTEND'
    color_texture_node.image_user.use_auto_refresh = True
    color_texture_node.image_user.frame_duration = 290
    color_texture_node.image = bpy.data.images.load(os.path.join(color_folder, sorted(os.listdir(color_folder))[0]))
    color_texture_node.image.source = 'SEQUENCE'
    color_texture_node.image.filepath = os.path.join(color_folder, sorted(os.listdir(color_folder))[0])

    # Add Depth Texture Image node
    depth_texture_node = nodes.new(type="ShaderNodeTexImage")
    depth_texture_node.location = (-600, -200)
    depth_texture_node.interpolation = 'Linear'
    depth_texture_node.extension = 'EXTEND'
    depth_texture_node.image = bpy.data.images.load(os.path.join(depth_folder, sorted(os.listdir(depth_folder))[0]))
    depth_texture_node.image.source = 'SEQUENCE'
    depth_texture_node.image_user.use_auto_refresh = True
    depth_texture_node.image_user.frame_duration = 290
    depth_texture_node.image.filepath = os.path.join(depth_folder, sorted(os.listdir(depth_folder))[0])

    # Name of the Node Group you want to reference
    node_group_name = "NodeGroup"
    node_group = None
    # Ensure the node group exists
    if node_group_name in bpy.data.node_groups:
        node_group = bpy.data.node_groups[node_group_name]
    else:
        print(f"Node group '{node_group_name}' not found!")
        node_group = None

    # Add the Node Group to a Material
    if node_group:
        
        if material is None:
            print("Material not found!")
        else:
            # Enable 'Use Nodes' if it's not already enabled
            if not material.use_nodes:
                material.use_nodes = True

            # Access the material's node tree
            node_tree = material.node_tree

            # Add a Node Group to the material
            node_group_node = node_tree.nodes.new(type="ShaderNodeGroup")
            node_group_node.node_tree = node_group

            # Position the node (optional)
            node_group_node.location = (200, 200)

            print(f"Node group '{node_group_name}' added to material '{material.name}'.")

    # Link nodes
    links.new(color_texture_node.outputs[0], node_group_node.inputs[1])  # Base Color    links.new(depth_texture_node.outputs[0], node_group_node.inputs[1])  # Displacement height
    links.new(depth_texture_node.outputs[0], node_group_node.inputs[2])  # Base Color    links.new(depth_texture_node.outputs[0], node_group_node.inputs[1])  # Displacement height
    
    links.new(node_group_node.outputs[0], output_node.inputs[0])  # Surface output
    links.new(node_group_node.outputs[1], output_node.inputs[2])  # Displacement output


    # Set material displacement method to "Displacement and Bump"
    material.displacement_method = "DISPLACEMENT"
    material.use_backface_culling = True
    material.use_backface_culling_shadow = False
    

    return material

def create_plane(layer_index, color_folder, depth_folder, z_offset, scale_factor, z_scale_reduction,subdivisions=1,depth_amount=0.2):
    # Load the first image to determine aspect ratio
    image_files = sorted([f for f in os.listdir(color_folder) if f.endswith('.png')])
    if not image_files:
        print(f"No images found in {color_folder}")
        return

    first_image_path = os.path.join(color_folder, image_files[0])
    img = bpy.data.images.load(first_image_path)
    aspect_ratio = img.size[0] / img.size[1]

    # Calculate Z position and scale
    z_location = layer_index * z_offset
    scale_adjustment = max(0.05, 1 - (z_scale_reduction * layer_index))

    # Create the plane
    bpy.ops.mesh.primitive_plane_add(size=2, location=(0, 0, z_location))
    plane = bpy.context.object
    plane.scale = (aspect_ratio * scale_adjustment, scale_adjustment, 1)
    plane.visible_shadow = False
    plane.visible_volume_scatter = False
    plane.visible_transmission = False

    bpy.ops.object.mode_set(mode='EDIT')  # Switch to Edit mode
    bpy.ops.mesh.subdivide(number_cuts=subdivisions)  # Apply subdivisions
    bpy.ops.mesh.subdivide(number_cuts=subdivisions)  # Apply subdivisions
    bpy.ops.object.mode_set(mode='OBJECT')  # Return to Object mode
    
    mesh = plane.data
    for f in mesh.polygons:
        f.use_smooth = True
    
    # Assign material to the plane
    material = create_material_with_textures(layer_index, color_folder, depth_folder,depth_amount)
    plane.data.materials.append(material)
    plane.name = f"Layer_{layer_index}"
    print(f"Created plane for layer {layer_index}")

def import_volumetric_video(base_folder, z_offset=0.1, z_scale_reduction=0.05,depth_amount=0.5):
    # Get all Layer and LayerDepth folders
    color_folders = sorted([f for f in os.listdir(base_folder) if f.startswith("Layer_")])
    depth_folders = sorted([f for f in os.listdir(base_folder) if f.startswith("LayerDepth_")])

    if len(color_folders) != len(depth_folders):
        print("Mismatch between Layer and LayerDepth folders")
        return

    for i, (color_folder, depth_folder) in enumerate(zip(color_folders, depth_folders)):
        color_path = os.path.join(base_folder, color_folder)
        depth_path = os.path.join(base_folder, depth_folder)
        
        create_plane(i, color_path, depth_path, z_offset, scale_factor=0.01, 
                        z_scale_reduction=z_scale_reduction,subdivisions=10,depth_amount=depth_amount)

    print("All planes created successfully.")

# Specify the base folder containing Layer_N and LayerDepth_N folders
base_folder = "F:\Projects\BlenderVolumetric\SourceVideo\Clip_1\Clip_1_Layers\out"
import_volumetric_video(base_folder, z_offset=0.25, z_scale_reduction=0.05,depth_amount=0.3)
