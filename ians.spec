#
# Conditional build:
%bcond_without	dist_kernel		# without distribution kernel
#
%define         _kernelsrcdir           /usr/src/linux-2.4
%define	_rel	1
Summary:	IANS utility for Intel(R) PRO/100
Summary(pl):	Narz�dzie IANS do karty Intel(R) PRO/100
Name:		ians
Version:	3.4.3a
Release:	%{_rel}
License:	BSD (see LICENSE_BINARY)
Group:		Base/Kernel
Source0:	ftp://aiedownload.intel.com/df-support/5600/eng/%{name}-%{version}.tar.gz
# Source0-md5:	6030f3ef19cf0e04cb9c83ecdca50c39
URL:		http://support.intel.com/support/network/adapter/pro100/
BuildRequires:	%{kgcc_package}
%{?without_dist_kernel:BuildRequires:	kernel24-source >= 2.4.0}
BuildRequires:	rpmbuild(macros) >= 1.118
%{?without_dist_kernel:Requires:	kernel(ians) = %{version}}
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Conflicts:	kernel > 2.6.0

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

%package -n kernel24-net-ians
Summary:	IANS kernel module for Intel(R) PRO/100
Summary(pl):	Modu� IANS do karty Intel(R) PRO/100
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{!?without_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
Requires:	ians = %{version}
Provides:	kernel(ians) = %{version}
Obsoletes:	kernel-net-ians
Obsoletes:	linux-smp-net-ians

%description -n kernel24-net-ians
This package contains module ians.o which allows you to use advanced
options of Intel cards (vlan, team-work).

%description -n kernel24-net-ians -l pl
Ten pakiet zawiera linuksowy modu� ians.o do kart Intel(R) PRO/100,
kt�ry pozwala na sterowanie zaawansowanymi opcjami tych kart (vlan,
team-work).

%package -n kernel24-smp-net-ians
Summary:	IANS kernel SMP module for Intel(R) PRO/100
Summary(pl):	Modu� SMP IANS do karty Intel(R) PRO/100
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{!?without_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod
Requires:	ians = %{version}
Provides:	kernel(ians) = %{version}
Obsoletes:	kernel-smp-net-ians
Obsoletes:	linux-net-ians

%description -n kernel24-smp-net-ians
This package contains module ians.o (for SMP systems) which allows you
to use advanced options of Intel cards (vlan, team-work).

%description -n kernel24-smp-net-ians -l pl
Ten pakiet zawiera linuksowy (SMP) modu� ians.o do kart Intel(R)
PRO/100, kt�ry pozwala na sterowanie zaawansowanymi opcjami tych kart
(vlan, team-work).

%prep
%setup -q -n iANS-%{version}

%build
cd src
%{__make} \
	CC="%{kgcc} -DCONFIG_X86_LOCAL_APIC -D__KERNEL_SMP=1 -D__SMP__" \
	SMP=1 \
	KSRC=%{_kernelsrcdir}

mv -f ../bin/ia32/ians.o ../bin/ia32/ians-smp.o
%{__make} clean \
	CC="%{kgcc}" \
	KSRC=%{_kernelsrcdir}

%{__make} \
	CC="%{kgcc}" \
	SMP=0 \
	KSRC=%{_kernelsrcdir}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc

%{__make} install -C src \
	MAN_DIR=%{_mandir} \
	BIN_DIR=/sbin \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	CC="%{kgcc}" \
	KSRC=%{_kernelsrcdir}

install bin/ia32/ians.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/ians.o
install bin/ia32/ians-smp.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/ians.o

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel24-net-ians
%depmod %{_kernel_ver}

%postun	-n kernel24-net-ians
%depmod %{_kernel_ver}

%post	-n kernel24-smp-net-ians
%depmod %{_kernel_ver}smp

%postun	-n kernel24-smp-net-ians
%depmod %{_kernel_ver}smp

%files
%defattr(644,root,root,755)
%attr(755,root,root) /sbin/*
%attr(644,root,root) %{_mandir}/man*/*
%dir %attr(755,root,root) %{_sysconfdir}
%doc README LICENSE

%files -n kernel24-net-ians
%defattr(644,root,root,755)
%attr(644,root,root) /lib/modules/%{_kernel_ver}/misc/*

%files -n kernel24-smp-net-ians
%defattr(644,root,root,755)
%attr(644,root,root) /lib/modules/%{_kernel_ver}smp/misc/*
