pyinstaller --noconfirm  pyinstaller-linux.spec
cp dist/helpviewer/helpviewer dist/opsipackagebuilder
rm -R -f dist/helpviewer