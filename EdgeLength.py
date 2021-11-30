bl_info = {
    'name': 'Edges size',
    'category': 'All'
}

import bpy
import numpy as np
import random
import string

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


#selected_edges = [edge.select for edge in bpy.context.selected_objects[0].data.edges]
class EdgesLength(bpy.types.Operator):
    bl_idname = 'mesh.get_edges_length'
    bl_label = 'Get Edges Length'
    bl_options = {"REGISTER", "UNDO"}
    
    total = 0
    
    def GetSelectedEdgesLength(self):
        print('id: '+id_generator())
        selected_obj = bpy.context.selected_objects[0]
        if bpy.context.mode=='EDIT_MESH':
            selected_obj.update_from_editmode ()
#       selectedVerts = [v for v in selected_obj.data.vertices if v.select]
        selectedEdges = [e for e in selected_obj.data.edges if e.select]
        #selectedEdges = [e for e in bpy.context.active_object.data.edges if e.select]
        print(len(selectedEdges))
        total = 0
        localToWorld = selected_obj.matrix_world
        print('local to world:',localToWorld)
        for index,val in enumerate(selectedEdges):
            v1_index = val.vertices[0]
            v2_index = val.vertices[1]
            
            v1 = selected_obj.data.vertices[v1_index].co
            v2 = selected_obj.data.vertices[v2_index].co
            x = v1 - v2
            mag = np.sqrt(x.dot(x))
            total = total + mag
            startVertex = val        
        self.__class__.total = total
        return total
 
    def execute(self, context):
        self.GetSelectedEdgesLength()
        self.report({'INFO'}, str(self.__class__.total))
        return {"FINISHED"}

class panel1(bpy.types.Panel):
    bl_idname = "panel.panel3"
    bl_label = "Panel3"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    #bl_category = "Tools"
    #bl_category = "MeasureTool"
 
    def draw(self, context):        
        self.layout.operator("mesh.get_edges_length", icon='MESH_CUBE', text="Get Edge Length")
        self.layout.label(text=str(EdgesLength.total))

        
 

def register():
    #bpy.utils.register_module(__name__)
    bpy.utils.register_class(EdgesLength)
    bpy.utils.register_class(panel1)
    
def unregister():
    #bpy.utils.unregister_module(__name__)
    bpy.utils.unregister_class(EdgesLength)
    bpy.utils.unregister_class(panel1)

    
if __name__=="__main__":
    register()


