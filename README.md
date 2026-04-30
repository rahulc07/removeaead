## Description
This is a very simple kernel module that disables aead crypto in kernels where algif\_aead is built-in. You do not need this if algif\_aead is built as an external module.

This prevents CVE-2026-31431 exploits and secures machines until updated kernels are available, installed and machines rebooted.

## RPMs
I also include a spec file for building kernel modules on recent RHEL releases. RPM will autoload the module and configure the system for loading it at the boot time.

A few pre-built rpms for RHEL 8 and 9.6/9.7 can be found here:
 - [kernel 4.18.0-553.117.1.el8_10.x86_64](http://springdale.princeton.edu/data/springdale/unsupported/8.10/x86_64/kmod-removeaead-1.0-0.sdl8.1.x86_64.rpm)
 - [kernel 5.14.0-570.40.1.el9_5.x86_64](http://springdale.princeton.edu/data/springdale/unsupported/9.5/x86_64/kmod-removeaead-1.0-0.sdl9.1.x86_64.rpm)
 - [kernel 5.14.0-570.73.1.el9_6.x86_64](http://springdale.princeton.edu/data/springdale/unsupported/9.7/x86_64/kmod-removeaead-1.0-0.sdl9.1.x86_64.rpm)
 - [kernel 5.14.0-570.106.1.el9_6.x86_64](http://springdale.princeton.edu/data/springdale/unsupported/9.7/x86_64/kmod-removeaead-1.0-1.sdl9.1.x86_64.rpm)
 - [kernel 5.14.0-611.16.1.el9_7.x86_64](http://springdale.princeton.edu/data/springdale/unsupported/9.7/x86_64/kmod-removeaead-1.0-1.sdl9.1.611.16.1.x86_64.rpm)
 - [kernel 5.14.0-611.42.1.el9_7.x86_64](http://springdale.princeton.edu/data/springdale/unsupported/9.7/x86_64/kmod-removeaead-1.0-1.sdl9.2.x86_64.rpm)

src.rpms can be found in appropriate SRPM directories.
