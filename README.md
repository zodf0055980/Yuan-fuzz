# Yuan-fuzz
Fuzzer run with argv based on AFL
## How to use
Use `-h` `--help` to know target program options, and use it to write XML file to help fuzzing.
I give some [XML examples](https://github.com/zodf0055980/Yuan-fuzz/tree/main/xml) here, maybe could help to write XML file.
## Technology
Add one fuzzing stage named arg_gen, it automatically generates random argv using xml. If find new path, add argv information in queue. When arg_gen stage end, restart forkserver with argv information in queue. 
## How to use
Install [libxml2](http://xmlsoft.org/downloads.html) first.

Build it.
```
$ make
```
use [libjpeg-turbo](https://github.com/libjpeg-turbo/libjpeg-turbo) to be running example.
``` 
Yuan-fuzz -i input -o output -m none -s ~/XML_PATH/parameters.xml -- ~/TARGET_PATH/libjpeg-turbo/build/cjpeg
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
### libvips
1. https://github.com/libvips/libvips/issues/1867
2. https://github.com/libvips/libvips/issues/1868
### openjpeg
1. https://github.com/uclouvain/openjpeg/issues/1283 (CVE-2020-27814)
2. https://github.com/uclouvain/openjpeg/issues/1284 (CVE-2020-27823)
3. https://github.com/uclouvain/openjpeg/issues/1286 (CVE-2020-27824)
4. https://github.com/uclouvain/openjpeg/issues/1293
5. https://github.com/uclouvain/openjpeg/issues/1294
6. https://github.com/uclouvain/openjpeg/issues/1297
7. https://github.com/uclouvain/openjpeg/issues/1299
8. https://github.com/uclouvain/openjpeg/issues/1302
### jasper
1. https://github.com/jasper-software/jasper/issues/252 (CVE-2020-27828)

## Thanks
Use [SQ-fuzz](https://github.com/fdgkhdkgh/SQ-Fuzz) to modify.
