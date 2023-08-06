@echo off
rem #==========================================================================
rem # Filename : visualpython.bat
rem # function : control VisualPython for windows
rem # Creator  : BlackLogic - LJ
rem # version  : 1.8
rem # License  :
rem # main prd : visualpython 0.2.0
rem # Date     : 2020 07.30
rem # MDate    : 2020 09.22
rem #==========================================================================

rem ## setting variables
set v_prod=visualpython
set v_option=%1
for /f "delims=, tokens=1*" %%i in ('pip show %v_prod% 2^>^&1 ^| find "Location"') do (
set v_1=%%i)
set v_path1=%v_1:~10%
set v_str1=jupyter nbextension
set v_str2=%v_prod%/src/main
set v_srch=pip search %v_prod%
set v_upgr=pip install %v_prod% --upgrade
set v_unst=pip uninstall %v_prod%
rem ## check env & set path2
where /q conda-env
IF ERRORLEVEL 1 (
    ECHO.
    ECHO Not a conda env.
    set v_path2=%APPDATA%\jupyter\nbextensions\
) ELSE (
    ECHO.
    ECHO conda env.
        set v_path2=%v_path1:~,-18%\share\jupyter\nbextensions\
)

rem ## Main Block
:l_main
IF /i "%v_option%"=="" goto :l_help
for %%i in (-h help)       do if /i %v_option% == %%i call :l_help
for %%i in (-e enable)     do if /i %v_option% == %%i call :l_enable
for %%i in (-d disable)    do if /i %v_option% == %%i call :l_disable
for %%i in (-i install)    do if /i %v_option% == %%i call :l_install
for %%i in (-up upgrade)   do if /i %v_option% == %%i call :l_upgrade
for %%i in (-v version)    do if /i %v_option% == %%i call :l_version
rem for %%i in (-ov overwirte) do if /i %v_option% == %%i call :l_overwrite
for %%i in (-ce checkext)  do if /i %v_option% == %%i call :l_check_extension
for %%i in (-cb checkbpl)  do if /i %v_option% == %%i call :l_check_visualpython
for %%i in (-vc versioncheck)  do if /i %v_option% == %%i call :l_version_cmp
for %%i in (-un uninstall) do if /i %v_option% == %%i goto :l_uninstall
goto :eof


rem ## Function Block
:l_help
    echo.
    echo usage: visualpy option
    echo optional arguments:
    echo  -h  | help        - show this help message and exit
    echo  -e  | enable      - enable VisualPython
    echo  -d  | disable     - disable VisualPython
    echo  -i  | install     - install VisualPython extensions
    echo  -un | uninstall   - uninstall VisualPython packages
    echo  -up | upgrade     - upgrade VisualPython Package
    echo  -v  |  version    - show VisualPython current version
rem echo  -o  |  overwrite  - overwrite VisualPython extensions
rem     echo                      If you upgraded using this command
rem     echo                        "pip install %v_prod% --upgrade".
rem echo                      Then use this option
    echo.
    goto :eof

:l_check_extension
    IF NOT EXIST %v_path2% call :l_prt_extensiondir
    goto :eof

:l_check_visualpython
    IF EXIST %v_path2%%v_prod% (
            set v_flag=1
            rem goto :l_prt_visualpythondir
        ) ELSE (
                set v_flag=2
            rem goto :l_prt_notexists_visualpythondir
        )
    goto :eof

:l_install
        IF EXIST %v_path2%%v_prod% ( rem echo "a"
                                     echo.
                                     echo installed %v_prod% Path :
                                     echo %v_path2%%v_prod%
                                     goto :l_prt_visualpythondir
        ) ELSE ( rem echo "b"
                 call :l_copy_files
             call :l_enable
        )
    goto :eof

:l_enable
    call :l_prt_be_line
    %v_str1% enable %v_str2%
    call :l_prt_af_line
    goto :eof

:l_disable
    call :l_prt_be_line
    %v_str1% disable %v_str2%
    call :l_prt_af_line
    goto :eof

:l_overwrite
    rem if visaulpython 없는경우 install로 수행
    rem else remove & install
        IF EXIST %v_path2%%v_prod% (
            call :l_disable
                call :l_remove_files
                call :l_copy_files
            call :l_enable
        ) else (
            goto :l_prt_notexists_visualpythondir
        )
    goto :eof

:l_copy_files
    call :l_prt_be_line
    rem /q not print src, trg name
    rem /y force overwrite
    rem /e copy directories (include empty directories)
        echo source : %v_path1%\%v_prod%
    xcopy /q /y /e %v_path1%\%v_prod% %v_path2%%v_prod%\
        echo target : %v_path2%%v_prod%\
        call :l_prt_af_line
    goto :eof

:l_remove_files
    call :l_prt_be_line
        echo Remove VisualPython Directories.
        rmdir /s /q %v_path2%%v_prod%
    call :l_prt_af_line
    goto :eof

:l_version_cmp
    for /f "delims=, tokens=1*" %%i in ('pip search %v_prod% 2^>^&1 ^| find "%v_prod%"') do (
    set ver_1=%%i)

    rem if change %v_prod% length then must change..
    rem echo %ver_1:~10,5%
    for /f "delims=, tokens=1*" %%i in ('pip show %v_prod% 2^>^&1 ^| find "Version"') do (
    set ver_2=%%i)
        rem echo %ver_2:~9%

        if %ver_1:~10,5% == %ver_2:~9% (
        rem    echo same
                set v_ver_flag=1
    ) else (
        rem    echo diff
                set v_ver_flag=0
        )
    goto :eof

:l_upgrade
        call :l_version_cmp
        if %v_ver_flag% == 0 (
            echo Running upgrade visualpython.
            call :l_disable
            %v_upgr%
                call :l_copy_files
                call :l_enable
        goto :eof
        ) else (
      call :l_prt_be_line
          echo Already installed last version.
          call :l_prt_af_line
        )
    goto :eof

:l_version
    call :l_prt_be_line
    for /f "delims=, tokens=1*" %%i in ('pip search %v_prod% 2^>^&1 ^| find "%v_prod%"') do (
    set ver_1=%%i)

    rem if change %v_prod% length then must change..
    echo Last release version : %ver_1:~10,5%

    for /f "delims=, tokens=1*" %%i in ('pip show %v_prod% 2^>^&1 ^| find "Version"') do (
    set ver_2=%%i)
        echo Installed version    : %ver_2:~9%
    call :l_prt_af_line
    goto :eof

:l_prt_extensiondir
    call :l_prt_be_line
    echo Nbextension not activated
        echo Plz install nbextension
    call :l_prt_af_line
    goto :eof

:l_prt_visualpythondir
    call :l_prt_be_line
    echo Already exists VisualPython.
    echo If want to overwirte then run below cmd, option
    echo.
    echo restart "visualpython" cmd, and use input option : "o"
    call :l_prt_af_line
    goto :eof

:l_prt_notexists_visualpythondir
    call :l_prt_be_line
    echo VisualPython extension not installed.
    echo.
    echo restart cmd : "visualpython -i"
    call :l_prt_af_line
    goto :eof

:l_prt_be_line
    echo.
    echo =========================================================================================
    goto :eof

:l_prt_af_line
    echo =========================================================================================
    goto :eof

:l_uninstall
    IF EXIST %v_path2%%v_prod% (
        call :l_disable
        call :l_remove_files
                echo %v_path2%%v_prod%
                call :l_prt_af_line
        %v_unst%
        rem call :l_prt_af_line
        ) else (
            call :l_prt_be_line
        echo %v_path1:~,-18%\share\jupyter\nbextensions\
                echo %v_path2%%v_prod%
                call :l_prt_af_line
                %v_unst%
                rem call :l_prt_af_line
        )


rem ## release variable
set v_option=
set v_path1=
set v_path2=
set v_str1=
set v_str2=
set v_srch=
set v_upgr=
set v_unst=
set ver_1=
set ver_2=
set v_1=
set v_2=
set v_flag=
set v_prod=
set v_ver_flag=

rem #==========================================================================
rem #End of File
rem #==========================================================================