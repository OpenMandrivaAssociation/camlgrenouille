%define name camlgrenouille

%define version 1.28
%define release 6

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

BuildRoot:      %_tmppath/%name-buildroot

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

%if %mdkversion < 200900
%post
%{update_menus}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README TODO
%doc script_demarrage.sh
%_bindir/*
%config(noreplace) %_sysconfdir/*
%{_datadir}/applications/mandriva-%{name}.desktop
%_miconsdir/%name.png
%_iconsdir/%name.png
%_liconsdir/%name.png




%changelog
* Thu Dec 09 2010 Oden Eriksson <oeriksson@mandriva.com> 1.28-5mdv2011.0
+ Revision: 616912
- the mass rebuild of 2010.0 packages

* Wed Sep 02 2009 Thierry Vignaud <tv@mandriva.org> 1.28-4mdv2010.0
+ Revision: 424743
- rebuild

* Wed Jul 23 2008 Thierry Vignaud <tv@mandriva.org> 1.28-3mdv2009.0
+ Revision: 243427
- rebuild
- drop old menu
- kill re-definition of %%buildroot on Pixel's request

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Wed Nov 28 2007 Guillaume Bedot <littletux@mandriva.org> 1.28-1mdv2008.1
+ Revision: 113560
- 1.28

  + Thierry Vignaud <tv@mandriva.org>
    - kill desktop-file-validate's error: string list key "Categories" in group "Desktop Entry" does not have a semicolon (";") as trailing character


* Fri Aug 04 2006 Olivier Thauvin <nanardon@mandriva.org>
+ 08/04/06 21:27:07 (52907)
- xdg menu

* Fri Aug 04 2006 Olivier Thauvin <nanardon@mandriva.org>
+ 08/04/06 21:22:20 (52902)
Import camlgrenouille

* Fri May 05 2006 Guillaume Bedot <littletux@mandriva.org> 1.27-1mdk
- Release 1.27
- Update URL
- Fix plugin path in config
- Fix menu
- Other fixes

* Wed May 18 2005 Nicolas Lécureuil <neoclust@mandriva.org> 1.13-1mdk
- 1.13
- Update Source

* Tue Mar 22 2005 Olivier Thauvin <nanardon@mandrake.org> 1.11-1mdk
- 1.11
- update url

* Thu Feb 12 2004 David Baudens <baudens@mandrakesoft.com> 1.10-6mdk
- Fix menu

* Wed Feb 11 2004 David Baudens <baudens@mandrakesoft.com> 1.10-5mdk
- Fix menu

* Tue Oct 28 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 1.10-4mdk
- Requires s/xvt/rxvt/ until xvt package or ptovides does not exists

* Tue Oct 28 2003 Pascal Terjan <CMoi@tuxfamily.org> 1.10-3mdk
- Remove dependency on ocaml (not needed at runtime)
- Replace xterm by xvt

* Tue Sep 30 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 1.10-2mdk
- From: Julien Catalano <julien.catalano@free.fr>
    - Fix grenouille shell script (adding $*);
    - Add README.mdk to help Mandrake Linux user to configure and run easily Camlgrenouille.

* Sun Sep 14 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 1.10-1mdk
- From Julien Catalano <julien.catalano@free.fr>
	- Creating RPM for Mandrake Linux.

