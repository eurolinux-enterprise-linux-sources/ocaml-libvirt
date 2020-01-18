%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

Name:           ocaml-libvirt
Version:        0.6.1.4
Release:        15%{?dist}
Summary:        OCaml binding for libvirt
License:        LGPLv2+

URL:            http://libvirt.org/ocaml/
Source0:        http://libvirt.org/sources/ocaml/%{name}-%{version}.tar.gz

ExcludeArch:    s390 s390x

# Upstream patch to fix int types.
Patch1:         0001-Use-C99-standard-int64_t-instead-of-OCaml-defined-an.patch

# Upstream patch to add virDomainCreateXML binding.
Patch2:         0001-Add-a-binding-for-virDomainCreateXML.patch

# Upstream patches to fix error handling.
Patch3:         0001-Suppress-errors-to-stderr-and-use-thread-local-virEr.patch
Patch4:         0002-Don-t-bother-checking-return-from-virInitialize.patch

# Upstream patch to remove unused function.
Patch5:         0001-Remove-unused-not_supported-function.patch

# Upstream patches to tidy up warnings.
Patch6:         0001-Use-g-warn-error.patch
Patch7:         0002-Update-dependencies.patch

# Upstream patches to add binding for virConnectGetAllDomainStats.
Patch8:         0003-Add-a-binding-for-virConnectGetAllDomainStats-RHBZ-1.patch
Patch9:         0004-examples-Print-more-stats-in-the-get_all_domain_stat.patch
Patch10:        0005-Change-binding-of-virConnectGetAllDomainStats-to-ret.patch

BuildRequires:  ocaml >= 3.10.0
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-findlib-devel

BuildRequires:  libvirt-devel >= 0.2.1
BuildRequires:  perl
BuildRequires:  gawk


%description
OCaml binding for libvirt.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%prep
%setup -q

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1


%build
%configure
# This conditional is due to ocamlc.opt crashing on i686 in the
# examples/ directory.  Can remove this (ie. revert back to what's
# in Fedora) when we update RHEL 7 to a newer OCaml version.
%ifnarch %{ix86}
make all doc
%else
make -C libvirt all
make doc
%endif
%if %opt
make opt
%endif


%install
# These rules work if the library uses 'ocamlfind install' to install itself.
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
mkdir -p $RPM_BUILD_ROOT%{_bindir}
%if %opt
make install-opt
%else
make install-byte
%endif


%files
%doc COPYING.LIB README ChangeLog
%{_libdir}/ocaml/libvirt
%if %opt
%exclude %{_libdir}/ocaml/libvirt/*.a
%exclude %{_libdir}/ocaml/libvirt/*.cmxa
%exclude %{_libdir}/ocaml/libvirt/*.cmx
%endif
%exclude %{_libdir}/ocaml/libvirt/*.mli
%{_libdir}/ocaml/stublibs/*.so
%{_libdir}/ocaml/stublibs/*.so.owner


%files devel
%doc COPYING.LIB README TODO.libvirt ChangeLog html/*
%if %opt
%{_libdir}/ocaml/libvirt/*.a
%{_libdir}/ocaml/libvirt/*.cmxa
%{_libdir}/ocaml/libvirt/*.cmx
%endif
%{_libdir}/ocaml/libvirt/*.mli


%changelog
* Wed Mar 29 2017 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.4-15
- Include all changes from Fedora Rawhide
  resolves: rhbz#1390171

* Fri Aug 08 2014 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.2-10
- Resolves: rhbz#1125629
- Disable bytecode build of examples.

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.6.1.2-8
- Mass rebuild 2013-12-27

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 29 2012 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.2-6
- Rebuild for OCaml 4.00.1.

* Fri Oct 12 2012 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.2-5
- Modernise the spec file.
- Add upstream patch to remove unnecessary get_cpu_stats second parameter
  (thanks Hu Tao).

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 09 2012 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.2-2
- Rebuild for OCaml 4.00.0.

* Fri Mar 23 2012 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.2-1
- New upstream version 0.6.1.2.

* Tue Mar  6 2012 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.1-1
- New upstream version 0.6.1.1.
- Remove mlvirsh subpackage, no longer upstream.
- Replace custom configure with RPM macro configure.
- Use RPM global instead of define.
- Use built-in RPM OCaml dependency generator.

* Fri Jan 06 2012 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.0-10
- Rebuild for OCaml 3.12.1.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 05 2011 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.0-8
- Rebuild for OCaml 3.12 (http://fedoraproject.org/wiki/Features/OCaml3.12).

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.0-7
- Rebuild for OCaml 3.11.2.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.0-5
- Force rebuild to test FTBFS issue.

* Fri Jun 12 2009 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.0-3
- Force rebuild to test FTBFS issue.

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.0-2
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Tue Mar 10 2009 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.0-1
- New upstream release 0.6.1.0.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.4.2-3
- Rebuild for OCaml 3.11.0+rc1.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.4.2-2
- Rebuild for OCaml 3.11.0

* Wed Jul  9 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.4.2-1
- New upstream version.
- In upstream, 'make install' became 'make install-byte' or 'make install-opt'

* Tue Jun 10 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.2.4-1
- New upstream version.

* Thu Jun  5 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.2.3-1
- New upstream version.

* Thu Jun  5 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.2.2-1
- New upstream version.
- Removed virt-ctrl, virt-df, virt-top subpackages, since these are
  now separate Fedora packages.

* Tue May 20 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.1.1-4
- Disable virt-top (bz 442871).
- Disable virt-ctrl (bz 442875).

* Mon May 19 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.1.1-3
- Disable virt-df (bz 442873).

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.1.1-2
- Rebuild for OCaml 3.10.2

* Thu Mar 20 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.1.1-1
- New upstream release 0.4.1.1.
- Move configure to build section.
- Pass RPM_OPT_FLAGS.

* Tue Mar  4 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.1.0-2
- Fix source URL.
- Install virt-df manpage.

* Tue Mar  4 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.1.0-1
- New upstream release 0.4.1.0.
- Upstream now requires ocaml-dbus >= 0.06, ocaml-lablgtk >= 2.10.0,
  ocaml-dbus-devel.
- Enable virt-df.

* Sat Mar  1 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.0.3-3
- Rebuild for ppc64.

* Wed Feb 13 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.0.3-2
- Add BR gtk2-devel

* Tue Feb 12 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.0.3-1
- New upstream version 0.4.0.3.
- Rebuild for OCaml 3.10.1.

* Tue Nov 20 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.3.4-1
- New upstream release 0.3.3.4.
- Upstream website is now http://libvirt.org/ocaml/

* Fri Oct 19 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.3.0-2
- Mistake: BR is ocaml-calendar-devel.

* Fri Oct 19 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.3.0-1
- New upstream release 0.3.3.0.
- Added support for virt-df, but disabled it by default.
- +BR ocaml-calendar.

* Mon Sep 24 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.2.8-1
- New upstream release 0.3.2.8.

* Thu Sep 20 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.2.7-1
- New upstream release 0.3.2.7.
- Ship the upstream ChangeLog file.

* Thu Sep  6 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.2.6-2
- Force dependency on ocaml >= 3.10.0-7 which has fixed requires/provides
  scripts.

* Thu Sep  6 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.2.6-1
- New upstream version 0.3.2.6.

* Wed Aug 29 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.2.5-1
- New upstream version 0.3.2.5.
- Keep TODO out of the main package, but add (renamed) TODO.libvirt and
  TODO.virt-top to the devel and virt-top packages respectively.
- Add BR gawk.

* Thu Aug 23 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.2.4-1
- New upstream version 0.3.2.4.

* Thu Aug 23 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.2.3-2
- build_* macros so we can choose what subpackages to build.

* Thu Aug 23 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.2.3-1
- Upstream version 0.3.2.3.
- Add missing BR libvirt-devel.

* Wed Aug 22 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.2.2-1
- Upstream version 0.3.2.2.

* Wed Aug 22 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.2.1-2
- Fix unclosed if-statement in spec file.

* Wed Aug 22 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.2.1-1
- Upstream version 0.3.2.1.
- Put HTML documentation in -devel package.

* Mon Aug  6 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.1.2-1
- Initial RPM release.
