# RPM note: the incorrect-fsf-address in extensions/SyntaxHighlight_GeSHi/geshi/docs/COPYING is fixed upstream
#  Patch: https://phabricator.wikimedia.org/rSVN68355

%global mwdatadir %{_datadir}/mediawiki
%global mwikidir  %{_var}/www/mediawiki

Summary: A wiki engine
Name:    mediawiki
Version: 1.27.4
Release: 8%{?dist}
License: GPLv2+ and Public Domain and CC-BY-SA and MIT and ASL 2.0 and BSD and GPLv3+
# License breakdown: see PACKAGE-LICENSING
URL:     http://www.mediawiki.org/
Source0: http://releases.wikimedia.org/mediawiki/1.27/mediawiki-%{version}.tar.gz
Source1: mediawiki.conf
Source2: README.RPM
Source3: PACKAGE-LICENSING
Source4: https://github.com/wikimedia/mediawiki-vendor/archive/mediawiki-vendor-REL1_27.tar.gz
BuildArch: noarch
# This package contains some python maintenance scripts
BuildRequires: python2-devel

Obsoletes: mediawiki < 1.14.0-46
Provides: mediawiki = %{version}-%{release}
Obsoletes: mediawiki116 < 1.16.0-10
Provides: mediawiki116 = %{version}-%{release}
Obsoletes: mediawiki119 < 1.19.23-1
Provides: mediawiki119 = %{version}-%{release}
Obsoletes: mediawiki123 < 1.23.13-1
Provides: mediawiki123 = %{version}-%{release}

%description
MediaWiki is the software used for Wikipedia and the other Wikimedia
Foundation websites. Compared to other wikis, it has an excellent
range of features and support for high-traffic websites using multiple
servers

%package doc
Summary: Documentation for mediawiki
License: GPLv3+
Requires: %{name} = %{version}-%{release}

%description doc
Documentation for mediawiki

%prep
%setup -q -n mediawiki-%{version}

##
## Copy over the README's 
cp -p %{SOURCE2} .
cp -p %{SOURCE3} .

mv ./resources/lib/jquery.chosen/LICENSE COPYING.MIT

%build

%install

# move away the documentation to the final folder.
mkdir -p %{buildroot}%{_defaultdocdir}/%{name}-%{version}

# now copy the rest to the buildroot.
mkdir -p %{buildroot}%{mwdatadir}

FILES="StartProfiler.sample api.php autoload.php composer.json composer.local.json-sample COPYING CREDITS FAQ Gemfile.lock Gruntfile.js HISTORY img_auth.php index.php INSTALL jsduck.json load.php opensearch_desc.php phpcs.xml profileinfo.php Rakefile README RELEASE-NOTES-1.27 thumb.php thumb_handler.php UPGRADE wiki.phtml"

DIRECS="mw-config cache extensions images includes languages maintenance resources serialized skins"

SCRIPTS="maintenance/postgres/mediawiki_mysql2postgres.pl maintenance/postgres/compare_schemas.pl maintenance/storage/make-blobs includes/limit.sh extensions/ConfirmEdit/captcha.py"

rm -f docs/html/.gitignore

for i in ${FILES} ${DIRECS}; do
    cp -a ./${i} %{buildroot}%{mwdatadir}/${i}
done

# remove unneeded parts
find %{buildroot}%{mwdatadir}/  \( -name .htaccess \) -exec rm '{}' \;
find %{buildroot}%{mwdatadir}/  \( -name \*.cmi \) -exec rm '{}' \;

tar zxvf %{SOURCE4} -C %{buildroot}%{mwdatadir}/
mv %{buildroot}%{mwdatadir}/mediawiki-vendor-REL1_27 %{buildroot}%{mwdatadir}/vendor

find %{buildroot}%{mwdatadir}/  \( -name .gitignore \) -exec rm '{}' \;
find %{buildroot}%{mwdatadir}/  \( -name .gitreview \) -exec rm '{}' \;

# create a default instance of which other instances can be copied
mkdir -p %{buildroot}%{mwikidir}
cd %{buildroot}%{mwikidir}/

cp -a %{buildroot}%{mwdatadir}/images .
cp -a %{buildroot}%{mwdatadir}/cache .

LINKS="mw-config api.php extensions includes index.php languages load.php maintenance opensearch_desc.php resources serialized skins"
for i in ${LINKS}; do
  ln -s %{mwdatadir}/${i} ./${i}
done

mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d/
install -m 0644 -p %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d/mediawiki.conf
for i in ${SCRIPTS}; do
    chmod +x %{buildroot}%{mwdatadir}/${i}
done

%files
%defattr(-,root,root,-)
%license PACKAGE-LICENSING COPYING COPYING.MIT
%doc CREDITS RELEASE-NOTES-1.27 UPGRADE README.RPM
%attr(0644,root,root)  %config(noreplace) %{_sysconfdir}/httpd/conf.d/mediawiki.conf
%{mwdatadir}
%dir %{mwikidir}
%{mwikidir}/*.php
%{mwikidir}/extensions
%{mwikidir}/includes
%{mwikidir}/languages
%{mwikidir}/maintenance
%{mwikidir}/mw-config
%{mwikidir}/resources
%{mwikidir}/serialized
%{mwikidir}/skins
%attr(-,apache,apache) %dir %{mwikidir}/cache
%attr(-,apache,apache) %dir %{mwikidir}/images
%{mwikidir}/images/README

%files doc
%doc FAQ HISTORY README docs

%changelog
* Tue Apr 24 2018 Jason Montleon <jmontleo@redhat.com> - 1.27.4-8
- Update to 1.27.4-8. Intended for use with an rh-phpXX SCL.

* Wed Sep 07 2016 Kevin Fenzi <kevin@scrye.com> - 1.27.1-1
- Initial version for epel7
