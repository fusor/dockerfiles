%if 0%{?copr}
%define build_timestamp .%(date +"%Y%m%d%H%M%%S")
%else
%define build_timestamp %{nil}
%endif

Name: mediawiki-container-scripts
Version:	1.0.0
Release:	1.1%{build_timestamp}%{?dist}
Summary:	Scripts for the mediawiki container image

License:	ASL 2.0
URL:		https://github.com/jmontleon/dockerfiles
Source0:	https://github.com/jmontleon/dockerfiles/archive/dockerfiles-%{version}.tar.gz
BuildArch:  noarch

%description
%{summary}

%prep
%setup -q -n %{name}-%{version}

%install
mkdir -p %{buildroot}%{_bindir} %{buildroot}%{_datadir}/%{name}
install -m 755 entrypoint.sh %{buildroot}%{_bindir}
install -m 644 mediawiki123.conf %{buildroot}%{_datadir}/%{name}/mediawiki123.conf.example

%files
%doc
%{_bindir}/entrypoint.sh
%{_datadir}/%{name}/mediawiki123.conf.example

%changelog

