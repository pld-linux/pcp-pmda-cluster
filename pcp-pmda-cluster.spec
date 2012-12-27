#include	/usr/lib/rpm/macros.perl
Summary:	Performance Co-Pilot PMDA for clusters
Summary(pl.UTF-8):	PMDA PCP dla klastrów
Name:		pcp-pmda-cluster
Version:	1.0.1
Release:	1
License:	GPL v2+
Group:		Applications/System
Source0:	ftp://oss.sgi.com/projects/pcp/download/%{name}-%{version}.tar.bz2
# Source0-md5:	4100f18ef3a6a5907acf54502b26d2d9
Patch0:		%{name}-pcpfiles.patch
Patch1:		%{name}-update.patch
URL:		http://oss.sgi.com/projects/pcp/
BuildRequires:	pcp-devel >= 3.6.10-2
BuildRequires:	perl-base
Requires:	pcp >= 3.0.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the PMDA for collecting metrics from a
cluster of nodes using a "push" model, rather than the PMCD polling
other nodes. It is useful for clusters where extra overhead from
running daemons is unacceptable.

%description -l pl.UTF-8

%package client
Summary:	Performance Co-Pilot (PCP) cluster PMDA client daemon
Summary(pl.UTF-8):	Demon kliencki PMDA PCP dla klastrów
Group:		Applications/System
Requires:	pcp >= 3.0.1

%description client
This is the client daemon for the Performance Co-Pilot (PCP) cluster
PMDA.

%description client -l pl.UTF-8

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__make} \
	CC="%{__cc}" \
	PCFLAGS="%{rpmcflags} -D_GNU_SOURCE" \
	PCP_AWK_PROG=awk \
	SUBPMNS="/var/lib/pcp/pmns/root_linux $(pwd)/src/tmpdata/pmdas/ib/root" \
	SUBHELP="$(pwd)/src/tmpdata/pmdas/linux/help $(pwd)/src/tmpdata/pmdas/ib/help"

%install
rm -rf $RPM_BUILD_ROOT
#install -d $RPM_BUILD_ROOT%{_sysconfdir}

%{__make} install \
	PREFIX=$RPM_BUILD_ROOT \
	SUBPMNS="/var/lib/pcp/pmns/root_linux $(pwd)/src/tmpdata/pmdas/ib/root" \
	SUBHELP="$(pwd)/src/tmpdata/pmdas/linux/help $(pwd)/src/tmpdata/pmdas/ib/help"

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir /var/lib/pcp/pmdas/cluster
%attr(755,root,root) /var/lib/pcp/pmdas/cluster/Install
%attr(755,root,root) /var/lib/pcp/pmdas/cluster/Remove
%attr(755,root,root) /var/lib/pcp/pmdas/cluster/pmdacluster
%doc /var/lib/pcp/pmdas/cluster/README
/var/lib/pcp/pmdas/cluster/domain.h
/var/lib/pcp/pmdas/cluster/help
/var/lib/pcp/pmdas/cluster/pmns
/var/lib/pcp/pmdas/cluster/root
%config(noreplace) %verify(not md5 mtime size) /var/lib/pcp/pmdas/cluster/config
%dir /var/lib/pcp/pmdas/cluster/nodes

%files client
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/pmclusterd
%attr(755,root,root) %{_libdir}/pcp/bin/pmclusterd
