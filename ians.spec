#
# _without_dist_kernel - without distribution kernel
#
%define		_rel 1
%define		_ver 1.7.17

Summary:	IANS utility for Intel(R) PRO/100
Summary(pl):	Narz�dzie IANS do karty Intel(R) PRO/100
Name:		ians
Version:	%{_ver}
Release:	%{_rel}
Group:		Base/Kernel
License:	BSD (see LICENSE_BINARY)
Vendor:		Intel Corporation
Source0:	ftp://aiedownload.intel.com/df-support/2895/eng/iANS-%{version}.tar.gz
URL:		http://support.intel.com/support/network/adapter/pro100/
%{!?_without_dist_kernel:BuildRequires: kernel-headers}
BuildRequires:	%{kgcc_package}
ExclusiveArch:	%{ix86}
%{!?_without_dist_kernel:Requires:	kernel(ians) = %{version}}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)


%define		_sysconfdir	/etc/ians

%description
This package contains the Linux driver for the Intel(R) PRO/100 family
of 10/100 Ethernet network adapters. It contains module ians.o which
allows you to use advanced options of that cards (vlan, team-work) and
some utilities.

%description -l pl
Ten pakiet zawiera linuksowy modu� ians.o do kart Intel(R) PRO/100,
kt�ry pozwala na sterowanie zaawansowanymi opcjami tych kart (vlan,
team-work) oraz narz�dzia do zarz�dzania tymi opcjami.

%package -n kernel-net-ians
Summary:	IANS kernel module for Intel(R) PRO/100
Summary(pl):	Modu� IANS do karty Intel(R) PRO/100
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Prereq:		/sbin/depmod
%{!?_without_dist_kernel:%requires_releq_kernel_up}
Requires:	ians = %{version}
Provides:	kernel(ians) = %{version}
Obsoletes:	linux-smp-net-ians

%description -n kernel-net-ians
This package contains module ians.o which allows you to use advanced
options of Intel cards (vlan, team-work).

%description -n kernel-net-ians -l pl
Ten pakiet zawiera linuksowy modu� ians.o do kart Intel(R) PRO/100,
kt�ry pozwala na sterowanie zaawansowanymi opcjami tych kart (vlan,
team-work).

%package -n kernel-smp-net-ians
Summary:	IANS kernel SMP module for Intel(R) PRO/100
Summary(pl):	Modu� SMP IANS do karty Intel(R) PRO/100
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Prereq:		/sbin/depmod
%{!?_without_dist_kernel:%requires_releq_kernel_smp}
Requires:	ians = %{version}
Provides:	kernel(ians) = %{version}
Obsoletes:	linux-net-ians

%description -n kernel-smp-net-ians
This package contains module ians.o (for SMP systems) which allows you
to use advanced options of Intel cards (vlan, team-work).

%description -n kernel-smp-net-ians -l pl
Ten pakiet zawiera linuksowy (SMP) modu� ians.o do kart Intel(R)
PRO/100, kt�ry pozwala na sterowanie zaawansowanymi opcjami tych kart
(vlan, team-work).

%prep
%setup -q -n iANS-%{_ver}

%build
cd src
%{__make} CC="%{kgcc} -DCONFIG_X86_LOCAL_APIC" SMP=1
mv -f ../bin/ia32/ians.o ../bin/ia32/ians-smp.o
%{__make} clean
%{__make} SMP=0

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/%{_sysconfdir}
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc
cd src
%{__make} MAN_DIR=/usr/share/man \
	BIN_DIR=/sbin \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	install
cd ..

install bin/ia32/ians.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/ians.o

install bin/ia32/ians-smp.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/ians.o

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
%doc README LICENSE install_scripts

%files -n kernel-net-ians
%defattr(644,root,root,755)
%attr(644,root,root) /lib/modules/%{_kernel_ver}/misc/*

%files -n kernel-smp-net-ians
%defattr(644,root,root,755)
%attr(644,root,root) /lib/modules/%{_kernel_ver}smp/misc/*
