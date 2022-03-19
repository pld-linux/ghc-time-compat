#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	time-compat
Summary:	Compatibility package for time
Name:		ghc-%{pkgname}
Version:	1.9.3
Release:	2
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/time-compat
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	6fbe42bfe2ce1e93aa7d98acf4aa61c2
URL:		http://hackage.haskell.org/package/time-compat
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base-orphans >= 0.8.1
%if %{with prof}
BuildRequires:	ghc-prof
BuildRequires:	ghc-base-orphans-prof >= 0.8.1
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires(post,postun):	/usr/bin/ghc-pkg
Requires:	ghc-base-orphans >= 0.8.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
This packages tries to compat as much of time features as possible.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-orphans-prof >= 0.8.1

%description prof
Profiling %{pkgname} library for GHC.  Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

cat >Setup.lhs<<'EOF'
#!/usr/bin/env runhaskell
> import Distribution.Simple
> main = defaultMain
EOF

%build
runhaskell Setup.lhs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs build
runhaskell Setup.lhs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.lhs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a

%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.dyn_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/Calendar
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/Calendar/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/Calendar/Easter
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/Calendar/Easter/*.dyn_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/Calendar/Easter/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/Calendar/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/Calendar/Julian
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/Calendar/Julian/*.dyn_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/Calendar/Julian/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/Calendar/MonthDay
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/Calendar/MonthDay/*.dyn_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/Calendar/MonthDay/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/Calendar/OrdinalDate
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/Calendar/OrdinalDate/*.dyn_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/Calendar/OrdinalDate/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/Calendar/WeekDate
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/Calendar/WeekDate/*.dyn_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/Calendar/WeekDate/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/Clock
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/Clock/*.dyn_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/Clock/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/Clock/POSIX
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/Clock/POSIX/*.dyn_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/Clock/POSIX/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/Clock/System
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/Clock/System/*.dyn_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/Clock/System/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/Clock/TAI
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/Clock/TAI/*.dyn_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/Clock/TAI/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/Format
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/Format/*.dyn_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/Format/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/Format/ISO8601
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/Format/ISO8601/*.dyn_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/Format/ISO8601/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/LocalTime
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/LocalTime/*.dyn_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/LocalTime/*.hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/Calendar/Easter/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/Calendar/Julian/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/Calendar/MonthDay/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/Calendar/OrdinalDate/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/Calendar/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/Calendar/WeekDate/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/Clock/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/Clock/POSIX/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/Clock/System/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/Clock/TAI/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/Format/ISO8601/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/Format/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/LocalTime/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Time/*.p_hi
%endif
