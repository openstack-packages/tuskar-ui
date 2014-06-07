Name:	      openstack-tuskar-ui
Version:	  0.1.0
Release:	  17%{?dist}
Summary:	  The UI component for Tuskar

Group:		  Applications/System
License:	  ASL 2.0
URL:		    https://github.com/openstack/tuskar-ui
Source0:	  https://pypi.python.org/packages/source/t/tuskar-ui/tuskar-ui-%{version}.tar.gz

Patch0:     0001-Fixing-manifest.in.patch
Patch1:     0003-Init-code-for-Instack-Undercloud.patch
Patch2:     0004-Adding-missing-setup-for-instack.patch
Patch3:     0005-Default-GlanceLogFile-template-parameter-value.patch
Patch4:     0006-Import-keystoneclient.apiclient.exceptions.patch
Patch5:     0007-Ensure-ipmi-username-and-password-are-set.patch

BuildArch:     noarch

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-lockfile
BuildRequires: python-pbr
BuildRequires: python-sphinx >= 1.1.3
BuildRequires: python-flake8
BuildRequires: python-coverage
BuildRequires: Django
BuildRequires: python-django
BuildRequires: python-django-horizon
BuildRequires: openstack-dashboard
BuildRequires: python-nose
BuildRequires: python-nose-xcover
BuildRequires: python-django-nose
BuildRequires: python-openstack-nose-plugin
BuildRequires: python-nose-exclude
BuildRequires: python-mock
BuildRequires: python-mox
BuildRequires: python-tuskarclient
BuildRequires: python-ironicclient
BuildRequires: tree

Requires: Django
Requires: python-django
Requires: python-django-compressor
Requires: python-django-openstack-auth
Requires: pytz
Requires: openstack-dashboard
Requires: python-lockfile
Requires: python-netaddr
Requires: python-pbr
Requires: python-eventlet
Requires: python-kombu
Requires: python-iso8601
Requires: python-oslo-config
Requires: python-lockfile
Requires: python-cinderclient
Requires: python-novaclient
Requires: python-keystoneclient
Requires: python-heatclient
Requires: python-glanceclient
Requires: python-neutronclient
Requires: python-ceilometerclient
Requires: python-swiftclient
Requires: python-ironicclient
Requires: python-tuskarclient


%description
tuskar-ui is a user interface for Tuskar, a management API for OpenStack
deployments. It is a plugin for OpenStack Horizon.

%prep
%setup -q -n tuskar-ui-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
rm -rf tuskar_ui.egg-info/

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt tools/{pip,test}-requires

%build
export OSLO_PACKAGE_VERSION=%{version}
%{__python2} setup.py build

%install
export OSLO_PACKAGE_VERSION=%{version}
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

# Move config to horizon
mkdir -p  %{buildroot}%{_sysconfdir}/openstack-dashboard/enabled
mkdir -p  %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled
mv _50_tuskar.py.example %{buildroot}%{_sysconfdir}/openstack-dashboard/enabled/_50_tuskar.py
ln -s %{_sysconfdir}/openstack-dashboard/enabled/_50_tuskar.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_50_tuskar.py

# Move static files to horizon. These require that you compile them again
# post install { python manage.py compress }
mkdir -p  %{buildroot}%{_datadir}/openstack-dashboard/static/infrastructure
cp -r tuskar_ui/infrastructure/static/infrastructure/* %{buildroot}%{_datadir}/openstack-dashboard/static/infrastructure/

%files
%doc LICENSE README.rst
%dir %{python_sitelib}/tuskar_ui
%{python_sitelib}/*.egg-info
%{python_sitelib}/tuskar_ui/*.py*
%{python_sitelib}/tuskar_ui/test
%{python_sitelib}/tuskar_ui/infrastructure
%{python_sitelib}/tuskar_ui/infrastructure/templates
%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_50_tuskar.py*
%dir %{_datadir}/openstack-dashboard/static/infrastructure
%{_datadir}/openstack-dashboard/static/infrastructure/js
%{_datadir}/openstack-dashboard/static/infrastructure/less
%{_datadir}/openstack-dashboard/static/infrastructure/tests
%{_datadir}/openstack-dashboard/static/infrastructure/angular_templates
%{_sysconfdir}/openstack-dashboard/enabled/_50_tuskar.py*

%check
# don't run tests on rhel
%if 0%{?rhel} == 0
# until django-1.6 support for tests is enabled, disable tests
export PYTHONPATH=$PYTHONPATH:%{_datadir}/openstack-dashboard
./run_tests.sh -N -P
%endif

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 09 2014 Jordan OMara <jomara@redhat.com> - 0.1.0-15
- IPMI form patch (jomara@redhat.com)

* Tue May 06 2014 Jordan OMara <jomara@redhat.com> - 0.1.0-14
- updated upstream patch w/ fixed escaping (jomara@redhat.com)

* Thu May 01 2014 Jordan OMara <jomara@redhat.com> - 0.1.0-13
- less confused patches from upstream (jomara@redhat.com)

* Thu May 01 2014 Jordan OMara <jomara@redhat.com> - 0.1.0-12
- Glance logfile & keystone api import fix (jomara@redhat.com)

* Wed Apr 30 2014 Jordan OMara <jomara@redhat.com> - 0.1.0-11
- Upstream instack comment patches

* Wed Apr 09 2014 Jordan OMara <jomara@redhat.com> - 0.1.0-10
- Explicit *.html callout

* Wed Apr 09 2014 Jordan OMara <jomara@redhat.com> - 0.1.0-8
- Github source is not sdist- moving to pypi

* Wed Apr 09 2014 Jordan OMara <jomara@redhat.com> - 0.1.0-7
- Correct upstream source now

* Tue Apr 08 2014 Jordan OMara <jomara@redhat.com> - 0.1.0-6
- Add unit tests

* Tue Apr 08 2014 Jordan OMara <jomara@redhat.com> - 0.1.0-5
- Remove .egg-info in %prep

* Mon Apr 07 2014 Jordan OMara <jomara@redhat.com> - 0.1.0-4
- Fixup from review

* Thu Apr 03 2014 Jordan OMara <jomara@redhat.com> - 0.1.0-3
- Added 0001-Missing-import-url.patch

* Tue Apr 01 2014 Jordan OMara <jomara@redhat.com> - 0.1.0-2
- adding infrastructure files to openstack-dashboard install

* Thu Mar 06 2014 Jordan OMara <jomara@redhat.com> - 0.1.0-1
- initial package
