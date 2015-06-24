pyinstaller --noconfirm  pyinstaller-linux.spec
cp dist/helpviewer/helpviewer dist/opsipackagebuilder
chmod -x dist/opsipackagebuilder/*.so*
chmod 777 dist/opsipackagebuilder/help
chmod 666 dist/opsipackagebuilder/help/opsipackagebuilder.qhc
rm -R -f dist/helpviewer
