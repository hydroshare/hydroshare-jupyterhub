#!/bin/bash
set -x
set -e

# see https://gist.github.com/SunnyRaj/788ca494db609a404c9dc4c88d47e775

# dual install gcc, g++ 5 and 7
update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-7 60 --slave /usr/bin/gcc-ar gcc-ar /usr/bin/gcc-ar-7 --slave /usr/bin/gcc-nm gcc-nm /usr/bin/gcc-nm-7 --slave /usr/bin/gcc-ranlib gcc-ranlib /usr/bin/gcc-ranlib-7

update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-5 60 --slave /usr/bin/gcc-ar gcc-ar /usr/bin/gcc-ar-5 --slave /usr/bin/gcc-nm gcc-nm /usr/bin/gcc-nm-5 --slave /usr/bin/gcc-ranlib gcc-ranlib /usr/bin/gcc-ranlib-5

update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-7 10
update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-5 10

