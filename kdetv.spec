%define libname                %mklibname kdevideo 1
%define __libtoolize    /bin/true

%define compile_enable_final 0

%define kdetv_epoch 1

Summary: 		Kdetv - KDE Video4Linux Stream Capture Viewer
Name: 			kdetv
Version: 		0.8.9
Release: 		%mkrel 3
Source: 		%name-%version.tar.bz2
Group: 			Video
License: 		GPL
URL: 			http://www.kwintv.org/
BuildRoot: 		%_tmppath/%name-%version
Patch1:			kdetv-0.8.0-fix-install.patch
Patch2:			kdetv-0.8.4-lib64.patch
Patch3:			kdetv-0.8.7-simd.patch
Patch4:			kdetv-0.8.9-auto26.patch

BuildRequires: 		kdelibs-devel, qt3-devel, arts
BuildRequires:		jpeg-devel, png-devel, kdebase-devel 
Buildrequires:		arts-devel, libMesaGLU-devel
BuildRequires:		libxxf86dga-devel, libxt-devel, libxv-devel
Requires: 		arts
# (nl)  maybe it should be better to only require kdebase-common
Requires:               kdebase
Requires:		%libname = %kdetv_epoch:%version-%release 
Obsoletes:		kwintv


%description
Kdetv allows you to watch TV in a window on your PC screen.
It has more or less the same abilities as xawtv
but it is is based on Qt and integrated in KDE.


%package -n %libname
Summary:    kdevideo libraries
Group:      System/Libraries
Epoch:      %kdetv_epoch
License:    LGPL
Obsoletes:	libqtvision1

%description -n %libname
These libraries provide TV support to KDE.


%package -n %{libname}-devel
Summary:    kdevideo libraries
Group:      Development/KDE and Qt
Epoch:      %kdetv_epoch
License:    LGPL
Requires:   %libname = %{kdetv_epoch}:%version-%release
Obsoletes:	libqtvision1-devel


%description -n %{libname}-devel
These're the files needed to develop applications that use qtvision libraries.


%prep
rm -rf $RPM_BUILD_ROOT

%setup -q -n%name-%version
%patch2 -p1 -b .lib64
%patch3 -p1 -b .simd-flags
%patch4 -p1 -b .auto26

%build
make -f admin/Makefile.common
export QTDIR=%_prefix/lib/qt3
export KDEDIR=%_prefix
export LD_LIBRARY_PATH=$QTDIR/%_lib:$KDEDIR/%_lib:$LD_LIBRARY_PATH
export PATH=$QTDIR/bin:$KDEDIR/bin:$PATH

CFLAGS="%optflags" CXXFLAGS="%optflags" \
	%configure  --disable-rpath \
%if "%{_lib}" != "lib"
				--enable-libsuffix="%(A=%{_lib}; echo ${A/lib/})" \
%endif
%if %compile_enable_final
				--enable-final \
%endif
        		--disable-debug 


%make

%install
%makeinstall 

#rm -rf $RPM_BUILD_ROOT/%_docdir/libqtvision1-0.8.0/COPYING
#rm -rf $RPM_BUILD_ROOT/%_docdir/libqtvision1-devel-0.8.0/COPYING

install -d $RPM_BUILD_ROOT%{_menudir}
kdedesktop2mdkmenu.pl %{name} "Multimedia/Video" $RPM_BUILD_ROOT%{_datadir}/applnk/Multimedia/kdetv.desktop $RPM_BUILD_ROOT%{_menudir}/%{name} 

chmod 4755 %buildroot/%_bindir/kdetvv4lsetup


# Dynamic desktop support
%define launchers /etc/dynamic/launchers/tvtuner
mkdir -p $RPM_BUILD_ROOT%launchers
cat > $RPM_BUILD_ROOT%launchers/%name.desktop << EOF
[Desktop Entry]
Name=KdeTv \$devicename
Comment=Kdetv
Exec=%_bindir/kdetv
Terminal=false
Icon=kdetv.png
Type=Application
EOF

%find_lang %name --with-html

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_menus
update-alternatives --install %{launchers}/kde.desktop tvtuner.kde.dynamic %launchers/%name.desktop 31
update-alternatives --install %{launchers}/gnome.desktop tvtuner.gnome.dynamic %launchers/%name.desktop 29
%if %mdkversion > 200600
%update_icon_cache hicolor
%endif


%postun
%clean_menus
if [ $1 = 0 ]; then
  update-alternatives --remove tvtuner.kde.dynamic %launchers/%name.desktop
  update-alternatives --remove tvtuner.gnome.dynamic %launchers/%name.desktop
fi
%if %mdkversion > 200600
%clean_icon_cache hicolor
%endif


%post -n %libname -p /sbin/ldconfig
%postun -n %libname -p /sbin/ldconfig

%files -f %name.lang
%defattr(-,root,root)
%doc COPYING
%_bindir/kdetv

%_bindir/kdetvv4lsetup

%_menudir/*

%dir %_datadir/apps/kdetv/
%_datadir/apps/kdetv/tips

%_iconsdir/hicolor/*/apps/kdetv.png

%_datadir/apps/kdetv/*.rc

%_datadir/applnk/Multimedia/kdetv.desktop

%dir %_datadir/apps/kdetv/channels-dist/
%_datadir/apps/kdetv/channels-dist/*.list
%_datadir/apps/kdetv/channels-dist/*.map

%_datadir/apps/profiles/kdetv.profile.xml

%_datadir/services/kdetv/*.desktop

%_datadir/servicetypes/kdetv/*.desktop   

%_datadir/apps/kdetv/icons/hicolor/16x16/apps/*.png
%_datadir/apps/kdetv/icons/hicolor/22x22/actions/*.png
   
%_datadir/apps/kdetv/icons/hicolor/22x22/apps/*.png
%_datadir/apps/kdetv/icons/hicolor/32x32/apps/*.png


%dir %_docdir/HTML/da/kdetv
%doc %_docdir/HTML/da/kdetv/common
%doc %_docdir/HTML/da/kdetv/*.bz2
%doc %_docdir/HTML/da/kdetv/*.docbook

%dir %_docdir/HTML/en/kdetv
%doc %_docdir/HTML/en/kdetv/common
%doc %_docdir/HTML/en/kdetv/*.bz2
%doc %_docdir/HTML/en/kdetv/*.docbook

%dir %_docdir/HTML/et/kdetv
%doc %_docdir/HTML/et/kdetv/common
%doc %_docdir/HTML/et/kdetv/*.bz2
%doc %_docdir/HTML/et/kdetv/*.docbook

%dir %_docdir/HTML/fr/kdetv
%doc %_docdir/HTML/fr/kdetv/common
%doc %_docdir/HTML/fr/kdetv/*.bz2
%doc %_docdir/HTML/fr/kdetv/*.docbook

%dir %_docdir/HTML/it/kdetv
%doc %_docdir/HTML/it/kdetv/common
%doc %_docdir/HTML/it/kdetv/*.bz2
%doc %_docdir/HTML/it/kdetv/*.docbook

%dir %_docdir/HTML/nl/kdetv
%doc %_docdir/HTML/nl/kdetv/common
%doc %_docdir/HTML/nl/kdetv/*.bz2
%doc %_docdir/HTML/nl/kdetv/*.docbook

%dir %_docdir/HTML/pt/kdetv
%doc %_docdir/HTML/pt/kdetv/common
%doc %_docdir/HTML/pt/kdetv/*.bz2
%doc %_docdir/HTML/pt/kdetv/*.docbook

%dir %_docdir/HTML/ru/kdetv
%doc %_docdir/HTML/ru/kdetv/common
%doc %_docdir/HTML/ru/kdetv/*.bz2
%doc %_docdir/HTML/ru/kdetv/*.docbook

%dir %_docdir/HTML/sv/kdetv
%doc %_docdir/HTML/sv/kdetv/common
%doc %_docdir/HTML/sv/kdetv/*.bz2
%doc %_docdir/HTML/sv/kdetv/*.docbook


%config(noreplace) %launchers/%name.desktop

%files -n %libname
%defattr(-,root,root)
%doc COPYING
%_libdir/kde3/*.la
%_libdir/kde3/*.so

%_libdir/*.la
%_libdir/*.so.*


%files -n %{libname}-devel
%defattr(-,root,root)
%doc COPYING
%_libdir/*.so


