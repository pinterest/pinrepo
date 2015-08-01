# Debian Pinrepo

## Run Debian Pinrepo

The provided `nginx.conf.tmpl` contains the minimum directives to make pinrepo work. Customize it to fit your own requirements; you need at least to change `DEBREPO_CACHE_PATH, DEBREPO_BUCKET, AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` to use your own bucket and key. Copy and overwrite the nginx server's nginx.conf and restart nginx. Be sure to copy `../nginx/proxy.conf` to your nginx config directory as well if not already.

## Publish Debian packages

We use deb-s3 to publish Debian packages. It's been working amazingly well for us. You can find all the details at https://github.com/krobertson/deb-s3. For example, use the following command to publish a Debian package

```
deb-s3 upload --preserve-versions --bucket DEBREPO_BUCKET --visibility private \
              --access-key-id AWS_ACCESS_KEY_ID --secret-access-key AWS_SECRET_ACCESS_KEY \
              --codename YOUR_CODENAME --component YOUR_COMPONENT \
              --arch YOUR_ARCH --sign=YOUR_SIGN YOUR_DEB_FILE
```
