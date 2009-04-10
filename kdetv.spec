%define major		1
%define libname		%mklibname kdevideo %{major}
%define develname	%mklibname kdevideo -d

%define compile_enable_final 0
%define launchers /etc/dynamic/launchers/tvtuner
%define kdetv_epoch 1

Summary: 		TV viewer for KDE
Name: 			kdetv
Version: 		0.8.9
Release: 		%mkrel 7
Source: 		%{name}-%{version}.tar.bz2
Group: 			Video
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
License: 		GPLv2+
URL: 			http://www.kde-apps.org/content/show.php?content=11602
Patch1:			kdetv-0.8.4-lib64.patch
Patch2:			kdetv-0.8.9-simd.patch
Patch3:			kdetv-0.8.9-auto26.patch
BuildRequires:		kdebase3-devel 
BuildRequires:		mesaglu-devel
BuildRequires:		libxxf86dga-devel
BuildRequires:		libxt-devel
BuildRequires:		libxv-devel
BuildRequires:		desktop-file-utils
BuildRequires:          zvbi-devel
Requires: 		arts
Requires:               kdebase-progs
Requires:		%{libname} = %{kdetv_epoch}:%{version}-%{release} 
Obsoletes:		kwintv


%description
Kdetv allows you to watch TV in a window on your PC screen.
It has more or less the same abilities as xawtv
but it is is based on Qt and integrated in KDE.


%post
%if %mdkversion < 200900
%{update_menus}
%endif
update-alternatives --install %{launchers}/kde.desktop tvtuner.kde.dynamic %{launchers}/%{name}.desktop 31
update-alternatives --install %{launchers}/gnome.desktop tvtuner.gnome.dynamic %{launchers}/%{name}.desktop 29
%if %mdkversion < 200900
%{update_icon_cache hicolor}
%endif

%postun
%if %mdkversion < 200900
%clean_menus
%endif
if [ $1 = 0 ]; then
  update-alternatives --remove tvtuner.kde.dynamic %{launchers}/%{name}.desktop
  update-alternatives --remove tvtuner.gnome.dynamic %{launchers}/%{name}.desktop
fi
%if %mdkversion < 200900
%{clean_icon_cache hicolor}
%endif

%files -f %{name}.lang
%defattr(-,root,root)
%{_kde3_bindir}/kdetv
%{_kde3_bindir}/kdetvv4lsetup
%{_kde3_datadir}/apps/kdetv
%{_kde3_iconsdir}/hicolor/*/apps/kdetv.png
%{_kde3_datadir}/applications/kde/%{name}.desktop
%{_kde3_datadir}/apps/profiles/kdetv.profile.xml
%{_kde3_datadir}/services/kdetv/*.desktop
%{_kde3_datadir}/servicetypes/kdetv/*.desktop
%config(noreplace) %{launchers}/%{name}.desktop

#--------------------------------------------------------------------

%package -n %{libname}
Summary:		Kdevideo libraries
Group:			System/Libraries
Epoch:			%{kdetv_epoch}
License:		LGPLv2+

%description -n %{libname}
These libraries provide TV support to KDE.

%files -n %{libname}
%defattr(-,root,root)
%{_kde3_libdir}/kde3/*.la
%{_kde3_libdir}/kde3/*.so
%{_kde3_libdir}/*.so.*

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

#--------------------------------------------------------------------

%package -n %{develname}
Summary:		Kdevideo libraries
Group:			Development/KDE and Qt
Epoch:			%{kdetv_epoch}
License:		LGPLv2+
Requires:		%{libname} = %{kdetv_epoch}:%{version}-%{release}
Obsoletes:		%{mklibname kdevideo 1 -d}

%description -n %{develname}
These are the files needed to develop applications that use qtvision
libraries.

%files -n %{develname}
%defattr(-,root,root)
%{_kde3_libdir}/*.so
%{_kde3_libdir}/*.la

#--------------------------------------------------------------------

%prep
%setup -q
%patch1 -p1 -b .lib64
%patch2 -p1 -b .simd-flags
%patch3 -p1 -b .auto26

%build
make -f admin/Makefile.common
%configure_kde3
%make

%install
rm -fr %buildroot
%makeinstall_std

chmod 4755 %buildroot/%{_kde3_bindir}/kdetvv4lsetup

# Dynamic desktop support
mkdir -p %{buildroot}%{launchers}
cat > %{buildroot}%{launchers}/%{name}.desktop << EOF
[Desktop Entry]
Name=KdeTv \$devicename
Comment=Kdetv
Exec=%{_kde3_bindir}/kdetv
Terminal=false
Icon=kdetv
Type=Application
EOF

mkdir -p %{buildroot}%{_kde3_datadir}/applications/kde
desktop-file-install --vendor='' --delete-original \
  --remove-key="Encoding" \
  --remove-category="Multimedia" \
  --remove-category="QT" \
  --add-category="Qt" \
  --dir %{buildroot}%{_kde3_datadir}/applications/kde/ %{buildroot}%{_kde3_datadir}/applnk/Multimedia/kdetv.desktop

%find_lang %{name} --with-html

%clean
rm -rf %{buildroot}
