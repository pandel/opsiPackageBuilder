md docs
sphinx-apidoc -M -f -e -o "docs/source" "oPB"
cd docs
call make.bat html
cd ..
pause