%define name camlgrenouille

%define version 1.28
%define release %mkrel 1

%define title   Camlgrenouille
%define longtitle Broadband connection test program

Summary:        %longtitle
Name:           %name
Version:        %version
Release:        %release
License:        GPL
Group:          Networking/Other
Url:		http://devel.grenouille.com/Camlgrenouille.php

Source0:        http://devel.grenouille.com/pub/camlgrenouille/sources/%{name}-%{version}.tar.gz
# Make 3 icons %name-{16,32,48}.png and then tar cjf %name-icons.tar.bz2 *png
Source1:        %name-icons.tar.bz2
Source2:	%name-missing-files.tar.bz2


Buildrequires: ocaml
Requires: rxvt

%description
This software is meant to test for your broadband connection,
and sends the results to www.grenouille.com

%prep
rm -rf $RPM_BUILD_ROOT
#unpack source, icons and missing files:
%setup -q -b2 -a1 -n %{name}-%{version}

%build
touch build_linux
make depend
make

%install
#installation des executables
mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -D -m 755 %{name} $RPM_BUILD_ROOT%{_bindir}/%{name}
install -D -m 755 camlgrenouille $RPM_BUILD_ROOT%{_bindir}/camlgrenouille
(cd $RPM_BUILD_ROOT%{_bindir}
 ln -s camlgrenouille grenouille )

#patch config
perl -pi -e 's#\./shell_ifconfig.sh#%{_sysconfdir}/%{name}/shell_ifconfig.sh#' user.config.linux

#installation des fichiers de config
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
install -D -m 644 user.config.linux $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/user.config
install -D -m 755 shell_ifconfig.sh $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/shell_ifconfig.sh

# icon
mkdir -p $RPM_BUILD_ROOT{%{_liconsdir},%{_iconsdir},%{_miconsdir}}
install -D -m 644 %{name}-48.png $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png
install -D -m 644 %{name}-32.png $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
install -D -m 644 %{name}-16.png $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png

# Menu
# Every entry must be changed according package specfications
# Pay attention to "section" "command" and "longtitle"
mkdir -p $RPM_BUILD_ROOT%{_menudir}
cat > $RPM_BUILD_ROOT%{_menudir}/%{name} << EOF
?package(%name): \
command="%{_bindir}/%{name} -f %{_sysconfdir}/%{name}/user.config" \
needs="text" \
icon="%{name}.png" \
section="Internet/Other" \
title="%{title}" \
longtitle="%{longtitle}" \
xdg="true"
EOF

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=%{title}
Comment=%{longtitle}
Exec=%{_bindir}/%{name} 
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=X-MandrivaLinux-Internet;
EOF

%post
%{update_menus}

%postun
%{clean_menus}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README TODO
%doc script_demarrage.sh
%_bindir/*
%config(noreplace) %_sysconfdir/*
%_menudir/%name
%{_datadir}/applications/mandriva-%{name}.desktop
%_miconsdir/%name.png
%_iconsdir/%name.png
%_liconsdir/%name.png


