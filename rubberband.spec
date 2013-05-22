Summary:	An audio time-stretching and pitch-shifting library and utility program
Summary(pl.UTF-8):	Biblioteka i narzędzie do rozciagania i harmonizowania dźwięku
Name:		rubberband
Version:	1.8.1
Release:	1
License:	GPL v2
Group:		Applications/Sound
Source0:	http://code.breakfastquay.com/attachments/download/34/%{name}-%{version}.tar.bz2
# Source0-md5:	6c2b4e18a714bcc297d0db81a10f9348
URL:		http://www.breakfastquay.com/rubberband/
BuildRequires:	fftw3-devel
BuildRequires:	ladspa-devel
BuildRequires:	libsamplerate-devel
BuildRequires:	libsndfile-devel
BuildRequires:	libstdc++-devel
BuildRequires:	pkg-config
BuildRequires:	vamp-devel
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Rubber Band is a library and utility program that permits you to
change the tempo and pitch of an audio recording independently of one
another.

%description -l pl.UTF-8
Rubber Band to biblioteka i program narzędziowy, który pozwala ci na
zmianę tempa i wysokości tonu nagrywanego dźwięku niezaleźnie od
innego.

%package libs
Summary:	rubberband library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki rubberband
Group:		Libraries

%description libs
rubberband library.

%description libs -l pl.UTF-8
Biblioteka rubberband.

%package devel
Summary:	Header files for rubberband library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki rubberband
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for rubberband library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki rubberband.

%package static
Summary:	Static rubberband library
Summary(pl.UTF-8):	Statyczna biblioteka rubberband
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static rubberband library.

%description static -l pl.UTF-8
Statyczna biblioteka rubberband.

%package -n ladspa-rubberband-plugins
Summary:	rubberband ladspa plugin
Group:		Applications/Sound

%description -n ladspa-rubberband-plugins
rubberband ladspa plugin.

%package -n vamp-plugins-rubberband
Summary:	rubberband vamp plugin
Group:		Applications/Sound

%description -n vamp-plugins-rubberband
rubberband vamp plugin.

%prep
%setup -q

%build
%configure
%{__make} \
	INSTALL_LIBDIR="%{_libdir}" \
	INSTALL_VAMPDIR="%{_libdir}/vamp" \
	INSTALL_LADSPADIR="%{_libdir}/ladspa"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	INSTALL_LIBDIR="%{_libdir}" \
	INSTALL_VAMPDIR="%{_libdir}/vamp" \
	INSTALL_LADSPADIR="%{_libdir}/ladspa" \
	INSTALL_PKGDIR="%{_pkgconfigdir}"

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG README.txt
%attr(755,root,root) %{_bindir}/rubberband

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/librubberband.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/librubberband.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/librubberband.so
%{_includedir}/%{name}
%{_pkgconfigdir}/rubberband.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/librubberband.a

%files -n ladspa-rubberband-plugins
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/ladspa/ladspa-rubberband.so
%{_libdir}/ladspa/ladspa-rubberband.cat
%{_datadir}/ladspa/rdf/ladspa-rubberband.rdf

%files -n vamp-plugins-rubberband
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/vamp/vamp-rubberband.so
%{_libdir}/vamp/vamp-rubberband.cat
