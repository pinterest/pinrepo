# Copyright 2015, Pinterest, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

OPENSSL_VERSION = 1.0.1m
ZLIB_VERSION = 1.2.8
PCRE_VERSION = 8.35
DEVKIT_VERSION = 0.2.19
SETNGINX_VERSION = 0.24
CACHEPURGE_VERSION = 2.3
NGINX_VERSION = 1.7.12
BUILD_DIR=$(CURDIR)/build
TARGET_DIR=$(CURDIR)/target

default: build

clean:
	rm -rf $(BUILD_DIR); \
	rm -rf $(TARGET_DIR);

prepare:
	mkdir -p $(BUILD_DIR); \
	mkdir -p $(TARGET_DIR);

download-pcre:
	cd $(BUILD_DIR); \
	mkdir pcre; \
	wget -O - http://iweb.dl.sourceforge.net/project/pcre/pcre/$(PCRE_VERSION)/pcre-$(PCRE_VERSION).tar.gz | tar zxf - -C pcre --strip-components=1

download-zlib:
	cd $(BUILD_DIR); \
	mkdir zlib; \
	wget -O - http://zlib.net/zlib-$(ZLIB_VERSION).tar.gz | tar zxf - -C zlib --strip-components=1

download-openssl:
	cd $(BUILD_DIR); \
	mkdir openssl; \
	wget -O - ftp://ftp.openssl.org/source/openssl-$(OPENSSL_VERSION).tar.gz | tar zxf - -C openssl --strip-components=1

download-ngx_devel_kit:
	cd $(BUILD_DIR); \
	mkdir ngx_devel_kit; \
	wget -O - https://github.com/simpl/ngx_devel_kit/archive/v$(DEVKIT_VERSION).tar.gz | tar zxf - -C ngx_devel_kit --strip-components=1

download-set-misc-nginx-module:
	cd $(BUILD_DIR); \
	mkdir set-misc-nginx-module; \
	wget -O - https://github.com/agentzh/set-misc-nginx-module/archive/v$(SETNGINX_VERSION).tar.gz | tar zxf - -C set-misc-nginx-module --strip-components=1

download-ngx_cache_purge:
	cd $(BUILD_DIR); \
	mkdir ngx_cache_purge; \
	wget -O - https://github.com/FRiCKLE/ngx_cache_purge/archive/$(CACHEPURGE_VERSION).tar.gz | tar zxf - -C ngx_cache_purge --strip-components=1

download-nginx-upstream-fair:
	cd $(BUILD_DIR); \
	mkdir nginx-upstream-fair; \
	wget -O - https://codeload.github.com/gnosek/nginx-upstream-fair/legacy.tar.gz/master | tar zxf - -C nginx-upstream-fair --strip-components=1

download-nginx:
	cd $(BUILD_DIR); \
	mkdir nginx; \
	wget -O - http://nginx.org/download/nginx-$(NGINX_VERSION).tar.gz | tar zxf - -C nginx --strip-components=1

download: prepare download-pcre download-zlib download-openssl download-ngx_devel_kit download-set-misc-nginx-module download-nginx download-ngx_cache_purge download-nginx-upstream-fair

build: clean download
	cd $(BUILD_DIR)/nginx; \
	./configure  \
	--prefix=$(TARGET_DIR) \
	--with-http_stub_status_module \
	--with-poll_module \
    --with-http_ssl_module \
	--with-openssl=../openssl \
    --with-pcre=../pcre \
	--with-zlib=../zlib \
	--add-module=../ngx_devel_kit \
	--add-module=../set-misc-nginx-module \
	--add-module=../ngx_cache_purge \
	--add-module=../nginx-upstream-fair \
    --without-http_scgi_module \
    --without-http_uwsgi_module \
    --without-http_fastcgi_module \
	--with-ld-opt="-static"; \
	make; \
	make install;
