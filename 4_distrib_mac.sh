pyinstaller --noconfirm  --windowed pyinstaller-mac.spec
rm -R -f dist/helpviewer
rm -R -f dist/opsipackagebuilder
cp images/prog_icons/mac/help.icns dist/opbHelpViewer.app/Contents/Resources/icon-windowed.icns
cp images/prog_icons/mac/opsipackagebuilder.icns dist/opsiPackageBuilder.app/Contents/Resources/icon-windowed.icns
