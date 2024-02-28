#
# Conditional build:
%bcond_without	java		# JNI library
%bcond_with	fftw3		# fftw3 for FFT (default is builtin)
%bcond_with	libsamplerate	# libsamplerate for resampling (default is builtin)

Summary:	An audio time-stretching and pitch-shifting library and utility program
Summary(pl.UTF-8):	Biblioteka i narzędzie do rozciągania i harmonizowania dźwięku
Name:		rubberband
Version:	3.3.0
Release:	1
License:	GPL v2+
Group:		Applications/Sound
Source0:	https://breakfastquay.com/files/releases/%{name}-%{version}.tar.bz2
# Source0-md5:	b0ba4fb331e694a07848896f4845e8ea
Patch0:		%{name}-pc.patch
Patch1:		%{name}-update.patch
URL:		https://www.breakfastquay.com/rubberband/
# also kissfft, sleef >= 3.3.0, ipp possible
%{?with_fftw3:BuildRequires:	fftw3-devel >= 3.0.0}
%{?with_jni:BuildRequires:	jdk}
BuildRequires:	ladspa-devel
# also speexdsp >= 1.0.0 possible
%{?with_libsamplerate:BuildRequires:	libsamplerate-devel >= 0.1.8}
BuildRequires:	libsndfile-devel >= 1.0.16
BuildRequires:	libstdc++-devel >= 6:5
BuildRequires:	lv2-devel
BuildRequires:	meson >= 0.53.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	vamp-devel >= 2.9
Requires:	%{name}-libs = %{version}-%{release}
Requires:	libsndfile >= 1.0.16
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
%{?with_libsamplerate:Requires:	libsamplerate >= 0.1.8}

%description libs
Shared rubberband library.

%description libs -l pl.UTF-8
Biblioteka współdzielona rubberband.

%package devel
Summary:	Header files for rubberband library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki rubberband
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
%{?with_libsamplerate:Requires:	libsamplerate-devel >= 0.1.8}

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
%{?with_libsamplerate:Requires:	libsamplerate >= 0.1.8}

%description -n java-rubberband
Java JNI interface for rubberband.

%description -n java-rubberband -l pl.UTF-8
Interfejs Javy JNI do rubberband.

%package -n ladspa-rubberband-plugins
Summary:	rubberband LADSPA plugin
Summary(pl.UTF-8):	Wtyczka LADSPA rubberband
Group:		Applications/Sound
Requires:	ladspa-common
%{?with_libsamplerate:Requires:	libsamplerate >= 0.1.8}

%description -n ladspa-rubberband-plugins
rubberband LADSPA plugin.

%description -n ladspa-rubberband-plugins -l pl.UTF-8
Wtyczka LADSPA rubberband.

%package -n lv2-rubberband
Summary:	rubberband LV2 plugin
Summary(pl.UTF-8):	Wtyczka LV2 rubberband
Group:		Applications/Sound
Requires:	lv2
%{?with_libsamplerate:Requires:	libsamplerate >= 0.1.8}

%description -n lv2-rubberband
rubberband LV2 plugin.

%description -n lv2-rubberband -l pl.UTF-8
Wtyczka LV2 rubberband.

%package -n vamp-plugins-rubberband
Summary:	rubberband Vamp plugin
Summary(pl.UTF-8):	Wtyczka Vamp rubberband
Group:		Applications/Sound
%{?with_libsamplerate:Requires:	libsamplerate >= 0.1.8}
Requires:	vamp >= 2.9

%description -n vamp-plugins-rubberband
rubberband Vamp plugin.

%description -n vamp-plugins-rubberband -l pl.UTF-8
Wtyczka Vamp rubberband.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%if %{with java}
# required for meson javac detection (at least meson 1.0.1 / openjdk8 combo)
export CLASSPATH=.
%endif

%meson build \
	%{?with_java:-Dextra_include_dirs="%{_jvmdir}/java/include,%{_jvmdir}/java/include/linux"} \
	%{?with_fft:-Dfft=fftw} \
	-Djni=%{__enabled_disabled java} \
	%{?with_libsamplerate:-Dresampler=libsamplerate}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%if %{with java}
install -d $RPM_BUILD_ROOT%{_javadir}
cp -p build/rubberband.jar $RPM_BUILD_ROOT%{_javadir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post	-n java-rubberband -p /sbin/ldconfig
%postun	-n java-rubberband -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG README.md
%attr(755,root,root) %{_bindir}/rubberband
%attr(755,root,root) %{_bindir}/rubberband-r3

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/librubberband.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/librubberband.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/librubberband.so
%{_includedir}/rubberband
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

%files -n lv2-rubberband
%defattr(644,root,root,755)
%dir %{_libdir}/lv2/rubberband.lv2
%attr(755,root,root) %{_libdir}/lv2/rubberband.lv2/lv2-rubberband.so
%{_libdir}/lv2/rubberband.lv2/lv2-rubberband.ttl
%{_libdir}/lv2/rubberband.lv2/manifest.ttl

%files -n vamp-plugins-rubberband
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/vamp/vamp-rubberband.so
%{_libdir}/vamp/vamp-rubberband.cat
