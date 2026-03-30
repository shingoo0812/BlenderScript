bl_info = {
    "name": "My Pie Menu Addon",
    "author": "You",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "3D View",
    "description": "Simple custom pie menu",
    "category": "3D View",
}

import bpy

addon_keymaps = []


# 🔹 Operator (optional, example)
class MY_OT_test(bpy.types.Operator):
    bl_idname = "my.test"
    bl_label = "Test Operator"

    def execute(self, context):
        print("Hello from Pie Menu")
        return {'FINISHED'}


# 🔹 Pie Menu
class MY_MT_pie(bpy.types.Menu):
    bl_label = "My Pie Menu"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        pie.operator("wm.save_mainfile", text="Save")
        pie.operator("wm.open_mainfile", text="Open")
        pie.operator("object.delete", text="Delete")
        pie.operator("mesh.primitive_cube_add", text="Add Cube")
        pie.operator("my.test", text="Test")


# 🔹 Register
def register():
    bpy.utils.register_class(MY_OT_test)
    bpy.utils.register_class(MY_MT_pie)

    # Keymap
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    if kc:
        km = kc.keymaps.new(name="3D View", space_type='VIEW_3D')
        kmi = km.keymap_items.new("wm.call_menu_pie", 'Q', 'PRESS')
        kmi.properties.name = "MY_MT_pie"

        addon_keymaps.append((km, kmi))


# 🔹 Unregister
def unregister():
    # remove keymap
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    bpy.utils.unregister_class(MY_MT_pie)
    bpy.utils.unregister_class(MY_OT_test)


if __name__ == "__main__":
    register()