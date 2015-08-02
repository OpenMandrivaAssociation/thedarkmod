%define debug_package	%{nil}
%define name thedarkmod
%define version 2.03
%define release 1
ExclusiveArch: %{ix86}


Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary:        Steampunk Stealth Game
License:        GPLv3 and CC-BY-SA
Group:          Games/Arcade
Url:            http://www.thedarkmod.com/
Source0:        http://www.thedarkmod.com/sources/%{name}.%{version}.src.7z
Source1:        thedarkmod.rpmlintrc
Source3:        thedarkmod
Source4:        thedarkmod.png
Source5:        thedarkmod.desktop


BuildRequires:  libboost-devel
BuildRequires:  glibc-devel
BuildRequires:  hicolor-icon-theme
BuildRequires:  jpeg-devel
BuildRequires:  libtinyxml-devel
BuildRequires:  pkgconfig(alsa)
BuildRequires:  bzip2-devel
BuildRequires:  freetype2-devel
BuildRequires:  pkgconfig(glew)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(IL)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libssl)
BuildRequires:  pkgconfig(openal)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xxf86vm)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  p7zip
BuildRequires:  scons
BuildRequires:  zip
BuildRequires:  desktop-file-utils

Requires:       xterm
Requires:       opengl-games-utils
Requires:       libpng12.so.0

%description
A first-person stealth game. In it you play a hooded figure
slinking through the shadows of a gothic steampunk city,
hunting priceless valuables while avoiding the swords and
arrows of those hired to stop you.

%prep
%setup -qc %{name}-%{version}
cat README.urpmi << EOF
=============================================
The default resolution is lame , to change it 
according to your screen resolution, edit the 
config file in $HOME/.doom/thedarkmod and set 
width=your_screen_width
height=your_screen_height.
The Data pk file are installed at install time,
according to your bandwith, wil take some time.
Brought to you by:
Symbianflo 
MandrivaUsers.Ro Rosalinux.Ro
MRB ain't no shit
==============================================
EOF

%build
touch scons.signatures.dblite
%scons  BUILD_GAMEPAK=1 NO_GCH=0 BUILD=release --debug=explain

pushd tdm_update
	scons -c
	scons BUILD="release"
popd

%install
mkdir -p %{buildroot}%{_libdir}/thedarkmod/
mv thedarkmod.x86 %{buildroot}%{_libdir}/thedarkmod/
mv gamex86-base.so %{buildroot}%{_libdir}/thedarkmod/gamex86.so
mv tdm_game02.pk4 %{buildroot}%{_libdir}/thedarkmod/

# wrapper
mkdir -p %{buildroot}%{_bindir}
install -m0755 %{SOURCE3} %{buildroot}%{_bindir}

install -m0755 tdm_update/tdm_update.linux %{buildroot}%{_libdir}/thedarkmod/

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/
install -m0644 %{SOURCE4} %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/

mkdir -p %{buildroot}%{_datadir}/applications/
install -m0644 %{SOURCE5} %{buildroot}%{_datadir}/applications/

desktop-file-validate %{buildroot}%{_datadir}/applications/thedarkmod.desktop

%post
# updating and install the pk files 
cd /usr/lib/thedarkmod
./tdm_update.linux && rm -f TheDarkMod.exe tdm_update.exe

%postun
rm -fr /usr/lib/thedarkmod

%files
%doc COPYING.txt LICENSE.txt README.txt README.urpmi
%{_bindir}/thedarkmod
%{_libdir}/thedarkmod
%{_datadir}/applications/thedarkmod.desktop
%{_datadir}/icons/hicolor/64x64/apps/thedarkmod.png
