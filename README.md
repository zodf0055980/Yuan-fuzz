# Yuan-fuzz
Fuzzer with argv
## How to use
先觀察程式執行有哪些參數，並依照參數撰寫設定檔，使用設定檔來協助模糊測試。
## example
用 [libjpeg-turbo](https://github.com/libjpeg-turbo/libjpeg-turbo) 當範例
``` 
./AFL/sqfuzz -i i1 -o o1 -m none -s parameters.xml -- ~/afl-target/libjpeg-turbo/build/cjpeg
```
從 afl 增加些許功能
```
-s xml        - add argv file information
-w            - let file path in front of argv
-r            - argv init random
```
## Bug reported
### libjpeg-turbo
1. https://github.com/libjpeg-turbo/libjpeg-turbo/issues/441
### binutils
1. https://sourceware.org/bugzilla/show_bug.cgi?id=26774
### libvips
1. https://github.com/libvips/libvips/issues/1867
2. https://github.com/libvips/libvips/issues/1868

## 致謝
使用 [SQ-fuzz](https://github.com/fdgkhdkgh/SQ-Fuzz) 修改，對內部程式做優化與加速(約 1.2 倍)，並使有些功能能使用，e.g. qemu-mode，bind cpu core。