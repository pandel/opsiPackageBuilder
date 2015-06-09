md docs
sphinx-apidoc -M -f -e -o "docs/source" "oPB"
cd docs
call make.bat clean
call make.bat html
call make.bat qthelp

qcollectiongenerator build\qthelp\opsipackagebuilder.qhcp

move build\qthelp\opsipackagebuilder.qch ..\oPB\help
move build\qthelp\opsipackagebuilder.qhc ..\oPB\help

cd ..

assistant -collectionFile oPB\help\opsipackagebuilder.qhc
