mkdir docs
sphinx-apidoc -M -f -e -o "docs/source" "oPB"
cd docs
make html
make qthelp
qcollectiongenerator build/qthelp/opsipackagebuilder.qhcp
mv build/qthelp/opsipackagebuilder.qch ../oPB/help
mv build/qthelp/opsipackagebuilder.qhc ../oPB/help

# assistant -collectionFile ../oPB/help/opsipackagebuilder.qhc
cd ..
