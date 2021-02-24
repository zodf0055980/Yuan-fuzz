# Yuan-fuzz
Fuzzer runs with argv information and uses k-means clustering to group seed. It's based on AFL.

## How to use
Use `-h` `--help` to know target program options, and use it to write XML file to help fuzzing.
I give some [XML examples](https://github.com/zodf0055980/Yuan-fuzz/tree/main/xml) here, maybe could help to write XML file.

## Technology
Add one fuzzing stage named arg_gen, it automatically generates random argv using xml. If find new path, add argv information in queue. When arg_gen stage end, restart forkserver with argv information in queue. 
Use [k-means clustering](https://github.com/zodf0055980/k-means-AFL) to group seed in seed pool to improve seed selection. 

## How to use
Install [libxml2](http://xmlsoft.org/downloads.html) first.

Build it.
```
$ make
```
use [libjpeg-turbo](https://github.com/libjpeg-turbo/libjpeg-turbo) to be running example.
``` 
$ python3 group_seed.py [port]
# Another Terminal
$ Yuan-fuzz -i [testcase_dir] -o [output_dir] -s [~/XML_PATH/parameters.xml] -p [port] -- ~/TARGET_PATH/libjpeg-turbo/build/cjpeg
```
We also add some option.
```
-s xml        - add argv file information
-w            - let file_path in front of argv
-r            - argv random initial
```
If your xml file have a lot of argv, maybe you have to change some define value in parse.h.
## Bug reported
### libjpeg-turbo
1. https://github.com/libjpeg-turbo/libjpeg-turbo/issues/441
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
### libsndfile
1. https://github.com/libsndfile/libsndfile/issues/675
### libxls
1. https://github.com/libxls/libxls/issues/90
### aom
1. https://bugs.chromium.org/p/aomedia/issues/detail?id=2905&q=&can=1
---
### libvips (not use fuzz)
1. https://github.com/libvips/libvips/issues/1867
2. https://github.com/libvips/libvips/issues/1868

## Thanks
Use [SQ-fuzz](https://github.com/fdgkhdkgh/SQ-Fuzz) to modify.
