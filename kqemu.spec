Name:           kqemu
Version:        1.3.0
Release:        0.8.pre11%{?dist}.1
Summary:        The QEMU Accelerator Module (KQEMU)

Group:          System Environment/Kernel
License:        GPLv2
URL:            http://bellard.org/qemu/
Source0:        http://bellard.org/qemu/kqemu-%{version}pre11.tar.gz
Source1:        %{name}.init
Source2:        %{name}.udev
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
ExcludeArch:    ppc ppc64

Provides:       kqemu-kmod-common = %{version}
Requires:       kqemu-kmod >= %{version}
Obsoletes:      kqemu-kmod < %{version}


Requires(post): /sbin/chkconfig
Requires(post): /sbin/service
Requires(preun): /sbin/service
Requires(preun): /sbin/chkconfig

Requires: qemu


%description
The QEMU Accelerator Module increases the speed of QEMU when a PC is 
emulated on a PC. It runs most of the target application code directly 
on the host processor to achieve near native performance. 



%prep
%setup -q -n kqemu-%{version}pre11


%build
# Nothing to build - was only needed for doc
echo "Nothing nothing to build"

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_initrddir}
install -pm 0755 %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/kqemu

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d
install -pm 0644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/60-kqemu.rules


%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ $1 -eq 1 ]; then
  /sbin/chkconfig --add kqemu ||:
#  /sbin/service kqemu start || :
fi

%preun 
if [ "$1" = 0 ]; then
  /sbin/service kqemu stop
  /sbin/chkconfig --del kqemu || :
fi 


%files
%defattr(-,root,root,-)
%doc Changelog COPYING LICENSE README
%doc tests *.html
%config %{_sysconfdir}/udev/rules.d/60-kqemu.rules
%{_initrddir}/kqemu


%changelog
* Sun Oct 05 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 1.3.0-0.8.pre11.1
- require qemu without a specific version

* Sat Oct 04 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 1.3.0-0.8.pre11
- rebuild for rpm fusion

* Fri Jun  6 2008 kwizart < kwizart at gmail.com > - 1.3.0-0.7.pre11
- Update init script

* Wed Jan  9 2008 kwizart < kwizart at gmail.com > - 1.3.0-0.6.pre11
- Fix ExcludeArch ppc for plague

* Sat Jan  5 2008 kwizart < kwizart at gmail.com > - 1.3.0-0.4.pre11
- Handle dev.rtc.max-user-freq with sysctl
- Add ExclusiveArch: i386 x86_64
- Udev rule in source

* Fri Nov  2 2007 kwizart < kwizart at gmail.com > - 1.3.0-0.3.pre11
- initscript is now faster
- Disable make doc (already done).

* Fri Nov  2 2007 kwizart < kwizart at gmail.com > - 1.3.0-0.2.pre11
- Clean for rpmfusion merge
- Improve initscript

* Fri Feb 09 2007 kwizart < kwizart at gmail.com > - 1.3.0-0.1.pre11
- Initial GPL Release.
