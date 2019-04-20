%define _userunitdir /usr/lib/systemd/user/

%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

Name:		gamemode
Version:	1.3.1
Release:	1
Summary:	Optimize system performance for games on demand
License:	BSD
URL:		https://github.com/FeralInteractive/gamemode
Source0:	%{url}/releases/download/%{version}/%{name}-%{version}.tar.xz

BuildRequires: gcc
BuildRequires: asciidoc
BuildRequires: meson
BuildRequires: pkgconfig(systemd)
BuildRequires: pkgconfig(libsystemd)
#BuildRequires: polkit-devel
BuildRequires: systemd

Requires:       %{libname} = %{version}-%{release}

%description
GameMode is a daemon/lib combo for GNU/Linux that allows games to
request a set of optimizations be temporarily applied to the host OS.
GameMode was designed primarily as a stop-gap solution to problems
with the Intel and AMD CPU "powersave" or "ondemand" governors, but
is now able to launch custom user defined plugins, and is intended
to be expanded further, as there are a wealth of automation tasks
one might want to apply.

HOW TO USE:
After installing libgamemodeauto.so.0 simply preload it into the game:
LD_PRELOAD=/usr/\$LIB/libgamemodeauto.so.0 ./game
Or edit the steam launch options:
LD_PRELOAD=$LD_PRELOAD:/usr/\$LIB/libgamemodeauto.so.0 %command%
Please note the backslash here in \$LIB is required.

%package -n %{libname}
Summary:       Library files for GameMode
Group:         System/Libraries
Requires:      %{name} = %{version}-%{release}

%description -n %{libname}
Library files for GameMode.

%package devel
Summary: Development package for %{name}
Requires: %{libname} = %{version}-%{release}

%description devel
Files for development with %{name}.

%prep
%setup -q

%build
%meson
%meson_build

%check
%meson_test

%install
%meson_install


%files
%license LICENSE.txt
%doc	 README.md
%{_bindir}/gamemoded
%{_libexecdir}/cpugovctl
%{_datadir}/polkit-1/actions/com.feralinteractive.GameMode.policy
%{_datadir}/dbus-1/services/com.feralinteractive.GameMode.service
#{_libdir}/libgamemode*.so.*
#{_libdir}/systemd/user/gamemoded.service
%{_userunitdir}/gamemoded.service
%{_mandir}/man8/gamemoded.8*

%files -n %{libname}
%{_libdir}/lib%{name}.so*
%{_libdir}/lib%{name}auto.so*

%files devel
%{_includedir}/gamemode_client.h
%{_libdir}/libgamemode*.so
%{_libdir}/pkgconfig/gamemode*.pc
