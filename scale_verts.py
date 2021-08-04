"""
in steps s d=10 n=2
in verts_in v
in scale s d=2.0 n=2
in framenum s d=0 n=2
out verts_out v
"""

# -------------------------------------------------------------------------------
# This script is used with Script Node Lite in Sverchok Blender add-on.
# This script scales vertices with 'scale' value, and repeats it 'steps' times.
# Once the process done, 'verts_out' returns values for each step by changing 'framenum' value.
# -------------------------------------------------------------------------------
#################################################################################
# How to use:
#     * Create C dynamic library in advance, from C file in the same directory.
#     * Then, replace 'load_library' args with your library name and path.
#     * Set parameters of the node, and when 'verts_in' input is connected,
#       '__init__' function is done, and you can use 'verts_out' value.
#################################################################################

def setup():
    
    import numpy as np
    import numpy.ctypeslib as npct
    import os
    import ctypes as ct

    def callback_func(step, dim1, dim2, data, selfp):

        # convert array type from c to numpy
        verts_arr = npct.as_array(ct.POINTER(ct.c_double).from_address(ct.addressof(data)), shape=(dim1, dim2))
        arr_stored = verts_arr.tolist()

        # call class method using self pointer
        instance = ct.cast(selfp, ct.py_object).value
        instance.store_frame(step, arr_stored)

    # class declaration
    # Derived from ctype.Structure to pass self pointer to c function 
    class CMultiply(ct.Structure):

        def __init__(self, steps=10, scale=2.0, verts=None):
            
            self.frame_storage = {}
            if verts == None:
                return;

            # declare callback function c type
            c_arr_type = np.ctypeslib.ndpointer(dtype=ct.c_double, flags='C_CONTIGUOUS')
            callback_func_type = ct.CFUNCTYPE(None, ct.c_int, ct.c_int, ct.c_int, c_arr_type, ct.c_void_p)
            
            # load library
            libscale_verts = npct.load_library('libscale_verts', os.path.dirname('/Path/to/the/library/directory/'))
            
            # declare argtypes and restype
            libscale_verts.process.argtypes = [
               ct.c_int, # step count
               ct.c_double, # scale value
               ct.c_int, # array dimension1
               ct.c_int, # array dimension2
               npct.ndpointer(dtype=np.uintp, ndim=1, flags='C'), # verts array
               callback_func_type, # callback func
               ct.py_object # self
               ]
            libscale_verts.process.restype = ct.c_int

            # convert array type
            verts_arr = np.array(verts)
            verts_arr_ptr = (verts_arr.__array_interface__['data'][0] + np.arange(verts_arr.shape[0])*verts_arr.strides[0]).astype(np.uintp)

            # call c function
            dim1, dim2 = verts_arr.shape[0], verts_arr.shape[1]
            res = libscale_verts.process(steps, scale, dim1, dim2, verts_arr_ptr, callback_func_type(callback_func), ct.py_object(self))

        # get frame
        def get_frame(self, number):
            return self.frame_storage.get(number) if number in self.frame_storage else []

        # store frame
        def store_frame(self, framestep, data):
            self.frame_storage[framestep] = data

    # instantiate main class
    cm = CMultiply(steps, scale, (verts_in[0] if verts_in is not None else None))

# set results per frame
verts_array = cm.get_frame(framenum)
verts_out.append(verts_array)


