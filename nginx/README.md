# Pinrepo nginx

The provided `Makefile` will download and build a customized version of nginx with minimum set of modules to make Pinrepo work. Feel free to change nginx and module versions, or incoporate this into your existing nginx build process.

Simply execute `make` to build and install nginx. By default, nginx executable and config files will be installed under ./target directory. Be sure to copy `proxy.conf` to `target/conf`. It is needed for S3 signing and proxying. 

To start nginx server: 

```sudo target/sbin/nginx```

Verify your nginx is working by executing 

```curl http://localhost/```

To stop nginx server: 

```sudo target/sbin/nginx -s stop```
