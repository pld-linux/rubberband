#
# Conditional build:
%bcond_without	java	# JNI library

Summary:	An audio time-stretching and pitch-shifting library and utility program
Summary(pl.UTF-8):	Biblioteka i narzędzie do rozciągania i harmonizowania dźwięku
Name:		rubberband
Version:	1.8.2
Release:	1
License:	GPL v2+
Group:		Applications/Sound
Source0:	https://breakfastquay.com/files/releases/%{name}-%{version}.tar.bz2
# Source0-md5:	db0ecb4f1a647bdaf7e43ef2ca2f7883
Patch0:		%{name}-pc.patch
Patch1:		%{name}-jni.patch
URL:		http://www.breakfastquay.com/rubberband/
BuildRequires:	fftw3-devel >= 3
%{?with_jni:BuildRequires:	jdk}
BuildRequires:	ladspa-devel
BuildRequires:	libsamplerate-devel
BuildRequires:	libsndfile-devel
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
BuildRequires:	vamp-devel
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Rubber Band is a library and utility program that permits you to
change the tempo and pitch of an audio recording independently of one
another.

%description -l pl.UTF-8
Rubber Band to biblioteka i program narzędziowy, który pozwala na
zmianę tempa i wysokości tonu nagrywanego dźwięku niezależnie.

%package libs
Summary:	Shared rubberband library
Summary(pl.UTF-8):	Biblioteka współdzielona rubberband
Group:		Libraries

%description libs
Shared rubberband library.

%description libs -l pl.UTF-8
Biblioteka współdzielona rubberband.

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

%package -n java-rubberband
Summary:	Java JNI interface for rubberband
Summary(pl.UTF-8):	Interfejs Javy JNI do rubberband
Group:		Libraries/Java
Requires:	jre

%description -n java-rubberband
Java JNI interface for rubberband.

%description -n java-rubberband -l pl.UTF-8
Interfejs Javy JNI do rubberband.

%package -n ladspa-rubberband-plugins
Summary:	rubberband LADSPA plugin
Summary(pl.UTF-8):	Wtyczka LADSPA rubberband
Group:		Applications/Sound
Requires:	ladspa-common

%description -n ladspa-rubberband-plugins
rubberband LADSPA plugin.

%description -n ladspa-rubberband-plugins -l pl.UTF-8
Wtyczka LADSPA rubberband.

%package -n vamp-plugins-rubberband
Summary:	rubberband Vamp plugin
Summary(pl.UTF-8):	Wtyczka Vamp rubberband
Group:		Applications/Sound
Requires:	vamp

%description -n vamp-plugins-rubberband
rubberband Vamp plugin.

%description -n vamp-plugins-rubberband -l pl.UTF-8
Wtyczka Vamp rubberband.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%configure
%{__make} all %{?with_java:jni} \
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

%if %{with java}
install -d $RPM_BUILD_ROOT%{_javadir}
cp -p lib/rubberband.jar $RPM_BUILD_ROOT%{_javadir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post	-n java-rubberband -p /sbin/ldconfig
%postun	-n java-rubberband -p /sbin/ldconfig

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

%if %{with java}
%files -n java-rubberband
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/librubberband-jni.so
%{_javadir}/rubberband.jar
%endif

%files -n ladspa-rubberband-plugins
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/ladspa/ladspa-rubberband.so
%{_libdir}/ladspa/ladspa-rubberband.cat
%{_datadir}/ladspa/rdf/ladspa-rubberband.rdf

%files -n vamp-plugins-rubberband
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/vamp/vamp-rubberband.so
%{_libdir}/vamp/vamp-rubberband.cat
