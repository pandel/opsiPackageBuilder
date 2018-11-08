call workon oPB

md docs
%USERPROFILE%\Envs\oPB\Scripts\sphinx-apidoc -M -f -e -o "docs/source" "oPB"
cd docs
call make.bat clean
rem call make.bat epub
rem call make.bat html
call make.bat qthelp

%USERPROFILE%\Envs\oPB\Lib\site-packages\pyqt5_tools\qcollectiongenerator build\qthelp\opsipackagebuilder.qhcp

move build\qthelp\opsipackagebuilder.qch ..\oPB\help
move build\qthelp\opsipackagebuilder.qhc ..\oPB\help

cd ..

%USERPROFILE%\Envs\oPB\Lib\site-packages\pyqt5_tools\assistant -collectionFile oPB\help\opsipackagebuilder.qhc

