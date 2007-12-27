%define major		1
%define libname		%mklibname kdevideo %{major}
%define develname	%mklibname kdevideo -d

%define compile_enable_final 0

%define kdetv_epoch 1

Summary: 		TV viewer for KDE
Name: 			kdetv
Version: 		0.8.9
Release: 		%mkrel 5
Source: 		%{name}-%{version}.tar.bz2
Group: 			Video
License: 		GPLv2+
URL: 			http://www.kde-apps.org/content/show.php?content=11602
Patch1:			kdetv-0.8.4-lib64.patch
Patch2:			kdetv-0.8.7-simd.patch
Patch3:			kdetv-0.8.9-auto26.patch
BuildRequires: 		kdelibs-devel
BuildRequires:		qt3-devel
BuildRequires:		arts
BuildRequires:		jpeg-devel
BuildRequires:		png-devel
BuildRequires:		kdebase-devel 
Buildrequires:		arts-devel
BuildRequires:		libMesaGLU-devel
BuildRequires:		libxxf86dga-devel
BuildRequires:		libxt-devel
BuildRequires:		libxv-devel
BuildRequires:		desktop-file-utils
Requires: 		arts
# (nl)  maybe it should be better to only require kdebase-common
Requires:               kdebase
Requires:		%{libname} = %{kdetv_epoch}:%{version}-%{release} 
Obsoletes:		kwintv


%description
Kdetv allows you to watch TV in a window on your PC screen.
It has more or less the same abilities as xawtv
but it is is based on Qt and integrated in KDE.


%package -n %{libname}
Summary:		kdevideo libraries
Group:			System/Libraries
Epoch:			%{kdetv_epoch}
License:		LGPLv2+

%description -n %{libname}
These libraries provide TV support to KDE.


%package -n %{develname}
Summary:		kdevideo libraries
Group:			Development/KDE and Qt
Epoch:			%{kdetv_epoch}
License:		LGPLv2+
Requires:		%{libname} = %{kdetv_epoch}:%{version}-%{release}
Obsoletes:		%{mklibname kdevideo 1 -d}

%description -n %{develname}
These are the files needed to develop applications that use qtvision
libraries.


%prep
rm -rf %{buildroot}

%setup -q
%patch1 -p1 -b .lib64
%patch2 -p1 -b .simd-flags
%patch3 -p1 -b .auto26

%build
make -f admin/Makefile.common
export QTDIR=%{qt3dir}
export KDEDIR=%{_prefix}
export LD_LIBRARY_PATH=$QTDIR/%{_lib}:$KDEDIR/%{_lib}:$LD_LIBRARY_PATH
export PATH=$QTDIR/bin:$KDEDIR/bin:$PATH

CFLAGS="%optflags" CXXFLAGS="%optflags" \
	%configure2_5x  --disable-rpath \
%if "%{_lib}" != "lib"
				--enable-libsuffix="%(A=%{_lib}; echo ${A/lib/})" \
%endif
%if %compile_enable_final
				--enable-final \
%endif
        		--disable-debug 

%make

%install
%makeinstall_std

chmod 4755 %buildroot/%{_bindir}/kdetvv4lsetup

# Dynamic desktop support
%define launchers /etc/dynamic/launchers/tvtuner
mkdir -p %{buildroot}%{launchers}
cat > %{buildroot}%{launchers}/%{name}.desktop << EOF
[Desktop Entry]
Name=KdeTv \$devicename
Comment=Kdetv
Exec=%{_bindir}/kdetv
Terminal=false
Icon=kdetv
Type=Application
EOF

mkdir -p %{buildroot}%{_datadir}/applications/kde
desktop-file-install --vendor='' --delete-original \
  --remove-key="Encoding" \
  --remove-category="Multimedia" \
  --remove-category="QT" \
  --add-category="Qt" \
  --dir %{buildroot}%{_datadir}/applications/kde/ %{buildroot}%{_datadir}/applnk/Multimedia/kdetv.desktop

%find_lang %{name} --with-html

%clean
rm -rf %{buildroot}

%post
%{update_menus}
update-alternatives --install %{launchers}/kde.desktop tvtuner.kde.dynamic %{launchers}/%{name}.desktop 31
update-alternatives --install %{launchers}/gnome.desktop tvtuner.gnome.dynamic %{launchers}/%{name}.desktop 29
%{update_icon_cache hicolor}

%postun
%clean_menus
if [ $1 = 0 ]; then
  update-alternatives --remove tvtuner.kde.dynamic %{launchers}/%{name}.desktop
  update-alternatives --remove tvtuner.gnome.dynamic %{launchers}/%{name}.desktop
fi
%{clean_icon_cache hicolor}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/kdetv

%{_bindir}/kdetvv4lsetup

%dir %{_datadir}/apps/kdetv/
%{_datadir}/apps/kdetv/tips

%{_iconsdir}/hicolor/*/apps/kdetv.png

%{_datadir}/apps/kdetv/*.rc

%{_datadir}/applications/kde/%{name}.desktop

%dir %{_datadir}/apps/kdetv/channels-dist/
%{_datadir}/apps/kdetv/channels-dist/*.list
%{_datadir}/apps/kdetv/channels-dist/*.map

%{_datadir}/apps/profiles/kdetv.profile.xml

%{_datadir}/services/kdetv/*.desktop

%{_datadir}/servicetypes/kdetv/*.desktop   

%{_datadir}/apps/kdetv/icons/hicolor/16x16/apps/*.png
%{_datadir}/apps/kdetv/icons/hicolor/22x22/actions/*.png
   
%{_datadir}/apps/kdetv/icons/hicolor/22x22/apps/*.png
%{_datadir}/apps/kdetv/icons/hicolor/32x32/apps/*.png


%config(noreplace) %{launchers}/%{name}.desktop

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/kde3/*.la
%{_libdir}/kde3/*.so

%{_libdir}/*.la
%{_libdir}/*.so.*


%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/*.so
