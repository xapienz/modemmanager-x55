%define snapshot .git20100317
%define ppp_version 2.4.5

Summary: Mobile broadband modem management service
Name: ModemManager
Version: 0.3
Release: 3%{snapshot}%{?dist}
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
Requires: dbus-glib >= 0.82
Requires: glib2 >= 2.18
BuildRequires: glib2-devel >= 2.18
BuildRequires: dbus-glib-devel >= 0.82
BuildRequires: libgudev-devel >= 143
BuildRequires: ppp = %{ppp_version}
BuildRequires: ppp-devel = %{ppp_version}
BuildRequires: polkit-devel
BuildRequires: automake autoconf intltool libtool
# for xsltproc
BuildRequires: libxslt

%description
The ModemManager service provides a consistent API to operate many different
modems, including mobile broadband (3G) devices.

%prep
%setup -q

%build

pppddir=`ls -1d %{_libdir}/pppd/2*`
%configure \
	--enable-more-warnings=yes \
	--with-udev-base-dir=/lib/udev \
	--with-tests=yes \
	--with-docs=yes \
	--disable-static \
	--with-pppd-plugin-dir=$pppddir \
	--with-polkit=yes

make %{?_smp_mflags}

%check
make check

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/pppd/2.*/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/pppd/2.*/*.so

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  gtk-update-icon-cache -q %{_datadir}/icons/hicolor
fi

%postun
/sbin/ldconfig
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  gtk-update-icon-cache -q %{_datadir}/icons/hicolor
fi

%files
%defattr(0644, root, root, 0755)
%doc COPYING README
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.ModemManager.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.ModemManager.service
%attr(0755,root,root) %{_sbindir}/modem-manager
%dir %{_libdir}/%{name}
%attr(0755,root,root) %{_libdir}/%{name}/*.so*
/lib/udev/rules.d/*
%{_datadir}/polkit-1/actions/*.policy
%{_datadir}/icons/hicolor/22x22/apps/modem-manager.png

%changelog
* Wed Mar 17 2010 Dan Williams <dcbw@redhat.com> - 0.3-3.git20100317
- mbm: add device IDs for C3607w
- mbm: fail earlier during connection failures
- mbm: fix username/password authentication when checked by the network
- hso: implement asynchronous signal quality updates
- option: implement asynchronous signal quality updates
- novatel: correctly handle CDMA signal quality
- core: basic PolicyKit support
- core: fix direct GSM registration information requests
- core: general GSM PIN/PUK unlock fixes
- core: poll GSM registration state internally for quicker status updates
- core: implement GSM 2G/3G preference
- core: implement GSM roaming allowed/disallowed preference
- core: emit signals on access technology changes
- core: better handling of disconnections
- core: fix simple CDMA status requests

* Thu Feb 11 2010 Dan Williams <dcbw@redhat.com> - 0.3-2.git20100211
- core: startup speed improvements
- core: GSM PIN checking improvements
- huawei: fix EVDO-only connections on various devices (rh #553199)
- longcheer: add support for more devices

* Tue Jan 19 2010 Dan Williams <dcbw@redhat.com> - 0.3-1.git20100119
- anydata: new plugin for AnyData CDMA modems (rh #547294)
- core: fix crashes when devices are unplugged during operation (rh #553953)
- cdma: prefer primary port for status/registration queries
- core: fix probing/detection of some PIN-locked devices (rh #551376)
- longcheer: add plugin for Alcatel (X020, X030, etc) and other devices
- gsm: fix Nokia N80 network scan parsing

* Fri Jan  1 2010 Dan Williams <dcbw@redhat.com> - 0.2.997-5.git20100101
- core: fix apparent hangs by limiting retried serial writes
- gsm: ensure modem state is reset when disabled

* Fri Dec 18 2009 Dan Williams <dcbw@redhat.com> - 0.2.997-4.git20091218
- sierra: fix CDMA registration detection in some cases (rh #547513)

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

