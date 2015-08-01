Pinrepo
=======

Pinrepo is Pinterest solution for storing and serving build artifacts such as debian
packages, maven jars and pypi packages.

* **Simple**: publish and store build artifacts in AWS S3; serve with Nginx reverse proxy
* **Extensible**: could eaily add other format support such as RPM
* **Reliable**: highly available nginx cluster and AWS S3 service
* **Scalable**: nginx layer scales horizontally; AWS S3 backend is highly scalable
* **Devops-riendly**: has been running in production for 8 month with virtually no maintenance

Find more details on the design at http://engineering.pinterest.com/.

1. [nginx](nginx/) contains a Makefile to build a simple nginx with the minimum set of modules
to run Pinrepo.

2. [deb](deb/) contains an nginx config file for debain package repo and instructions to publish
debian packages

3. [maven](maven/) contains an nginx config file for maven repo and instructions to publish
maven jars

4. [pypi](pypi/) contains an nginx config file for pypi repo, the pypi-release source code and
instructions to publish pypi packages
