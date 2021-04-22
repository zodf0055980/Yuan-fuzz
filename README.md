# Yuan-fuzz
Fuzzer runs with argv information and uses k-means clustering to group seed.

```
  Written and maintained by zodf0055980 <zodf0055980@gmail.com>
  Based on American Fuzzy Lop by Michal Zalewski
```

## Technology
Yuan-fuzz is a fuzzer implementing a technique to generate argv in addition fuzzing stage named arg_gen. It can help to fuzz binary target that has a lot of argv can use. 

And I also use k-means clustering to the group in the seed pool to improve seed selection likes [k-means-AFL](https://github.com/zodf0055980/k-means-AFL).

## Usage
Install [libxml2](http://xmlsoft.org/downloads.html) first.

Build it.
```
$ make
```
Use `-h` `--help` to know target program options, and use it to write XML file to help fuzzing.
I give some [XML examples](https://github.com/zodf0055980/Yuan-fuzz/tree/main/xml) here, maybe could help to write XML file.

When run fuzzer, you should open our seed selection server first.
```
$ python3 group_seed.py [port]
```

The command line usage of Yuan-fuzz is similar to AFL.
```
$ Yuan-fuzz -i [testcase_dir] -o [output_dir] -s [~/XML_PATH/parameters.xml] -p [port] -- [Target program]
```
I also implement two command that can help arg_gen stage.
```
-w            - let file_path in front of argv
-r            - argv random initial
```

## Example
Use [libjpeg-turbo](https://github.com/libjpeg-turbo/libjpeg-turbo) to be example.
```
$ git clone git@github.com:libjpeg-turbo/libjpeg-turbo.git
```
Build with instrumentation, you can use other compiler.
```
$ export CC=~/Yuan-fuzz/afl-gcc                                       
$ export CXX=~/Yuan-fuzz/afl-g++
$ export AFL_USE_ASAN=1 ;
$ cd libjpeg-turbo
$ mkdir build && cd build
$ cmake -G"Unix Makefiles" ..
$ make
```
Run fuzzer
``` 
$ python3 group_seed.py 8888
# Another Terminal
$ Yuan-fuzz -i ./testcases/images/jpeg -o fuzz_output -m none -s ./xml/libjpeg-turbo/djpeg/parameters.xml -p 8888 -- ~/TARGET_PATH/libjpeg-turbo/build/djpeg
```
If your xml file have a lot of argv, maybe you have to change some define value in parse.h.

## Interpreting output
It will have addition subdirectories created within the output directory and updated in real time.

- queue_info/queue
- queue_info/crashes
- queue_info/hangs

It save all seed running parameters and one-to-one correspondence with seed in queue, crashes, hangs subdirectories.
## Bug reported
### libjpeg-turbo
1. https://github.com/libjpeg-turbo/libjpeg-turbo/issues/441 (CVE-2020-35538)
### binutils
1. https://sourceware.org/bugzilla/show_bug.cgi?id=26774
2. https://sourceware.org/bugzilla/show_bug.cgi?id=26805
3. https://sourceware.org/bugzilla/show_bug.cgi?id=26809
### openjpeg
1. https://github.com/uclouvain/openjpeg/issues/1283 (CVE-2020-27814)
2. https://github.com/uclouvain/openjpeg/issues/1284 (CVE-2020-27823)
3. https://github.com/uclouvain/openjpeg/issues/1286 (CVE-2020-27824)
4. https://github.com/uclouvain/openjpeg/issues/1293 (CVE-2020-27841)
5. https://github.com/uclouvain/openjpeg/issues/1294 (CVE-2020-27842)
6. https://github.com/uclouvain/openjpeg/issues/1297 (CVE-2020-27843)
7. https://github.com/uclouvain/openjpeg/issues/1299 (CVE-2020-27844)
8. https://github.com/uclouvain/openjpeg/issues/1302 (CVE-2020-27845)
### jasper
1. https://github.com/jasper-software/jasper/issues/252 (CVE-2020-27828)
2. https://github.com/jasper-software/jasper/issues/263
### libsndfile
1. https://github.com/libsndfile/libsndfile/issues/675
### libxls
1. https://github.com/libxls/libxls/issues/90
### aom
1. https://bugs.chromium.org/p/aomedia/issues/detail?id=2905&q=&can=1
2. https://bugs.chromium.org/p/aomedia/issues/detail?id=2911&q=&can=1
3. https://bugs.chromium.org/p/aomedia/issues/detail?id=2912&q=&can=1
4. https://bugs.chromium.org/p/aomedia/issues/detail?id=2913&q=&can=1
5. https://bugs.chromium.org/p/aomedia/issues/detail?id=2914&q=&can=1
### libredwg
1. https://github.com/LibreDWG/libredwg/issues/320
2. https://github.com/LibreDWG/libredwg/issues/323
3. https://github.com/LibreDWG/libredwg/issues/324
4. https://github.com/LibreDWG/libredwg/issues/321
5. https://github.com/LibreDWG/libredwg/issues/325 (non release code-path)
### libxml2
1. https://gitlab.gnome.org/GNOME/libxml2/-/issues/231
2. https://gitlab.gnome.org/GNOME/libxml2/-/issues/235
3. https://gitlab.gnome.org/GNOME/libxml2/-/issues/237
---
### libvips (not use fuzz)
1. https://github.com/libvips/libvips/issues/1867
2. https://github.com/libvips/libvips/issues/1868

## Thanks
Use [SQ-fuzz](https://github.com/fdgkhdkgh/SQ-Fuzz) to modify.
