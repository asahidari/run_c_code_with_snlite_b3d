# Running external C code with SNLite

## Description

This project is an example of running external C code with Script Node Lite (SNLite) node of [Sverchok add-on](https://github.com/nortikin/sverchok) for [Blender](https://www.blender.org). You can also use this as a template, when you intend to run your own C/C++ codes in Blender.

This project idea is originated from [@zeffi's gist](https://gist.github.com/zeffii/9e156f0d37977fd1b0ca3c65d0ddc611) and [nortikin/sverchok#2152](https://github.com/nortikin/sverchok/issues/2152) .

## Usage

### Create C library and modify Python file
- Create C dynamic library in advance, from C file in the same directory.  
    
    ```console
    :: Windows
    cl.exe /D_USRDLL /D_WINDLL scale_verts.c /MT /link /DLL /OUT:libscale_verts.dll
    ```
    ```sh
    # macOS
    gcc -dynamiclib -o ./libscale_verts.dylib ./scale_verts.c
    ```
    ```sh
    # Linux
    gcc -c -fPIC scale_verts.c -o scale_verts.o
    gcc scale_verts.o -shared -o libscale_verts.so
    ```
### Open Sverchok node editor
- Install Blender and Sverchok add-on.
- Enable the add-on with Menu->Edit->Preferences...-> add-ons.  
- Open sverchok node editor, and click '+New' button in the header.  

### Use SNLite node
- Press 'Shift-A' and select 'scripts'->'ScriptNodeLite'.  
- Open Text editor in Blender and click '+New' to create a text buffer.
- Copy and paste the Python script to the text buffer.
- Modify "load_library" arguments in the script to load your library.
    
    ```python
            # load library
            libscale_verts = npct.load_library('libscale_verts', os.path.dirname('/Path/to/the/library/directory/'))
    ```
- Put the the text buffer name to the node and click the right button.
- Set the node parameters and input some vertices to the node.  
- After that, calculation run and you can use output data, changing 'framenum' parameter.  

![Image of runningscript with SNLite](./images/scale_verts_screen_shot.png)

## Use this project as a template for running C coode
- Modify original script and C code for your own projects, especially for projects that require large amount of calculation and high performance.

#### Project Files
- scale_verts.py  
- scale_verts.c  

## Requirements
* Blender 2.8 (or later)
* sverchok add-on 0.6 (or later)

## Author
asahidari

## Licence
[GPL 3](https://www.gnu.org/licenses/quick-guide-gplv3.html)
