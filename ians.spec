%define         _kernel_ver 	%(grep UTS_RELEASE %{_kernelsrcdir}/include/linux/version.h 2>/dev/null | cut -d'"' -f2)
%define		_kernel_ver_str	%(echo %{_kernel_ver} | sed s/-/_/g)
%define		_rel 3

Summary:	IANS utility for Intel(R) PRO/100
Summary(pl):	Narzêdzie IANS do karty Intel(R) PRO/100
Name:		ians
Version:	1.5.18c
Release:	%{_rel}
Group:		Base/Kernel
Group(de):	Grundsätzlich/Kern
Group(pl):	Podstawowe/J±dro
License:	BSD, see LICENSE_BINARY
Vendor:		Intel Corporation
Source0:	ftp://aiedownload.intel.com/df-support/2895/eng/iANS-%{version}.tar.gz
Patch0:		%{name}-makefile.patch
URL:		http://support.intel.com/support/network/adapter/pro100/
Exclusivearch:  %{ix86}
Requires:       kernel(ians) = %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)


%define		_sysconfdir	/etc/ians

%description
This package contains the Linux driver for the Intel(R) PRO/100 family
of 10/100 Ethernet network adapters. It contains module ians.o which
allows you to use advanced options of that cards (vlan, team-work)
and some utilities.

%description -l pl
Ten pakiet zawiera linuksowy modu³ ians.o do kart Intel(R) PRO/100, który
pozwala na sterowanie zaawansowanymi opcjami tych kart (vlan, team-work)
oraz narzêdzia do zarz±dzania tymi opcjami.

%package -n kernel-net-ians
Summary:	IANS kernel module for Intel(R) PRO/100
Summary(pl):	Modu³ IANS do karty Intel(R) PRO/100
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Group(de):	Grundsätzlich/Kern
Group(pl):	Podstawowe/J±dro
Conflicts:	kernel < %{_kernel_ver}, kernel > %{_kernel_ver}
Conflicts:	kernel-%{?_with_smp:up}%{!?_with_smp:smp}
Requires:	ians = %{version}
Obsoletes:	linux-smp-net-ians
Provides:	kernel(ians) = %{version}
Prereq:		/sbin/depmod

%description -n kernel-net-ians
This package contains module ians.o which allows you to use advanced options
of Intel cards (vlan, team-work).

%description -n kernel-net-ians -l pl
Ten pakiet zawiera linuksowy modu³ ians.o do kart Intel(R) PRO/100, który
pozwala na sterowanie zaawansowanymi opcjami tych kart (vlan, team-work).

%package -n kernel-smp-net-ians
Summary:	IANS kernel SMP module for Intel(R) PRO/100
Summary(pl):	Modu³ SMP IANS do karty Intel(R) PRO/100
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Group(de):	Grundsätzlich/Kern
Group(pl):	Podstawowe/J±dro
Conflicts:	kernel < %{_kernel_ver}, kernel > %{_kernel_ver}
Conflicts:	kernel-%{?_with_smp:up}%{!?_with_smp:smp}
Requires:	ians = %{version}
Obsoletes:	linux-net-ians
Provides:	kernel(ians) = %{version}
Prereq:		/sbin/depmod

%description -n kernel-smp-net-ians
This package contains module ians.o (for SMP systems) which allows you to use
advanced options of Intel cards (vlan, team-work).

%description -n kernel-smp-net-ians -l pl
Ten pakiet zawiera linuksowy (SMP) modu³ ians.o do kart Intel(R) PRO/100, który
pozwala na sterowanie zaawansowanymi opcjami tych kart (vlan, team-work).

%prep
%setup -q -n iANS-1.5.18
%patch -p0

%build
cd src
%{__make} CC="kgcc -DCONFIG_X86_LOCAL_APIC" SMP=1
mv bin/ia32/ians.o bin/ia32/ians-smp.o
%{__make} clean
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/%{_sysconfdir}
cd src
%{__make} DESTDIR=$RPM_BUILD_ROOT install
cd ..
# clean out the files created by running depmod in make install
rm -f $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/modules.*

gzip -9nf README LICENSE_BINARY src/LICENSE_OPEN_SOURCE

install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp
install src/bin/ia32/ians-smp.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/ians.o

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel-net-ians
/sbin/depmod -a

%postun	-n kernel-net-ians
/sbin/depmod -a

%post	-n kernel-smp-net-ians
/sbin/depmod -a

%postun	-n kernel-smp-net-ians
/sbin/depmod -a

%files
%defattr(644,root,root,755)
%attr(755,root,root) /sbin/*
%attr(644,root,root) %{_mandir}/man*/*
%dir %attr(755,root,root) %{_sysconfdir}
%doc *.gz install_scripts src/*.gz

%files -n kernel-net-ians
%defattr(644,root,root,755)
%attr(644,root,root) /lib/modules/%{_kernel_ver}/*

%files -n kernel-smp-net-ians
%defattr(644,root,root,755)
%attr(644,root,root) /lib/modules/%{_kernel_ver}smp/*
