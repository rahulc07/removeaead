# Define the kmod package name here.
%global kmod_name removeaead

# If kmod_kernel_version isn't defined on the rpmbuild line, define it here.
%{!?kmod_kernel_version: %define kmod_kernel_version %(uname -r | sed 's/\.x86_64//')}

%ifarch aarch64
%define kbase kernel-64k
%define asuffix +64k
%else
%define kbase kernel
%define asuffix %{nil}
%endif

Name:		kmod-removeaead
Version:	1.0
# Taken over by kmodtool
Release:	1%{?dist}.2
Summary:	Disable aead
Group:		System Environment/Kernel
License:	GPL
Source:		removeaead.tgz

%define findpat %( echo "%""P" )
%define __find_requires /usr/lib/rpm/redhat/find-requires.ksyms
%define __find_provides /usr/lib/rpm/redhat/find-provides.ksyms %{kmod_name} %{?epoch:%{epoch}:}%{version}-%{release}
%define dup_state_dir %{_localstatedir}/lib/rpm-state/kmod-dups
%define kver_state_dir %{dup_state_dir}/kver
%define kver_state_file %{kver_state_dir}/%{kmod_kernel_version}.%{_arch}
%define dup_module_list %{dup_state_dir}/rpm-kmod-%{kmod_name}-modules
%define debug_package %{nil}

%global _use_internal_dependency_generator 0
%global kernel_source() %{_usrsrc}/kernels/%{kmod_kernel_version}.%{_arch}%{asuffix}

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)=

ExclusiveArch:  x86_64

BuildRequires:  elfutils-libelf-devel
BuildRequires:  %{kbase} = %{kmod_kernel_version}
BuildRequires:  %{kbase}-devel = %{kmod_kernel_version}
BuildRequires:  %{kbase}-abi-stablelists = %{kmod_kernel_version}
BuildRequires:  kernel-rpm-macros
BuildRequires:  redhat-rpm-config

Provides:       %{kbase}-modules >= %{kmod_kernel_version}.%{_arch}
Provides:       kmod-%{kmod_name} = %{?epoch:%{epoch}:}%{version}-%{release}

Requires(post): %{_sbindir}/weak-modules
Requires(postun):       %{_sbindir}/weak-modules
Requires:       %{kbase} >= %{kmod_kernel_version}

%description
Remove aead

%prep
#setup -T -c -n %{name}-%{version} -a 0
%setup -q -n removeaead

%build
export KDIR="%{kernel_source}"
make KVER="%{kmod_kernel_version}" KDIR="%{kernel_source}" \
	KERNEL_UNAME="%{kmod_kernel_version}" SYSSRC="%{kernel_source}" \
	KERNELVER=$(echo %{kmod_kernel_version} | sed "s/[\.-]/_/g"|sed "s/\([0-9]*_[0-9]*_[0-9]*_[0-9]*\).*/\1/") KERNELDIR="%{kernel_source}" \
	KERNEL="%{kmod_kernel_version}.%{_arch}" PROCPROC=AMD SFMP=%{with sfmp} \

whitelist="/lib/modules/kabi-current/kabi_whitelist_%{_target_cpu}"
for modules in $( find . -name "*.ko" -type f -printf "%{findpat}\n" | sed 's|\.ko$||' | sort -u ) ; do
        # update greylist
        nm -u ./$modules.ko | sed 's/.*U //' |  sed 's/^\.//' | sort -u | while read -r symbol; do
                grep -q "^\s*$symbol\$" $whitelist || echo "$symbol" >> ./greylist
        done
done
sort -u greylist | uniq > greylist.txt

%install
%{__install} -d %{buildroot}/lib/modules/%{kmod_kernel_version}.%{_arch}%{asuffix}/extra/%{kmod_name}/
%{__install} *.ko %{buildroot}/lib/modules/%{kmod_kernel_version}.%{_arch}%{asuffix}/extra/%{kmod_name}/
#%{__install} -d %{buildroot}/usr/share/removeaead/devel/
#%{__install} Module.symvers removeaead/nv-p2p.h %{buildroot}/usr/share/nvidia/devel/
#{__install} -d %{buildroot}%{_sysconfdir}/depmod.d/
#{__install} -m 0644 kmod-%{kmod_name}.conf %{buildroot}%{_sysconfdir}/depmod.d/
%{__install} -d %{buildroot}%{_defaultdocdir}/kmod-%{kmod_name}-%{version}/
#{__install} -m 0644 %{SOURCE5} %{buildroot}%{_defaultdocdir}/kmod-%{kmod_name}-%{version}/
%{__install} -m 0644 greylist.txt %{buildroot}%{_defaultdocdir}/kmod-%{kmod_name}-%{version}/

mkdir -p %{buildroot}/etc/modules-load.d/
echo removeaead > %{buildroot}/etc/modules-load.d/removeaead.conf

# strip the modules(s)
find %{buildroot} -type f -name \*.ko -exec %{__strip} --strip-debug \{\} \;

# Sign the modules(s)
%if %{?_with_modsign:1}%{!?_with_modsign:0}
        # If the module signing keys are not defined, define them here.
        %{!?privkey: %define privkey %{_sysconfdir}/pki/SECURE-BOOT-KEY.priv}
        %{!?pubkey: %define pubkey %{_sysconfdir}/pki/SECURE-BOOT-KEY.der}
        for module in $(find %{buildroot} -type f -name \*.ko);
                do %{_usrsrc}/kernels/%{kmod_kernel_version}.%{_arch}/scripts/sign-file \
                sha256 %{privkey} %{pubkey} $module;
        done
%endif

%clean
%{__rm} -rf %{buildroot}

%post
if [ -e "/boot/System.map-%{kmod_kernel_version}.%{_arch}%{asuffix}" ]; then
    /usr/sbin/depmod -aeF "/boot/System.map-%{kmod_kernel_version}.%{_arch}%{asuffix}" "%{kmod_kernel_version}.%{_arch}%{asuffix}" > /dev/null || :
fi

modules=( $(find /lib/modules/%{kmod_kernel_version}.%{_arch}%{asuffix}/extra/%{kmod_name} | grep '\.ko$') )
if [ -x "/usr/sbin/weak-modules" ]; then
	printf '%s\n' "${modules[@]}" | %{_sbindir}/weak-modules --add-modules
fi
/usr/sbin/modprobe removeaead

%preun
rpm -ql kmod-%{kmod_name}-%{version}-%{release}.%{_arch} | grep '\.ko$' > /var/run/rpm-kmod-removeaead-fs-modules

%postun
if [ -e "/boot/System.map-%{kmod_kernel_version}.%{_arch}%{asuffix}" ]; then
    /usr/sbin/depmod -aeF "/boot/System.map-%{kmod_kernel_version}.%{_arch}%{asuffix}" "%{kmod_kernel_version}.%{_arch}%{asuffix}" > /dev/null || :
fi

modules=( $(cat "/var/run/rpm-kmod-removeaead-fs-modules") )
if [ -x "/usr/sbin/weak-modules" ]; then
	printf '%s\n' "${modules[@]}" | %{_sbindir}/weak-modules --remove-modules
fi

%files
%defattr(644,root,root,755)
/lib/modules/%{kmod_kernel_version}.%{_arch}%{asuffix}/extra
%doc /usr/share/doc/kmod-%{kmod_name}-%{version}/
/etc/modules-load.d/removeaead.conf

%changelog
* Thu Dec 05 2024 Josko Plazonic <plazonic@princeton.edu>
- initial build
