%define         _kernel_ver 	%(grep UTS_RELEASE %{_kernelsrcdir}/include/linux/version.h 2>/dev/null | cut -d'"' -f2)
%define		_kernel_ver_str	%(echo %{_kernel_ver} | sed s/-/_/g)
%define		smpstr		%{?_with_smp:-smp}
%define         smp     	%{?_with_smp:1}%{!?_with_smp:0}

Summary:	IANS utility for Intel(R) PRO/100
Summary(pl):	Narz�dzie IANS do karty Intel(R) PRO/100
Name:		ians
Version:	1.4.27
Release:	1
Group:		Base/Kernel
Group(de):	Grunds�tzlich/Kern
Group(pl):	Podstawowe/J�dro
License:	BSD
Vendor:		Intel Corporation
Source0:	ftp://download.intel.com/df-support/2895/eng/iANS-%{version}.tar.gz
Patch0:		%{name}-makefile.patch
URL:		http://support.intel.com/support/network/adapter/pro100/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/ians

%description
This package contains the Linux driver for the Intel(R) PRO/100 family
of 10/100 Ethernet network adapters. It contains module ians.o which
allows you to use advanced options of that cards (vlan, team-work).

%description -l pl
Ten pakiet zawiera Linuksowy modu� ians.o do kart Intel(R) PRO/100, kt�ry
pozwala na sterowanie zaawansowanymi opcjami tych kart (vlan, team-work).

%package -n kernel%{smpstr}-net-ians
Summary:	IANS utility for Intel(R) PRO/100
Summary(pl):	Narz�dzie IANS do karty Intel(R) PRO/100
Release:	%{release}@%{_kernel_ver_str}
Group:		Base/Kernel
Group(de):	Grunds�tzlich/Kern
Group(pl):	Podstawowe/J�dro
Conflicts:	kernel < %{_kernel_ver}, kernel > %{_kernel_ver}
Conflicts:	kernel-%{?_with_smp:up}%{!?_with_smp:smp}
Obsoletes:	linux-net-ians
Obsoletes:	ians
Provides:	ians
Prereq:		/sbin/depmod

%description -n kernel%{smpstr}-net-ians
This package contains the Linux driver for the Intel(R) PRO/100 family
of 10/100 Ethernet network adapters. It contains module ians.o which
allows you to use advanced options of that cards (vlan, team-work).

%description -n kernel%{smpstr}-net-ians -l pl
Ten pakiet zawiera Linuksowy modu� ians.o do kart Intel(R) PRO/100, kt�ry
pozwala na sterowanie zaawansowanymi opcjami tych kart (vlan, team-work).

%prep
%setup -q -n iANS-%{version}
%patch -p0

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/%{_sysconfdir}

%{__make} DESTDIR=$RPM_BUILD_ROOT install

# clean out the files created by running depmod in make install
rm -f $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/modules.*

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{smpstr}-net-ians
/sbin/depmod -a

%postun	-n kernel%{smpstr}-net-ians
/sbin/depmod -a

%files -n kernel%{smpstr}-net-ians
%defattr(644,root,root,755)
%attr(644,root,root) /lib/modules/%{_kernel_ver}/*
%attr(644,root,root) %{_mandir}/man*/*
%attr(755,root,root) /sbin/*
%dir %attr(755,root,root) %{_sysconfdir}
