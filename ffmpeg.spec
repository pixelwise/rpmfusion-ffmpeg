# TODO: add make test to %%check section

#global branch  oldabi-
#global date    20110612
#global rel     rc1

# Cuda and others are only available on some arches
%global cuda_arches x86_64 i686

%if 0%{?fedora} >= 25
# OpenCV 3.X has an overlinking issue - unsuitable for core libraries
# Reported as https://github.com/opencv/opencv/issues/7001
%global _without_opencv   1
%endif

%if 0%{?rhel}
%global _without_frei0r   1
%global _without_opencv   1
%global _without_vpx      1
%global _without_nvenc    1
%endif

# flavor nonfree
%if 0%{?_with_nonfree:1}
%global flavor           -nonfree
%global progs_suffix     -nonfree
#global build_suffix     -lgpl
%ifarch %{cuda_arches}
%global _with_cuda       1
%global _with_cuvid      1
%global _with_libnpp     1
%endif
%global _with_fdk_aac    1
%global _without_cdio    1
%global _without_frei0r  1
%global _without_gpl     1
%global _without_x264    1
%global _without_x265    1
%global _without_xvid    1
%endif

# Disable nvenc when not relevant
%ifnarch %{cuda_arches}
%global _without_nvenc    1
%endif

# extras flags
%if 0%{!?_without_nvenc:1}
%global nvenc_cflags -I%{_includedir}/nvenc
%endif
%if 0%{?_with_cuda}
%global cuda_cflags $(pkg-config --cflags cuda-8.0)
%global cuda_ldflags -L%{_libdir}/nvidia
%endif

%if 0%{?_with_libnpp}
%global libnpp_cflags $(pkg-config --cflags nppi-8.0 nppc-8.0)
%global libnpp_ldlags $(pkg-config --libs-only-L nppi-8.0 nppc-8.0)
%endif

%if 0%{?_without_gpl}
%global lesser L
%endif

%if 0%{!?_without_amr} || 0%{?_with_gmp} || 0%{?_with_smb}
%global ffmpeg_license %{?lesser}GPLv3+
%else
%global ffmpeg_license %{?lesser}GPLv2+
%endif

Summary:        Digital VCR and streaming server
Name:           ffmpeg%{?flavor}
Version:        3.3.2
Release:        1%{?date}%{?date:git}%{?rel}%{?dist}
License:        %{ffmpeg_license}
URL:            http://ffmpeg.org/
%if 0%{?date}
Source0:        ffmpeg-%{?branch}%{date}.tar.bz2
%else
Source0:        http://ffmpeg.org/releases/ffmpeg-%{version}.tar.xz
%endif
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
%{?_with_cuda:BuildRequires: cuda-driver-dev-8-0 cuda-misc-headers-8-0 cuda-drivers-devel%{_isa}}
%{?_with_libnpp:BuildRequires: cuda-cudart-dev-8-0 cuda-misc-headers-8-0 cuda-npp-dev-8-0}
BuildRequires:  bzip2-devel
%{?_with_faac:BuildRequires: faac-devel}
%{?_with_fdk_aac:BuildRequires: fdk-aac-devel}
%{?_with_flite:BuildRequires: flite-devel}
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
%{!?_without_frei0r:BuildRequires: frei0r-devel}
%{?_with_gme:BuildRequires: game-music-emu-devel}
BuildRequires:  gnutls-devel
BuildRequires:  gsm-devel
%{?_with_ilbc:BuildRequires: ilbc-devel}
BuildRequires:  lame-devel >= 3.98.3
%{!?_without_jack:BuildRequires: jack-audio-connection-kit-devel}
%{!?_without_ladspa:BuildRequires: ladspa-devel}
BuildRequires:  libass-devel
BuildRequires:  libbluray-devel
%{?_with_bs2b:BuildRequires: libbs2b-devel}
%{?_with_caca:BuildRequires: libcaca-devel}
%{!?_without_cdio:BuildRequires: libcdio-paranoia-devel}
%{?_with_chromaprint:BuildRequires: libchromaprint-devel}
#libcrystalhd is currently broken
%{?_with_crystalhd:BuildRequires: libcrystalhd-devel}
%if 0%{?_with_ieee1394}
BuildRequires:  libavc1394-devel
BuildRequires:  libdc1394-devel
BuildRequires:  libiec61883-devel
%endif
BuildRequires:  libgcrypt-devel
BuildRequires:  libGL-devel
Buildrequires:  libmodplug-devel
%{?_with_rtmp:BuildRequires: librtmp-devel}
%{?_with_smb:BuildRequires: libsmbclient-devel}
%{?_with_ssh:BuildRequires: libssh-devel}
BuildRequires:  libtheora-devel
BuildRequires:  libv4l-devel
BuildRequires:  libvdpau-devel
BuildRequires:  libvorbis-devel
%{?!_without_vpx:BuildRequires: libvpx-devel >= 0.9.1}
%ifarch %{ix86} x86_64
%{!?_without_mfx:BuildRequires: libmfx-devel}
BuildRequires:  libXvMC-devel
%{?!_without_vaapi:BuildRequires: libva-devel >= 0.31.0}
BuildRequires:  yasm
%endif
%{?_with_webp:BuildRequires: libwebp-devel}
%{?_with_netcdf:BuildRequires: netcdf-devel}
%{!?_without_nvenc:BuildRequires: nvenc-devel}
%{!?_without_amr:BuildRequires: opencore-amr-devel vo-amrwbenc-devel}
%{!?_without_openal:BuildRequires: openal-soft-devel}
%if 0%{!?_without_opencl:1}
BuildRequires:  opencl-headers ocl-icd-devel
%{?fedora:Recommends: opencl-icd}
%endif
%{!?_without_opencv:BuildRequires: opencv-devel}
BuildRequires:  openjpeg2-devel
BuildRequires:  opus-devel
%{!?_without_pulse:BuildRequires: pulseaudio-libs-devel}
BuildRequires:  perl(Pod::Man)
%{?_with_rubberband:BuildRequires: rubberband-devel}
BuildRequires:  schroedinger-devel
%{!?_without_tools:BuildRequires: SDL2-devel}
%{?_with_snappy:BuildRequires: snappy-devel}
BuildRequires:  soxr-devel
BuildRequires:  speex-devel
BuildRequires:  subversion
%{?_with_tesseract:BuildRequires: tesseract-devel}
#BuildRequires:  texi2html
BuildRequires:  texinfo
%{?_with_twolame:BuildRequires: twolame-devel}
%{?_with_wavpack:BuildRequires: wavpack-devel}
%{!?_without_x264:BuildRequires: x264-devel >= 0.0.0-0.31}
%{!?_without_x265:BuildRequires: x265-devel}
%{!?_without_xvid:BuildRequires: xvidcore-devel}
BuildRequires:  zlib-devel
%{?_with_zmq:BuildRequires: zeromq-devel}
%{?_with_zvbi:BuildRequires: zvbi-devel}

%description
FFmpeg is a complete and free Internet live audio and video
broadcasting solution for Linux/Unix. It also includes a digital
VCR. It can encode in real time in many formats including MPEG1 audio
and video, MPEG4, h263, ac3, asf, avi, real, mjpeg, and flash.

%package        libs
Summary:        Libraries for %{name}

%description    libs
FFmpeg is a complete and free Internet live audio and video
broadcasting solution for Linux/Unix. It also includes a digital
VCR. It can encode in real time in many formats including MPEG1 audio
and video, MPEG4, h263, ac3, asf, avi, real, mjpeg, and flash.
This package contains the libraries for %{name}

%package     -n libavdevice%{?flavor}
Summary:        Special devices muxing/demuxing library

%description -n libavdevice%{?flavor}
Libavdevice is a complementary library to libavf "libavformat". It provides
various "special" platform-specific muxers and demuxers, e.g. for grabbing
devices, audio capture and playback etc.

%package        devel
Summary:        Development package for %{name}
Requires:       %{name}-libs%{_isa} = %{version}-%{release}
Requires:       libavdevice%{?flavor}%{_isa} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
FFmpeg is a complete and free Internet live audio and video
broadcasting solution for Linux/Unix. It also includes a digital
VCR. It can encode in real time in many formats including MPEG1 audio
and video, MPEG4, h263, ac3, asf, avi, real, mjpeg, and flash.
This package contains development files for %{name}

# Don't use the %%configure macro as this is not an autotool script
%global ff_configure \
./configure \\\
    --prefix=%{_prefix} \\\
    --bindir=%{_bindir} \\\
    --datadir=%{_datadir}/%{name} \\\
    --docdir=%{_docdir}/%{name} \\\
    --incdir=%{_includedir}/%{name} \\\
    --libdir=%{_libdir} \\\
    --mandir=%{_mandir} \\\
    --arch=%{_target_cpu} \\\
    --optflags="%{optflags}" \\\
    --extra-ldflags="%{?__global_ldflags} %{?cuda_ldflags} %{?libnpp_ldlags}" \\\
    --extra-cflags="%{?nvenc_cflags} %{?cuda_cflags} %{?libnpp_cflags}" \\\
    %{?flavor:--disable-manpages} \\\
    %{?progs_suffix:--progs-suffix=%{progs_suffix}} \\\
    %{?build_suffix:--build-suffix=%{build_suffix}} \\\
    %{!?_without_amr:--enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libvo-amrwbenc --enable-version3} \\\
    --enable-bzlib \\\
    %{?_with_chromaprint:--enable-chromaprint} \\\
    %{!?_with_crystalhd:--disable-crystalhd} \\\
    --enable-fontconfig \\\
    %{!?_without_frei0r:--enable-frei0r} \\\
    --enable-gcrypt \\\
    %{?_with_gmp:--enable-gmp --enable-version3} \\\
    --enable-gnutls \\\
    %{!?_without_ladspa:--enable-ladspa} \\\
    --enable-libass \\\
    --enable-libbluray \\\
    %{?_with_bs2b:--enable-libbs2b} \\\
    %{?_with_caca:--enable-libcaca} \\\
    %{?_with_cuda:--enable-cuda --enable-nonfree} \\\
    %{?_with_cuvid:--enable-cuvid --enable-nonfree} \\\
    %{!?_without_cdio:--enable-libcdio} \\\
    %{?_with_ieee1394:--enable-libdc1394 --enable-libiec61883} \\\
    %{?_with_faac:--enable-libfaac --enable-nonfree} \\\
    %{?_with_fdk_aac:--enable-libfdk-aac --enable-nonfree} \\\
    %{?_with_flite:--enable-libflite} \\\
    %{!?_without_jack:--enable-indev=jack} \\\
    --enable-libfreetype \\\
    --enable-libfribidi \\\
    %{?_with_gme:--enable-libgme} \\\
    --enable-libgsm \\\
    %{?_with_ilbc:--enable-libilbc} \\\
    %{?_with_libnpp:--enable-libnpp --enable-nonfree} \\\
    --enable-libmp3lame \\\
    %{?_with_netcdf:--enable-netcdf} \\\
    %{!?_without_nvenc:--enable-nvenc} \\\
    %{!?_without_openal:--enable-openal} \\\
    %{!?_without_opencl:--enable-opencl} \\\
    %{!?_without_opencv:--enable-libopencv} \\\
    %{!?_without_opengl:--enable-opengl} \\\
    --enable-libopenjpeg \\\
    --enable-libopus \\\
    %{!?_without_pulse:--enable-libpulse} \\\
    %{?_with_rtmp:--enable-librtmp} \\\
    %{?_with_rubberband:--enable-librubberband} \\\
    --enable-libschroedinger \\\
    %{?_with_smb:--enable-libsmbclient} \\\
    %{?_with_snappy:--enable-libsnappy} \\\
    --enable-libsoxr \\\
    --enable-libspeex \\\
    %{?_with_ssh:--enable-libssh} \\\
    %{?_with_tesseract:--enable-libtesseract} \\\
    --enable-libtheora \\\
    %{?_with_twolame:--enable-libtwolame} \\\
    --enable-libvorbis \\\
    --enable-libv4l2 \\\
    %{!?_without_vpx:--enable-libvpx} \\\
    %{?_with_webp:--enable-libwebp} \\\
    %{!?_without_x264:--enable-libx264} \\\
    %{!?_without_x265:--enable-libx265} \\\
    %{!?_without_xvid:--enable-libxvid} \\\
    %{?_with_zmq:--enable-libzmq} \\\
    %{?_with_zvbi:--enable-libzvbi} \\\
    --enable-avfilter \\\
    --enable-avresample \\\
    --enable-postproc \\\
    --enable-pthreads \\\
    --disable-static \\\
    --enable-shared \\\
    %{!?_without_gpl:--enable-gpl} \\\
    --disable-debug \\\
    --disable-stripping


%prep
%if 0%{?date}
%setup -q -n ffmpeg-%{?branch}%{date}
echo "git-snapshot-%{?branch}%{date}-RPMFusion" > VERSION
%else
%setup -q -n ffmpeg-%{version}
%endif
# fix -O3 -g in host_cflags
sed -i "s|check_host_cflags -O3|check_host_cflags %{optflags}|" configure
mkdir -p _doc/examples
cp -pr doc/examples/{*.c,Makefile,README} _doc/examples/

%build
%{ff_configure}\
    --shlibdir=%{_libdir} \
%if 0%{?_without_tools:1}
    --disable-doc \
    --disable-ffmpeg --disable-ffplay --disable-ffprobe --disable-ffserver \
%else
%ifarch %{ix86}
    --cpu=%{_target_cpu} \
%endif
%ifarch %{ix86} x86_64
    %{!?_without_qsv:--enable-libmfx} \
%endif
%ifarch %{ix86} x86_64 ppc ppc64
    --enable-runtime-cpudetect \
%endif
%ifarch ppc
    --cpu=g3 \
    --enable-pic \
%endif
%ifarch ppc64
    --cpu=g5 \
    --enable-pic \
%endif
%ifarch %{arm}
    --disable-runtime-cpudetect --arch=arm \
%ifarch armv6hl
    --cpu=armv6 \
%else
    --enable-thumb \
%endif
%ifarch armv7hnl
    --enable-neon \
%endif
%endif
%endif

%make_build V=1
make documentation V=1
make alltools V=1

%install
%make_install V=1
%if 0%{!?flavor:1}
rm -r %{buildroot}%{_datadir}/%{name}/examples
%endif
%if 0%{!?progs_suffix:1}
install -pm755 tools/qt-faststart %{buildroot}%{_bindir}
%endif

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%post -n libavdevice%{?flavor} -p /sbin/ldconfig

%postun -n libavdevice%{?flavor} -p /sbin/ldconfig

%if 0%{!?_without_tools:1}
%files
%doc COPYING.* CREDITS README.md doc/ffserver.conf
%{_bindir}/ffmpeg%{?progs_suffix}
%{_bindir}/ffplay%{?progs_suffix}
%{_bindir}/ffprobe%{?progs_suffix}
%{_bindir}/ffserver%{?progs_suffix}
%{!?progs_suffix:%{_bindir}/qt-faststart}
%{!?flavor:
%{_mandir}/man1/ffmpeg*.1*
%{_mandir}/man1/ffplay*.1*
%{_mandir}/man1/ffprobe*.1*
%{_mandir}/man1/ffserver*.1*
}
%{_datadir}/%{name}
%endif

%files libs
%{_libdir}/lib*.so.*
%exclude %{_libdir}/libavdevice%{?build_suffix}.so.*
%{!?flavor:%{_mandir}/man3/lib*.3.gz
%exclude %{_mandir}/man3/libavdevice.3*
}

%files -n libavdevice%{?flavor}
%{_libdir}/libavdevice%{?build_suffix}.so.*
%{!?flavor:%{_mandir}/man3/libavdevice.3*}

%files devel
%doc MAINTAINERS doc/APIchanges doc/*.txt
%doc _doc/examples
%{!?flavor:%doc %{_docdir}/%{name}/*.html}
%{_includedir}/%{name}
%{_libdir}/pkgconfig/lib*.pc
%{_libdir}/lib*.so


%changelog
* Wed Jun 07 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.3.2-1
- Updated to 3.3.2

* Mon May 15 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.3.1-1
- Updated to 3.3.1

* Wed Apr 19 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.3-1
- Updated to 3.3
- Make nvenc x86 only
- Remove obsolete x11grab configure option

* Sun Mar 19 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 3.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Feb 11 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.2.4-1
- Updated to 3.2.4

* Mon Feb 06 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.2.3-1
- Updated to 3.2.3

* Tue Jan 03 2017 Dominik Mierzejewski <rpm@greysector.net> - 3.2.2-3
- rebuild for x265

* Mon Jan 02 2017 Dominik Mierzejewski <rpm@greysector.net> - 3.2.2-2
- enable optional nonfree build with cuda, cuvid, npp and fdk-aac
  (most credit for this goes to Nicolas Chauvet)
- allow disabling x11grab (conflicts with nonfree builds)
- use Recommends only on Fedora (patch by Nicolas Chauvet)
- enable AMR codecs by default (rfbz#4367, patch by Nicolas Chauvet)

* Tue Dec 06 2016 Julian Sikorski <belegdol@fedoraproject.org> - 3.2.2-1
- Updated to 3.2.2

* Sat Nov 26 2016 Julian Sikorski <belegdol@fedoraproject.org> - 3.2.1-1
- Updated to 3.2.1

* Wed Nov 16 2016 Adrian Reber <adrian@lisas.de> - 3.2-3
- Rebuild for libcdio-0.94

* Tue Nov 08 2016 Sérgio Basto <sergio@serjux.com> - 3.2-2
- Rebuild for x265-2.1

* Sat Oct 29 2016 Julian Sikorski <belegdol@fedoraproject.org> - 3.2-1
- Updated to 3.2
- Dropped openjpeg2 patch
- Updated BuildRequires to SDL2-devel
- Incorporated some cleanups from RF #4243

* Tue Oct 25 2016 Julian Sikorski <belegdol@fedoraproject.org> - 3.1.5-1
- Updated to 3.1.5

* Sat Oct 01 2016 Leigh Scott <leigh123linux@googlemail.com> - 3.1.4-2
- Fix missing libxvid (rfbz#4274)

* Sat Oct 01 2016 Julian Sikorski <belegdol@fedoraproject.org> - 3.1.4-1
- Updated to 3.1.4

* Thu Sep 08 2016 Nicolas Chauvet <kwizart@gmail.com> - 3.1.3-3
- Disable OpenCV for Fedora >= 25

* Sat Sep 03 2016 Dominik Mierzejewski <rpm@greysector.net> - 3.1.3-2
- enable QSV support by default, since libmfx is in Fedora now
- QSV is x86 only
- put x86-specific BRs in one place

* Sat Aug 27 2016 Julian Sikorski <belegdol@fedoraproject.org> - 3.1.3-1
- Updated to 3.1.3

* Thu Aug 25 2016 Leigh Scott <leigh123linux@googlemail.com> - 3.1.2-2
- enable support for nvenc

* Wed Aug 10 2016 Julian Sikorski <belegdol@fedoraproject.org> - 3.1.2-1
- Updated to 3.1.2

* Wed Jul 27 2016 Julian Sikorski <belegdol@fedoraproject.org> - 3.1.1-1
- Updated to 3.1.1
- Dropped included patch
- Added $RPM_LD_FLAGS to %%configure
- Switched to openjpeg2
- Fixed build with openjpeg2-2.1.1 (patch by Sandro Mani)

* Sat Jul 23 2016 Igor Gnatenko <ignatenko@redhat.com> - 3.0.2-5
- Rebuild for libvpx soname bump

* Sun Jul 10 2016 Dominik Mierzejewski <rpm@greysector.net> - 3.0.2-4
- enable jack by default (rfbz#2156)
- re-enable opencl by default (rfbz#3640 was fixed)
- add conditional support for QSV via libmfx (rfbz#4043)
- drop libcelt support (celt 0.11 no longer available in Fedora)
- drop libdirac support (unsupported by FFmpeg)
- make xvidcore support optional
- add missing ldconfig calls for libavdevice package
- move libavdevice manpage to its subpackage
- move examples from main package to -devel as docs
- add support for libiec61883 and make DV (IEEE 1394) support optional
- enable optional support for many external libraries (rfbz#4109)

* Thu Jul 07 2016 Julian Sikorski <belegdol@fedoraproject.org> - 3.0.2-3
- Fixed build failure on rawhide due to newer opencv using a patch from upstream
  git

* Sun Jun 12 2016 Leigh Scott <leigh123linux@googlemail.com> - 3.0.2-2
- rebuilt

* Sat May 14 2016 Michael Kuhn <suraia@ikkoku.de> - 3.0.2-1
- Update to 3.0.2.

* Mon May 02 2016 Julian Sikorski <belegdol@fedoraproject.org> - 2.8.7-1
- Updated to 2.8.7

* Mon Feb 01 2016 Julian Sikorski <belegdol@fedoraproject.org> - 2.8.6-1
- Updated to 2.8.6

* Sat Jan 16 2016 Julian Sikorski <belegdol@fedoraproject.org> - 2.8.5-1
- Updated to 2.8.5

* Wed Dec 23 2015 Julian Sikorski <belegdol@fedoraproject.org> - 2.8.4-1
- Updated to 2.8.4
- Fixed Fraunhofer FDK AAC conditional build (RF # 3898)

* Sun Nov 29 2015 Julian Sikorski <belegdol@fedoraproject.org> - 2.8.3-1
- Updated to 2.8.3

* Sat Nov 14 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.8.2-1
- Update to 2.8.2

* Sat Oct 24 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.8.1-1
- Update to 2.8.1

* Sat Jul 25 2015 Julian Sikorski <belegdol@fedoraproject.org> - 2.6.4-1
- Updated to 2.6.4

* Wed May 27 2015 Julian Sikorski <belegdol@fedoraproject.org> - 2.6.3-1
- Updated to 2.6.3

* Sat May 16 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.6.2-3
- Rebuilt for x265

* Mon May 11 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.6.2-2
- Disable opencl by default - rfbz#3640
- Add with condition for nvenc,fdk_aac

* Tue May 05 2015 Julian Sikorski <belegdol@fedoraproject.org> - 2.6.2-1
- Updated to 2.6.2

* Tue Apr 28 2015 Julian Sikorski <belegdol@fedoraproject.org> - 2.4.9-1
- Updated to 2.4.9

* Wed Apr 15 2015 Dominik Mierzejewski <rpm@greysector.net> - 2.4.8-3
- rebuilt for new x265

* Mon Apr 13 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.4.8-2
- Fix sed for f22 where cflags contains a directory path

* Mon Mar 30 2015 Julian Sikorski <belegdol@fedoraproject.org> - 2.4.8-1
- Updated to 2.4.8

* Sun Feb 15 2015 Julian Sikorski <belegdol@fedoraproject.org> - 2.4.7-1
- Updated to 2.4.7

* Sun Feb 01 2015 Dominik Mierzejewski <rpm at greysector.net> - 2.4.6-3
- enable LADSPA support (rfbz#3134)

* Sun Feb 01 2015 Dominik Mierzejewski <rpm at greysector.net> - 2.4.6-2
- enable OpenCL support
- BR texinfo instead of texi2html to reduce BRs by half
- drop support for building on SPARC (no longer a Fedora Secondary Arch)
- move libavdevice to a subpackage (rfbz#3075)

* Wed Jan 14 2015 Julian Sikorski <belegdol@fedoraproject.org> - 2.4.6-1
- Updated to 2.4.6

* Sun Dec 21 2014 Julian Sikorski <belegdol@fedoraproject.org> - 2.4.5-1
- Updated to 2.4.5

* Thu Dec 18 2014 Dominik Mierzejewski <rpm at greysector.net> - 2.4.4-2
- enable support for libx265 by default (rfbz#3421, patch by Nerijus Baliūnas)

* Mon Dec 01 2014 Julian Sikorski <belegdol@fedoraproject.org> - 2.4.4-1
- Updated to 2.4.4

* Tue Nov 04 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.4.3-2
- Rebuilt for vaapi 0.36

* Sun Nov 02 2014 Julian Sikorski <belegdol@fedoraproject.org> - 2.4.3-1
- Updated to 2.4.3

* Sun Oct 19 2014 Sérgio Basto <sergio@serjux.com> - 2.4.2-1
- Update to ffmpeg-2.4.2

* Fri Oct 03 2014 Julian Sikorski <belegdol@fedoraproject.org> - 2.3.4-1
- Updated to 2.3.4

* Sat Sep 27 2014 kwizart <kwizart@gmail.com> - 2.3.3-3
- Rebuild back to ffmpeg 2.3x

* Sat Sep 13 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.3.3-2
- Disable libcelt by default - rfbz#3359

* Tue Sep 02 2014 Julian Sikorski <belegdol@fedoraproject.org> - 2.3.3-1
- Updated to 2.3.3

* Tue Aug 12 2014 Julian Sikorski <belegdol@fedoraproject.org> - 2.3.2-1
- Updated to 2.3.2

* Sun Aug 03 2014 Julian Sikorski <belegdol@fedoraproject.org> - 2.3.1-1
- Updated to 2.3.1
- README → README.md

* Tue Jul 15 2014 Julian Sikorski <belegdol@fedoraproject.org> - 2.2.5-1
- Updated to 2.2.5

* Tue Jul 08 2014 Julian Sikorski <belegdol@fedoraproject.org> - 2.2.4-1
- Updated to 2.2.4

* Wed Jun 04 2014 Julian Sikorski <belegdol@fedoraproject.org> - 2.2.3-1
- Updated to 2.2.3

* Mon May 05 2014 Julian Sikorski <belegdol@fedoraproject.org> - 2.2.2-1
- Updated to 2.2.2

* Fri Apr 18 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.2.1-1
- Update to 2.2.1

* Mon Mar 24 2014 Julian Sikorski <belegdol@fedoraproject.org> - 2.2-1
- Updated to 2.2

* Fri Mar 21 2014 Julian Sikorski <belegdol@fedoraproject.org> - 2.1.4-4
- Rebuilt for libass-0.10.2

* Tue Mar 18 2014 Julian Sikorski <belegdol@fedoraproject.org> - 2.1.4-3
- Rebuilt for x264

* Thu Mar 06 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.1.4-2
- Rebuilt for x264

* Tue Feb 25 2014 Julian Sikorski <belegdol@fedoraproject.org> - 2.1.4-1
- Updated to 2.1.4

* Thu Jan 16 2014 Julian Sikorski <belegdol@fedoraproject.org> - 2.1.3-1
- Updated to 2.1.3

* Wed Nov 20 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.1.1-1
- Update to 2.1.1

* Tue Oct 29 2013 Julian Sikorski <belegdol@fedoraproject.org> - 2.1-1
- Updated to 2.1

* Tue Oct 22 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.0.2-2
- Rebuilt for x264

* Wed Oct 09 2013 Julian Sikorski <belegdol@fedoraproject.org> - 2.0.2-1
- Updated to 2.0.2

* Mon Sep 30 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.0.1-3
- Rebuilt

* Tue Aug 27 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.0.1-2
- Enable avresample as noticed by Xavier Bachelot

* Tue Aug 13 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.0.1-1
- Update to 2.0.1

* Thu Aug 01 2013 Julian Sikorski <belegdol@fedoraproject.org> - 2.0-1
- Updated to 2.0
- Dropped the no longer needed bogus man dir work-around

* Thu Aug 01 2013 Julian Sikorski <belegdol@fedoraproject.org> - 1.2.2-1
- Updated to 1.2.2

* Sat Jul 20 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.2.1-7
- Rebuilt for x264

* Tue Jul 02 2013 Dominik Mierzejewski <rpm at greysector.net> - 1.2.1-6
- fix building with libcdio

* Mon Jul 01 2013 Dominik Mierzejewski <rpm at greysector.net> - 1.2.1-5
- build with soxr support enabled (rfbz#2853)

* Thu Jun 27 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.2.1-4
- Reverse the logic for neon on arm

* Wed Jun 19 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.2.1-3
- Enable neon on armv7hnl
- Enable thumb on all arm but armv6hl

* Tue May 14 2013 Julian Sikorski <belegdol@fedoraproject.org> - 1.2.1-1
- Updated to 1.2.1

* Sun May 05 2013 Julian Sikorski <belegdol@fedoraproject.org> - 1.2-2
- Rebuilt for x264-0.130

* Mon Mar 18 2013 Julian Sikorski <belegdol@fedoraproject.org> - 1.2-1
- Updated to 1.2

* Mon Mar 18 2013 Julian Sikorski <belegdol@fedoraproject.org> - 1.1.4-1
- Updated to 1.1.4

* Sun Mar 10 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.1.3-1
- Update to 1.1.3

* Sun Jan 20 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.1.1-1
- Update to 1.1.1
- Disable libcdio with fedora 19

* Mon Jan 07 2013 Julian Sikorski <belegdol@fedoraproject.org> - 1.1-1
- Updated to 1.1
- Added new man pages

* Tue Dec 04 2012 Julian Sikorski <belegdol@fedoraproject.org> - 1.0.1-1
- Updated to 1.0.1

* Fri Nov 23 2012 Julian Sikorski <belegdol@fedoraproject.org> - 1.0-5
- Rebuilt for x264-0.128

* Sat Nov 03 2012 Julian Sikorski <belegdol@fedoraproject.org> - 1.0-4
- Fixed -O3 -g in host_cflags
- Made the installation verbose too

* Sat Nov 03 2012 Julian Sikorski <belegdol@fedoraproject.org> - 1.0-3
- Use Fedora %%{optflags}
- Made the build process verbose

* Thu Nov 01 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.0-2
- Add opus
- Enable opencv frei0r by default
- Disable librmtp - use builtin implementation rfbz#2399

* Thu Oct 04 2012 Julian Sikorski <belegdol@fedoraproject.org> - 1.0-1
- Updated to 1.0
- Dropped obsolete Group, Buildroot, %%clean and %%defattr
- Dropped the included patch

* Wed Sep 05 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.11.1-3
- Rebuilt for x264 ABI 125

* Sat Jul 21 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.11.1-2
- Backport fix rfbz#2423

* Thu Jun 14 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.11.1-1
- Updated to 0.11.1

* Wed Jun 13 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.10.4-1
- Updated to 0.10.4

* Mon May 07 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.10.3-1
- Updated to 0.10.3

* Tue May 01 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.10.2-3
- Sync with ffmpeg-compat and EL
- Add BR libmodplug-devel
- Enable libass openal-soft

* Tue Apr 10 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.10.2-2
- Explicitely disable neon unless armv7hnl

* Sun Mar 18 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.10.2-1
- Updated to 0.10.2

* Mon Mar 12 2012 root - 0.10-2
- Rebuilt for x264 ABI 0.120

* Sun Feb 19 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.10-1
- Update to 0.10
- Disable dirac by default - rfbz#1946
- Enabled by default: libv4l2 gnutls
- New RPM Conditionals:
  --with crystalhd dirac jack frei0r openal opencv
  --without celt cdio pulse

* Wed Feb 01 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.8.9-1
- Update to 0.8.9
- Add BR libass-devel
- Rebuilt for libvpx

* Mon Jan 09 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.8.8-1
- Update to 0.8.8

* Wed Dec 21 2011 Nicolas Chauvet <kwizart@gmail.com> - 0.8.7-1
- Update to 0.8.7

* Fri Oct 28 2011 Nicolas Chauvet <kwizart@gmail.com> - 0.8.5-2
- Fix for glibc bug rhbz#747377

* Sun Oct 23 2011 Dominik Mierzejewski <rpm at greysector.net> - 0.8.5-1
- update to 0.8.5

* Fri Sep 23 2011 Dominik Mierzejewski <rpm at greysector.net> - 0.8.4-1
- update to 0.8.4
- fix FFmpeg name spelling

* Mon Aug 22 2011 Dominik Mierzejewski <rpm at greysector.net> - 0.8.2-1
- update to 0.8.2
- enable CELT decoding via libcelt
- support AMR WB encoding via libvo-amrwbenc (optional)
- enable FreeType support

* Thu Jul 14 2011 Nicolas Chauvet <kwizart@gmail.com> - 0.7.1-1
- Update to 0.7.1

* Fri Jul 01 2011 Nicolas Chauvet <kwizart@gmail.com> - 0.7-0.3.20110612git
- Add XvMC in ffmpeg

* Sun Jun 12 2011 Nicolas Chauvet <kwizart@gmail.com> - 0.7-0.2.20110612git
- Update to 20110612git from oldabi branch

* Sun Jun 12 2011 Nicolas Chauvet <kwizart@gmail.com> - 0.7-0.1.rc1
- Update to 7.0-rc1
- Remove upstreamed patch
- Fix flv - rfbz#1743
- New RPM build conditional --without x264.

* Tue Apr 12 2011 Dominik Mierzejewski <rpm at greysector.net> - 0.6.90-0.2.rc0
- fixed missing av_parser_parse symbol (upstream patch)

* Mon Apr 04 2011 Dominik Mierzejewski <rpm at greysector.net> - 0.6.90-0.1.rc0
- updated to 0.6.90-rc0 release
- ensure main package is version-locked to the -libs subpackage

* Sun Feb 27 2011 Dominik Mierzejewski <rpm at greysector.net> - 0.6.1-1.20110227git
- 20110227 snapshot
- bump version to post-0.6.1 to allow stable 0.6.1 update in older branches
- drop --with amr->opencore_amr indirection
- add qt-faststart tool (bug #1259)
- build PIC objects on PPC (bug #1457)
- provide custom version string
- require latest x264 build

* Fri Jan 21 2011 Hans de Goede <j.w.r.degoede@hhs.nl> - 0.6-5.20100704svn
- Rebuild for new openjpeg

* Wed Jul 21 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.6-4.20100704svn
- Enable libva
- Restore compatibility --with amr

* Mon Jul 05 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.6-3.20100704svn
- Fix build using --define ffmpegsuffix 'foo'
- Disable FFmpeg binaries when built with suffix.

* Sun Jul 04 2010 Dominik Mierzejewski <rpm at greysector.net> - 0.6-2.20100704svn
- 20100703 snapshot
- enable libvpx (WebM/VP8) support (rfbz#1250)
- drop faad2 support (dropped upstream)
- drop old Obsoletes:
- enable librtmp support

* Sat Jun 19 2010 Dominik Mierzejewski <rpm at greysector.net> - 0.6-1.20100619svn
- 20100619 snapshot

* Thu Apr 29 2010 Dominik Mierzejewski <rpm at greysector.net> - 0.6-0.3.20100429svn
- 20100429 snapshot
- dropped unnecessary imlib2-devel BR

* Sat Mar 20 2010 Dominik Mierzejewski <rpm at greysector.net> - 0.6-0.2.20100320svn
- bump for rebuild

* Sat Mar 20 2010 Dominik Mierzejewski <rpm at greysector.net> - 0.6-0.1.20100320svn
- 20100320 snapshot
- drop upstream'd patch
- bumped version to pre-0.6
- added ffprobe to file list

* Sat Jan 16 2010 Dominik Mierzejewski <rpm at greysector.net> - 0.5-6.20100116svn
- 20100116 snapshot, requires recent x264
- fix textrels on x86_64 in a different way (patch by Reimar Döffinger)
- use -mlongcall instead of -fPIC to fix rfbz#804, it's faster

* Sat Nov  7 2009 Hans de Goede <j.w.r.degoede@hhs.nl> - 0.5-5.20091026svn
- Add -fPIC -dPIC when compiling on ppc (rf804)

* Thu Oct 22 2009 Dominik Mierzejewski <rpm at greysector.net> - 0.5-4.20091026svn
- 20091026 snapshot, requires recent x264
- dropped support for old amr libs (not supported upstream since July)
- don't disable yasm for generic builds
- fixed opencore amr support
- dropped workaround for non-standard openjpeg headers location
- dropped separate SIMDified libs for x86 and ppc(64),
  runtime CPU detection should be enough

* Thu Oct 15 2009 kwizart <kwizart at gmail.com > - 0.5-3.svn20091007
- Update to svn snapshot 20091007
- Add BR dirac vdpau.
- Use --with nonfree as a separate conditional for amr and faac.
- Use --with gplv3 as a separate conditional for opencore-amr.
- Don't build faac by default because it's nonfree.
- Allow to --define 'ffmpegsuffix custom' for special SONAME.

* Fri Mar 27 2009 Dominik Mierzejewski <rpm at greysector.net> - 0.5-2
- rebuild for new faad2 and x264

* Tue Mar 10 2009 Dominik Mierzejewski <rpm at greysector.net> - 0.5-1
- 0.5 release
- enable yasm on x86_64, fix resulting textrels
- add missing obsoletes for ffmpeg-compat-devel (really fix bug #173)
- disable yasm and certain asm optimizations for generic ix86 builds
- %%{_bindir} is now usable
- include more docs
- specfile cleanups
- add JPEG2000 decoding support via openjpeg

* Sat Jan 31 2009 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.58.20090131
- 20090131 snapshot

* Wed Dec 17 2008 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.57.20081217
- 20081217 snapshot
- fix pkgconfig files again (broken in 0.4.9-0.55.20081214)

* Mon Dec 15 2008 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.56.20081214
- drop libdirac support for now

* Sun Dec 14 2008 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.55.20081214
- 20081214 snapshot
- change the lib split on x86, it doesn't work right for P3/AthlonXP
- specfile cleanups
- enable bzlib, dirac and speex support via external libs
- sort BR list alphabetically
- drop upstream'd patch

* Thu Dec 11 2008 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.54.20081202
- fix pkgconfig file generation

* Thu Dec 04 2008 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.53.20081202
- 20081202 snapshot
- drop upstreamed/obsolete patches

* Thu Nov 20 2008 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.52.20080908
- add obsoletes for -compat package (RPMFusion bug #173)

* Sat Nov 01 2008 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.51.20080908
- reworked build system
- build optimized versions where it makes sense
- specfile cleanups
- enable yasm for optimized asm routines on x86_32
- add obsoletes for Freshrpms' libpostproc subpackage

* Thu Sep 18 2008 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.50.20080908
- 20080908 snapshot (r25261), last before ABI change

* Fri Sep 05 2008 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.49.20080905
- 20080905 snapshot
- fix build --with amr
- update snapshot.sh
- drop liba52 support, native ac3 decoder is better in every way

* Mon Aug 25 2008 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.48.20080825
- 20080825 snapshot
- use CFLAGS more similar to upstream
- enable X11 grabbing input
- enable libavfilter

* Sun Aug 03 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.4.9-0.47.20080614
- rebuild

* Sat Jun 14 2008 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.46.20080614
- 20080614 snapshot
- no need to conditionalize swscaler anymore
- dropped obsolete pkgconfig patch
- BR latest x264

* Mon Mar 03 2008 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.45.20080113
- rebuild for new x264

* Sun Jan 13 2008 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.44.20080113
- 20080113 snapshot
- drop unnecessary patch
- enable libdc1394 support
- enable swscaler

* Mon Nov 12 2007 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.43.20071111
- ensure that we use the correct faad2 version

* Sun Nov 11 2007 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.42.20071111
- 20071111 snapshot
- current faad2 is good again

* Thu Oct 18 2007 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.41.20071011
- fix BRs and Requires for faad2

* Thu Oct 11 2007 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.40.20071011
- 20071011 snapshot
- don't link against faad2-2.5, it makes GPL'd binary non-distributable
- go back to normal linking instead of dlopen() of liba52

* Sun Sep 23 2007 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.39.20070923
- 20070923 snapshot
- use faad2 2.5
- optional AMR support
- dropped obsolete patch

* Thu Jun 07 2007 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.38.20070607
- 20070607 snapshot
- libdca BR dropped (no longer supported)
- drop gsm.h path hack, gsm in Fedora now provides a compatibility symlink
- remove arch hacks, ffmpeg's configure is smart enough
- enable cmov on x86_64

* Thu May 03 2007 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.37.20070503
- require older faad2 to prevent bugreports like #1388
- prepare for libdc1394 support
- enable pthreads
- 20070503 snapshot

* Thu Feb 08 2007 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.35.20070204
- libswscale.pc is necessary regardless of --enable-swscaler

* Sun Feb  4 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.4.9-0.34.20070204
- 2007-02-04 snapshot, enable libtheora.
- Make swscaler optional, disabled again by default (#1379).

* Fri Jan 05 2007 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.34.20061214
- move vhooks to -libs

* Wed Jan 03 2007 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.33.20061214
- split -libs subpackage for multilib installs

* Tue Dec 26 2006 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.32.20061214
- new kino works with swscaler, re-enabled

* Tue Dec 19 2006 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.31.20061214
- disable swscaler, it breaks kino

* Sun Dec 17 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.4.9-0.30.20061214
- fix pkgconfig patch

* Sat Dec 16 2006 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.29.20061214
- liba52 change broke build on 64bit
- resurrect lost URL changes

* Fri Dec 15 2006 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.28.20061214
- fixed build on x86
- change liba52 file-based dependency to provides-based
- resurrect and update pkgconfig patch

* Thu Dec 14 2006 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.27.20061214
- new snapshot URL
- new URL

* Thu Dec 14 2006 Dominik Mierzejewski <rpm at greysector.net> - 0.4.9-0.26.20061214
- 2006-12-14 snapshot
- added libdca support
- enabled swscaler
- dropped obsolete patches

* Mon Oct 30 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.4.9-0.25.20061030
- 2006-10-30 snapshot, fixes x86_64 build.
- Apply a less intrusive workaround for LAME detection issues.

* Sat Oct 28 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.4.9-0.25.20061028
- 2006-10-28 snapshot, build with x264.
- Clean up some pre-FC4 compat build dependency cruft.
- Quick and dirty workarounds for ./configure's libmp3lame test and asm
  register issues on ix86.

* Fri Oct 06 2006 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 0.4.9-25
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 26 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.4.9-0.24.20060817
- Drop SELinux fcontext settings, they're supposedly fixed upstream again.

* Thu Aug 17 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.4.9-0.23.20060817
- 2006-08-17 snapshot.
- Fix svn rev in "ffmpeg -version" etc.

* Wed Aug  9 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.4.9-0.23.20060804
- Reintroduce SELinux fcontext settings on ix86 (not needed on x86_64, ppc),
  they're not completely taken care of upstream (#1120).
- Split svn snapshot creator into a separate script.

* Fri Aug  4 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.4.9-0.22.20060804
- 2006-08-04 snapshot.
- Drop bogus version from SDL-devel build dependency.
- Drop no longer relevant libpostproc obsoletion.
- Prune pre-2005 changelog entries.
- Specfile cleanup.

* Sat Jun 17 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.4.9-0.22.20060617
- 2006-06-17 snapshot.

* Mon Jun 12 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.4.9-0.22.20060612
- 2006-06-12 snapshot, rgb.txt patch applied upstream.
- Patch to force linking vhook modules with their dependencies, --as-needed
  seems to drop needed things for some reason for drawtext and imlib2.
- Revert to dlopen()'ing liba52 and add file based dependency on it, it's
  easier this way again due to --as-needed linkage.

* Wed May 17 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.4.9-0.22.20060517
- 2006-05-17 snapshot.
- Link with faad2, don't dlopen() it.

* Sat May 13 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.4.9-0.22.20060513
- 2006-05-13 snapshot.
- Drop SELinux fixups, they're part of upstream policy now.

* Sat Apr 15 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.4.9-0.22.20060407
- SELinux file context fixups (mplayer, vdr-dxr3 etc) while waiting for #188358

* Sat Apr  8 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.4.9-0.21.20060407
- 2006-04-07 CVS snapshot.
- Move *.so to -devel, hopefully nothing needs them any more.

* Fri Mar 31 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.4.9-0.21.20051228
- Remove superfluous dependencies from pkgconfig files (#747).
- Re-enable MMX on x86_64.

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- switch to new release field

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Wed Dec 28 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.4.9-0.lvn.0.20.20051228
- 2005-12-28 CVS snapshot.
- Let upstream configure take care of PIC settings (patched for ppc).
- Own shared lib symlinks.

* Fri Dec 23 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.4.9-0.lvn.0.20.20050801
- Apply upstream fix for CVE-2005-4048.
- Patch to find rgb.txt in FC5 too.

* Thu Sep 29 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:0.4.9-0.lvn.0.19.20050801
- Clean up obsolete pre-FC3 stuff (FAAC is now unconditionally enabled).
- Drop zero Epochs.

* Tue Aug 16 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:0.4.9-0.lvn.0.18.20050801
- Apply some upstream and some mine (libdir) fixes to pkgconfig files.
- Add pkgconfig dependency to -devel.
- Include gsm support.

* Thu Aug 4 2005 David Woodhouse <dwmw2@infradead.org> - 0:0.4.9-0.lvn.0.17.20050801
- Update to 20050801 snapshot to make xine-lib happy
- Enable Altivec support by using --cpu=powerpc (not 'ppc')
- Enable theora
- Add pkgconfig files
- Undefine various things which might be macros before redefining them

* Sat Jul 23 2005 Dams <anvil[AT]livna.org> - 0:0.4.9-0.lvn.0.17.20050427
- Added patch from Marc Deslauriers to fix wmv2 distorsion

* Sun Jul 10 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:0.4.9-0.lvn.0.16.20050427
- Enable faac by default, rebuild with "--without faac" to disable.
- Clean up obsolete pre-FC2 and other stuff.

* Sun May 22 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:0.4.9-0.lvn.0.15.20050427
- PPC needs -fPIC too.

* Sat May 21 2005 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 0:0.4.9-0.lvn.0.14.20050427
- disable mmx for now on x86_64 to fix build

* Sat Apr 30 2005 Dams <anvil[AT]livna.org> - 0:0.4.9-0.lvn.0.13.20050427
- Removed bogus devel requires
- Re-added conditionnal a52dec buildreq

* Fri Apr 29 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:0.4.9-0.lvn.0.12.20050427
- Link avcodec with a52 when building with a52bin, remove unnecessary
  hardcoded liba52.so.0 dependency.

* Fri Apr 29 2005 Dams <anvil[AT]livna.org> - 0:0.4.9-0.lvn.0.11.20050427
- Fixed devel package deps

* Fri Apr 29 2005 Dams <anvil[AT]livna.org> - 0:0.4.9-0.lvn.0.10.20050427
- texi2html replaces tetex as build dependency (FC4 compliance)
- re-added man pages

* Thu Apr 28 2005 Dams <anvil[AT]livna.org> - 0:0.4.9-0.lvn.0.9.20050427
- Patch from Enrico to fix build on gcc4
- Missing BuildReq a52dec-devel when a52bin is defined
- Patch to fix a52 build

* Wed Apr 27 2005 Dams <anvil[AT]livna.org> - 0:0.4.9-0.lvn.0.8.20050427
- Updated tarball to cvs 20050427 snapshot
- Enabled libogg, xvid, a52bin
- Dropped Patch[0-3]
