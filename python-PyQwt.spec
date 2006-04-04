#
# Conditional build:
%bcond_with	numeric		# build with Python Numeric extend
%bcond_without	numarray	# build without Python numarray extend
#
%define		module	PyQwt
Summary:	Python bindings for the Qwt library
Name:		python-%{module}
Version:	4.2
Release:	0.1
License:	GPL v2+
Group:		Libraries/Python
Source0:	http://dl.sourceforge.net/pyqwt/%{module}-%{version}.tar.gz
# Source0-md5:	70cf89765cc51c3e9e2e5d1eef9522f1
URL:		http://pyqwt.sourceforge.net/
BuildRequires:	python-PyQt-devel
BuildRequires:	python-devel >= 1:2.3
%{?with_numarray:BuildRequires:	python-numarray-devel}
%{?with_numeric:BuildRequires:	python-numpy-devel}
BuildRequires:	qwt-devel >= 4.2.0-3
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
Requires:	python-PyQt
%{?with_numarray:Requires:	python-numarray}
%{?with_numeric:Requires:	python-numpy}
%pyrequires_eq	python-libs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sipfilesdir	%{_datadir}/sip

%description
PyQwt is a set of Python bindings for the Qwt C++ class library which
extends the Qt framework with widgets for scientific and engineering
applications. It provides a widget to plot 2-dimensional data and
various widgets to display and control bounded or unbounded floating
point values.

%package devel
Summary:	Files needed to build other bindings based on PyQwt
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-sip-devel

%description devel
Files needed to build other bindings based on PyQwt.

%package examples
Summary:	Examples for PyQwt
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description examples
Examples code demonstrating how to use the Python bindings for Qwt.

%prep
%setup -q -n %{module}-%{version}

%build
export QTDIR=%{_prefix}
cd configure
python configure.py \
	-c -j 3 \
	-d %{py_sitedir} \
	-i %{_includedir}/qwt \
	-l %{_libdir} \
	-v %{_sipfilesdir}

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
cp -R examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS Doc/html/pyqwt
%dir %{py_sitedir}/iqt
%dir %{py_sitedir}/qwt
%attr(755,root,root) %{py_sitedir}/iqt/*.so
%attr(755,root,root) %{py_sitedir}/qwt/*.so
%{py_sitedir}/iqt/*.py[co]
%{py_sitedir}/qwt/*.py[co]

%files devel
%defattr(644,root,root,755)
%{_sipfilesdir}/qwt

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/*