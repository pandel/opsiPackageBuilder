pyinstaller --noconfirm  pyinstaller-linux.spec
cp dist/helpviewer/helpviewer dist/opsipackagebuilder
chmod -x dist/opsipackagebuilder/*.so*
chmod -x dist/opsipackagebuilder/qt5_plugins/bearer/*.so*
chmod -x dist/opsipackagebuilder/qt5_plugins/iconengines/*.so*
chmod -x dist/opsipackagebuilder/qt5_plugins/imageformats/*.so*
chmod -x dist/opsipackagebuilder/qt5_plugins/platforms/*.so*
chmod -x dist/opsipackagebuilder/qt5_plugins/sqldrivers/*.so*
chmod -x dist/opsipackagebuilder/*.so*
chmod 777 dist/opsipackagebuilder/help
chmod 666 dist/opsipackagebuilder/help/opsipackagebuilder.qhc
rm -R -f dist/helpviewer
