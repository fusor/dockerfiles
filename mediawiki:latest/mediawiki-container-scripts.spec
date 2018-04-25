%if 0%{?copr}
%define build_timestamp .%(date +"%Y%m%d%H%M%%S")
%else
%define build_timestamp %{nil}
%endif

Name: mediawiki-container-scripts
Version:	1.2.0
Release:	1%{build_timestamp}%{?dist}
Summary:	Scripts for the mediawiki container image

License:	ASL 2.0
URL:		https://github.com/fusor/dockerfiles
Source0:	https://github.com/fusor/dockerfiles/archive/mediawiki-container-scripts-%{version}.tar.gz
BuildArch:  noarch

%description
%{summary}

%prep
%setup -q -n %{name}-%{version}

%install
mkdir -p %{buildroot}%{_bindir} %{buildroot}%{_datadir}/%{name}
install -m 755 entrypoint.sh %{buildroot}%{_bindir}
install -m 644 mediawiki.conf %{buildroot}%{_datadir}/%{name}/mediawiki.conf.example

%files
%doc
%{_bindir}/entrypoint.sh
%{_datadir}/%{name}/mediawiki.conf.example

%changelog
* Wed Oct 04 2017 Jason Montleon <jmontleo@redhat.com> 1.0.2-1
- update archive name (jmontleo@redhat.com)

* Wed Oct 04 2017 Jason Montleon <jmontleo@redhat.com> 1.0.1-1
- new package built with tito


