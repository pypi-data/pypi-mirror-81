# 1. Install Package ( windows / Linux / Mac )
### 1.1. requirements
> - Python 3.x
> - jupyter notebook or anaconda env  
>   _pip install jupyter_ <br>
>   or <br>
>   _python -m pip install --user jupyter_ <br>
>
>   _pip3 install jupyter_  <br>
>   or <br>
>   _python3 -m pip install --user jupyter_ <br>

### 1.2. Install VisualPython package  
> **[pip / conda]**  
> _pip install visualpython_

### 1.3. Optional package
* jupyter_contrib_nbextensions<br> 
* Install to manage nbtextensions visually.
>> **[pip]**<br>
>>  _pip install jupyter_contrib_nbextensions <br>_
   _jupyter contrib nbextension install --user_
>> **[conda - anaconda env]**  
> _conda install -c conda-forge jupyter_contrib_nbextensions_ <br>
   _jupyter contrib nbextension install --user_

# 2.Package controller for Linux/Mac
### 2.1. VisualPython contoller info

> **usage: _visualpy [option]_** <br>

```
  optional arguments:
   -h,   -H, help       - show this help message and exit
   -e,   -E, enable     - enable VisualPython
   -d,   -D, disable    - disable VisualPython
   -i,   -I, install    - install VisualPython extensions
   -un, -UN, uninstall  - uninstall VisualPython packages
   -up, -UP, upgrade    - upgrade VisualPython Package
   -v,   -V, version    - show VisualPython current version
   -o,   -O, overwrite  - overwrite VisualPython extensions
```

### 2.2. Activate VisualPython
> _visualpy install_ <br>
> or <br>
> _visualpy -i_

### 2.3. Disable VisualPython
> _visualpy disable_ <br>
> or  
> _visualpy -d_

### 2.4. Enable VisualPython extension
> _visualpy enable_ <br>
> or <br>
> _visualpy -e_

### 2.5. Upgrade VisualPython package version
> _visualpy upgrade_ <br>
> or <br>
> _visualpy -up_

### 2.6. Uninstall VisualPython package
> _visualpy uninstall_ <br>
> or <br>
> _visualpy -un_

### 2.7. Overwrite VisualPython package
* manually upgrade <br>
* step <br>
> 1) pip show visualpython<br>
> 2) Check result value of "Location" string.<br>
> 3) Move to "Location" dir.<br>
> 4) Replace new and existing files at "Location" dir.<br>
> 5) After replace files run cmd.<br>
>> _visualpy overwrite_ <br>
>> or <br>
>> _visualpy -o_

# 3.Package controller for Windows
### 3.1. visualpython controller info

> usage: _visualpy [option]_<br>

```
  optional arguments:
   -h,   -H, help       - show this help message and exit
   -e,   -E, enable     - enable VisualPython
   -d,   -D, disable    - disable VisualPython
   -i,   -I, install    - install VisualPython extensions
   -un, -UN, uninstall  - uninstall VisualPython packages
   -up, -UP, upgrade    - upgrade VisualPython Package
   -v,   -V, version    - show VisualPython current version
   -o,   -O, overwrite  - overwrite VisualPython extensions
                          manual version upgrade
```

### 3.2. Activate VisualPython
> _visualpy -i_ <br>
> or <br>
> _visualpy install_ <br>

### 3.3 Disable VisualPython
> _visualpy -d_ <br>
> or <br>
> _visualpy disable_ <br>

### 3.4. Enable VisualPython extension
> _visualpy -e_ <br>
> or <br>
> _visualpy enable_ <br>

### 3.5. Upgrade VisualPython package version
> _visualpy -up_ <br>
> or <br>
> _visualpy upgrade_ <br>

### 3.6. Uninstall VisualPython package
> _visualpy -un_ <br>
> or <br>
> _visualpy uninstall_ <br>
