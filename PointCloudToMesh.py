import bpy

# ===== 関数定義 =====
def point_cloud_to_mesh(obj=None, voxel_size=0.05, radius=0.15):
    if obj is None:
        obj = bpy.context.object
    if obj is None:
        raise ValueError("対象オブジェクトが見つかりません")

    if obj.type == 'EMPTY':
        children = [c for c in obj.children if c.type == 'MESH']
        pc_children = [c for c in children if len(c.data.polygons) == 0]
        obj = pc_children[0] if pc_children else children[0]
        print(f"EMPTYの子を使用: {obj.name}")

    obj.hide_set(False)
    obj.hide_viewport = False
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.context.view_layer.update()

    for mod in [m for m in obj.modifiers if m.name == "PointsToVolume"]:
        obj.modifiers.remove(mod)

    mod = obj.modifiers.new(name="PointsToVolume", type='NODES')
    if mod is None:
        raise RuntimeError("modifiers.new() が None を返しました")

    ng_name = f"GN_{obj.name}_PtV"
    if ng_name in bpy.data.node_groups:
        bpy.data.node_groups.remove(bpy.data.node_groups[ng_name])
    tree = bpy.data.node_groups.new(ng_name, 'GeometryNodeTree')
    mod.node_group = tree

    nodes = tree.nodes
    links = tree.links

    tree.interface.new_socket('Geometry', in_out='INPUT',  socket_type='NodeSocketGeometry')
    tree.interface.new_socket('Geometry', in_out='OUTPUT', socket_type='NodeSocketGeometry')

    n_in  = nodes.new('NodeGroupInput');             n_in.location  = (-500, 0)
    n_ptv = nodes.new('GeometryNodePointsToVolume'); n_ptv.location = (-200, 0)
    n_vtm = nodes.new('GeometryNodeVolumeToMesh');   n_vtm.location = ( 150, 0)
    n_out = nodes.new('NodeGroupOutput');            n_out.location = ( 450, 0)

    n_ptv.inputs['Resolution Mode'].default_value = 'Size'
    n_ptv.inputs['Voxel Size'].default_value      = voxel_size
    n_ptv.inputs['Radius'].default_value          = radius
    n_ptv.inputs['Density'].default_value         = 1.0

    n_vtm.inputs['Resolution Mode'].default_value = 'Size'
    n_vtm.inputs['Voxel Size'].default_value      = voxel_size
    n_vtm.inputs['Threshold'].default_value       = 0.1
    n_vtm.inputs['Adaptivity'].default_value      = 0.0

    links.new(n_in.outputs[0],         n_ptv.inputs['Points'])
    links.new(n_ptv.outputs['Volume'], n_vtm.inputs['Volume'])
    links.new(n_vtm.outputs['Mesh'],   n_out.inputs[0])

    obj.display_type = 'SOLID'
    with bpy.context.temp_override(object=obj):
        bpy.ops.object.modifier_apply(modifier="PointsToVolume")

    print(f"✅ 完了: {obj.name} → {len(obj.data.vertices)}頂点 / {len(obj.data.polygons)}ポリゴン")
    return obj

# ===== ここで実行 =====
# obj, voxel_size, radius
point_cloud_to_mesh()  # 選択中オブジェクト（EMPTYでも可）