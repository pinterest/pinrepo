# Pypi Pinrepo

## Run Pypi Pinrepo

The provided `nginx.conf.tmpl` contains the minimum directives to make pinrepo work. Customize it to fit your own requirements; you need at least to change `PYPIREPO_CACHE_PATH, PYPIREPO_BUCKET, PYPIREPO_REGION, AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` to use your own bucket and key. Copy and overwrite your nginx server's nginx.conf and restart nginx. Be sure to copy `../nginx/proxy.conf` to your nginx config directory as well if not already.

## Install pypi-release

```
pip install pypi-release
```

## Use the included pypi-release source

The included pypi-release package under pypi-release directory could upload pypi packages to S3.

## Publish pypi package

```
pypi-release -b PYPIREPO_BUCKET -i AWS_ACCESS_KEY_ID -k AWS_SECRET_ACCESS_KEY -f sample-package-1.0.0.tar.gz
```
```
usage: pypi-release.py [-h] [-f FILE_PATH] [-i AWS_ACCESS_KEY_ID]
                       [-k AWS_SECRET_ACCESS_KEY] -b BUCKET [-m MAX_ENTRY]
                       [--regenerate-index] [-p PACKAGE_NAME] [-d WORK_DIR]
                       [--force] [--dry-run]

Release python packages to Pypi Pinrepo.

optional arguments:
  -h, --help            show this help message and exit
  -f FILE_PATH, --file-path FILE_PATH
                        the full path of the package to be released
  -i AWS_ACCESS_KEY_ID, --aws-access-key-id AWS_ACCESS_KEY_ID
                        AWS access key id; if not provided, will use
                        environment variable AWS_ACCESS_KEY_ID
  -k AWS_SECRET_ACCESS_KEY, --aws-secret-access-key AWS_SECRET_ACCESS_KEY
                        AWS secret access key; if not provided, will use
                        environment variable AWS_SECRET_ACCESS_KEY
  -b BUCKET, --bucket BUCKET
                        AWS bucket holding all the python packages.
  -m MAX_ENTRY, --max-entry MAX_ENTRY
                        the max number of versions to keep in index.html,
                        default is unlimited.
  --regenerate-index    [re]generate the index.html for a package,
                        package_name is needed.
  -p PACKAGE_NAME, --package_name PACKAGE_NAME
                        the name of the package to regenerate index.html for
  -d WORK_DIR, --work-dir WORK_DIR
                        the directory to save intermediate files, default is
                        /tmp.
  --force               force to release the same version again, will
                        overwrite the existing one.
  --dry-run             will not update anything, just a sanity test.
  ```
