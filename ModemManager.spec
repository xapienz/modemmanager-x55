%define snapshot .git20091218

Summary: Mobile broadband modem management service
Name: ModemManager
Version: 0.2.997
Release: 4%{snapshot}%{?dist}
#
# Source from git://anongit.freedesktop.org/ModemManager/ModemManager
# tarball built with:
#    ./autogen.sh --prefix=/usr --sysconfdir=/etc --localstatedir=/var
#    make distcheck
#
Source: %{name}-%{version}%{snapshot}.tar.bz2
License: GPLv2+
Group: System Environment/Base

URL: http://www.gnome.org/projects/NetworkManager/
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires: glib2-devel
BuildRequires: dbus-glib-devel >= 0.75
BuildRequires: libgudev-devel >= 143

%description
The ModemManager service provides a consistent API to operate many different
modems, including mobile broadband (3G) devices.

%prep
%setup -q

%build
%configure \
	--enable-more-warnings=yes \
	--with-udev-base-dir=/lib/udev \
	--disable-static

make %{?_smp_mflags}

%check
make check

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(0644, root, root, 0755)
%doc COPYING README
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.ModemManager.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.ModemManager.service
%attr(0755,root,root) %{_sbindir}/modem-manager
%dir %{_libdir}/%{name}
%attr(0755,root,root) %{_libdir}/%{name}/*.so*
/lib/udev/rules.d/*

%changelog
* Fri Dec 18 2009 Dan Williams <dcbw@redhat.com> - 0.2.997-4.git20091218
- sierra: fix CDMA registration detection in some cases

* Wed Dec 16 2009 Dan Williams <dcbw@redhat.com> - 0.2.997-3.git20091216
- sierra: ensure CDMA device is powered up when trying to use it
- cdma: better signal quality parsing (fixes ex Huawei EC168C)
- zte: handle unsolicited messages better during probing

* Mon Dec 14 2009 Dan Williams <dcbw@redhat.com> - 0.2.997-2.git20091214
- cdma: fix signal strength reporting on some devices
- cdma: better registration state detection when dialing (ex Sierra 5275)
- option: always use the correct tty for dialing commands

* Mon Dec  7 2009 Dan Williams <dcbw@redhat.com> - 0.2.997-1
- core: fix reconnect after manual disconnect (rh #541314)
- core: fix various segfaults during registration
- core: fix probing of various modems on big-endian architectures (ie PPC)
- core: implement modem states to avoid duplicate operations
- hso: fix authentication for Icera-based devices like iCON 505
- zte: use correct port for new devices
- nozomi: fix detection

* Thu Nov  5 2009 Dan Williams <dcbw@redhat.com> - 0.2-4.20091105
- Update to latest git
- core: fix pppd 2.4.5 errors about 'baudrate 0'
- cdma: wait for network registration before trying to connect
- gsm: add cell access technology reporting
- gsm: allow longer-running network scans
- mbm: various fixes for Ericsson F3507g/F3607gw/Dell 5530
- nokia: don't power down phones on disconnect
- hso: fix disconnection/disable

* Wed Aug 26 2009 Dan Williams <dcbw@redhat.com> - 0.2-3.20090826
- Fixes for Motorola and Ericsson devices
- Fixes for CDMA "serving-system" command parsing

* Fri Jul 31 2009 Matthias Clasen <mclasen@redhat.com>
- Fix a typo in one of the udev rules files

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-2.20090707
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 7 2009 Dan Williams <dcbw@redhat.com> - 0.2-1.20090707
- Fix source repo location
- Fix directory ownership

* Tue Jul 7 2009 Dan Williams <dcbw@redhat.com> - 0.2-0.20090707
- Initial version

