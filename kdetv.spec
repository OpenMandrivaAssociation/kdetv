%define major		1
%define libname		%mklibname kdevideo %{major}
%define develname	%mklibname kdevideo -d

%define compile_enable_final 0
%define launchers /etc/dynamic/launchers/tvtuner

%define svn     986125

Summary: 		TV viewer for KDE
Name: 			kdetv
Version: 		0.9.0
Release: 		%mkrel 0.%svn.2
Epoch:          1
Source: 		%{name}-%{version}.%svn.tar.bz2
Group: 			Video
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
License: 		GPLv2+
URL: 			https://www.kde-apps.org/content/show.php?content=11602
BuildRequires:	kdebase4-devel 
BuildRequires:	mesaglu-devel
BuildRequires:	libxxf86dga-devel
BuildRequires:	libxt-devel
BuildRequires:	libxv-devel
BuildRequires:	desktop-file-utils
BuildRequires:  zvbi-devel
Requires:       kdebase4-runtime
Obsoletes:		kwintv

%description
Kdetv allows you to watch TV in a window on your PC screen.
It has more or less the same abilities as xawtv
but it is is based on Qt and integrated in KDE.

%post
update-alternatives --install %{launchers}/kde.desktop tvtuner.kde.dynamic %{launchers}/%{name}.desktop 31
update-alternatives --install %{launchers}/gnome.desktop tvtuner.gnome.dynamic %{launchers}/%{name}.desktop 29

%postun
if [ $1 = 0 ]; then
  update-alternatives --remove tvtuner.kde.dynamic %{launchers}/%{name}.desktop
  update-alternatives --remove tvtuner.gnome.dynamic %{launchers}/%{name}.desktop
fi

%files 
%defattr(-,root,root)
%{_kde_bindir}/kdetv
%{_kde_bindir}/kdetvv4lsetup
%{_kde_datadir}/apps/kdetv
%{_kde_iconsdir}/hicolor/*/*/*.png
%{_kde_datadir}/applications/kde4/%{name}.desktop
%{_kde_datadir}/apps/profiles/kdetv.profile.xml
%{_kde_datadir}/kde4/services/kdetv/*.desktop
%{_kde_datadir}/kde4/servicetypes/kdetv/*.desktop
%config(noreplace) %{launchers}/%{name}.desktop
%{_kde_libdir}/kde4/kdetv_*
%{_kde_libdir}/kde4/libzvbidecoder.so

#------------------------------------------------   

%define kdetvvideo_major 1
%define libkdetvvideo %mklibname kdetvvideo %kdetvvideo_major

%package -n %libkdetvvideo
Summary: KDE 4 core library
Group: System/Libraries
Obsoletes: %{_lib}kdevideo1 < 1:0.9.0-0.986125.2

%description -n %libkdetvvideo
KDE 4 core library.

%files -n %libkdetvvideo
%defattr(-,root,root)
%_kde_libdir/libkdetvvideo.so.%{kdetvvideo_major}*

#------------------------------------------------   

%define libkdetv_major 1
%define liblibkdetv %mklibname libkdetv %libkdetv_major

%package -n %liblibkdetv
Summary: KDE 4 core library
Group: System/Libraries

%description -n %liblibkdetv
KDE 4 core library.

%files -n %liblibkdetv
%defattr(-,root,root)
%_kde_libdir/liblibkdetv.so.%{libkdetv_major}*

#------------------------------------------------

%package -n %{develname}
Summary:		Kdevideo libraries
Group:			Development/KDE and Qt
License:		LGPLv2+
Requires:		%{libkdetvvideo} = %{epoch}:%{version}-%{release}
Requires:       %{liblibkdetv} = %{epoch}:%{version}-%{release}
Obsoletes:		%{mklibname kdevideo 1 -d}

%description -n %{develname}
These are the files needed to develop applications that use qtvision
libraries.

%files -n %{develname}
%defattr(-,root,root)
%{_kde_libdir}/*.so
%{_kde_libdir}/libkvideoio.a

#--------------------------------------------------------------------

%prep
%setup -q -n %name

%build
%cmake_kde4
%make

%install
cd build
rm -fr %buildroot
%makeinstall_std

chmod 4755 %buildroot/%{_kde_bindir}/kdetvv4lsetup

# Dynamic desktop support
mkdir -p %{buildroot}%{launchers}
cat > %{buildroot}%{launchers}/%{name}.desktop << EOF
[Desktop Entry]
Name=KdeTv \$devicename
Comment=Kdetv
Exec=%{_kde_bindir}/kdetv
Terminal=false
Icon=kdetv
Type=Application
EOF

%check
for f in %{buildroot}%{_kde_datadir}/applications/kde4/*.desktop ; do
     desktop-file-validate $f
done 

%clean
rm -rf %{buildroot}
