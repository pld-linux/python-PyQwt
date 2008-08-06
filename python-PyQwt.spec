#
# Conditional build:
%bcond_with	numeric		# build with Python Numeric extend
%bcond_without	numarray	# build without Python numarray extend
#
%define		module	PyQwt
Summary:	Python bindings for the Qwt library
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki Qwt
Name:		python-%{module}
Version:	5.1.0
Release:	0.1
License:	GPL v2+
Group:		Libraries/Python
Source0:	http://dl.sourceforge.net/pyqwt/%{module}-%{version}.tar.gz
# Source0-md5:	c9d662a0d4fc95cec75d3c526e4e748a
URL:		http://pyqwt.sourceforge.net/
BuildRequires:	QtCore-devel
BuildRequires:	QtGui-devel
BuildRequires:	QtSvg-devel
%{?with_numeric:BuildRequires:	python-Numeric-devel}
BuildRequires:	python-PyQt4-devel
BuildRequires:	python-devel >= 1:2.3
%{?with_numarray:BuildRequires:	python-numpy-numarray-devel}
BuildRequires:	python-sip-devel
BuildRequires:	qwt-devel >= 4.2.0-3
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
%{?with_numeric:Requires:	python-Numeric}
Requires:	python-PyQt4
%{?with_numarray:Requires:	python-numarray}
%pyrequires_eq	python-libs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sipfilesdir	%{_datadir}/sip

%description
PyQwt is a set of Python bindings for the Qwt C++ class library which
extends the Qt framework with widgets for scientific and engineering
applications. It provides a widget to plot 2-dimensional data and
various widgets to display and control bounded or unbounded floating
point values.

%description -l pl.UTF-8
PyQwt to zbiór wiązań Pythona do biblioteki klas C++ Qwt,
rozszerzającej szkielet Qt o widgety dla aplikacji naukowych i
inżynierskich. Udostępnia widget do wykresów danych 2-wymiarowych i
różne widgety do wyświetlania i zmiany ograniczonych i
nieograniczonych wartości zmiennoprzecinkowych.

%package devel
Summary:	Files needed to build other bindings based on PyQwt
Summary(pl.UTF-8):	Pliki potrzebne do tworzenia innych wiązań w oparciu o PyQwt
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-sip-devel

%description devel
Files needed to build other bindings based on PyQwt.

%description devel -l pl.UTF-8
Pliki potrzebne do tworzenia innych wiązań w oparciu o PyQwt.

%package examples
Summary:	Examples for PyQwt
Summary(pl.UTF-8):	Przykłady do PyQwt
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description examples
Examples code demonstrating how to use the Python bindings for Qwt.

%description examples -l pl.UTF-8
Przykładowy kod demonstrujący sposób użycia wiązań Pythona do Qwt.

%prep
%setup -q -n %{module}-%{version}

%build
export QTDIR=%{_prefix}
cd configure
python configure.py \
	-Q ../qwt-5.1

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

export QTDIR=%{_prefix}
cd configure
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
cd ..

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

rm -f examples/{iqt,qwt}
cp -R qt4examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Doc/html/pyqwt
%dir %{py_sitedir}/PyQt4/Qwt5
%attr(755,root,root) %{py_sitedir}/PyQt4/Qwt5/*.so
%{py_sitedir}/PyQt4/Qwt5/*.py[co]

%files devel
%defattr(644,root,root,755)
%{_sipfilesdir}/PyQt4/Qwt5

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/*
