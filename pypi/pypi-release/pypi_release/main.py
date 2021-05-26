# -*- coding: utf-8 -*-
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

"""
Release python packages to Pypi Pinrepo.
"""
import datetime
import hashlib
import os
import re
import time

import boto

MAX_ENTRY = 0
ENTRY_PATTERN = re.compile('<a href="(.*)">(.*)</a>(.*)')
NEW_ENTRY_TMPL = '<a href="../%s/%s#md5=%s" rel="internal">%s</a> %s %d<br/>'
INDEX_HTML_TOP_TMPL = (
    "<html><head>"
    '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
    "<title>Index of %s</title>"
    '</head><body bgcolor="white">'
    "<h1>Index of %s</h1><hr>"
)
INDEX_HTML_BOTTOM_TMPL = "<hr></body></html>"
OLD_INDEX_FILENAME = "index.html.old"
NEW_INDEX_FILENAME = "index.html.new"

# Steal from pip source, https://github.com/pypa/pip/blob/develop/pip/_vendor/distlib/util.py
PROJECT_NAME_AND_VERSION = re.compile(
    r"([a-z0-9_]+([.-][a-z_][a-z0-9_]*)*)-"
    r"([a-z0-9_.+-]+)\.(tar\.gz|tar\.bz2|tar|tgz|zip|whl)",
    re.I,
)


class S3(object):
    def __init__(
        self,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        bucket=None,
    ):
        conn = boto.connect_s3(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        self.bucket = conn.get_bucket(bucket)

    def exists(self, key):
        return self.bucket.get_key(key) is not None

    def upload(self, key, path):
        self.bucket.new_key(key).set_contents_from_filename(path)

    def download(self, key, path):
        self.bucket.get_key(key).get_contents_to_filename(path)

    def get(self, key):
        self.bucket.get_key(key)

    def list(self, key):
        return self.bucket.list(prefix=key)

    # wait until file show up in S3
    def wait_until_available(self, key, n=100, interval=1):
        sleep_time = interval
        total_sleep_time = interval
        for x in range(n):
            if not self.exists(key):
                print("wait until %s is available in S3..." % key)
                time.sleep(sleep_time)
                total_sleep_time += sleep_time
                sleep_time += interval
            else:
                return
        raise Exception(
            "%s has not showed up in S3 after %d sec, check it manually."
            % (key, total_sleep_time)
        )


class PackageItem(object):
    def __init__(self, name, md5, date, size):
        self.name = name
        self.md5 = md5
        self.date = date
        self.size = size


def safe_name(name):
    return re.sub("[^A-Za-z0-9.]+", "-", name).lower()


# Give full path of the file, return the package name and file name
def extract_package_name(path):
    # make sure file exists
    if not os.path.isfile(path):
        raise Exception("%s does not exist or not a valid file" % path)

    file_name = os.path.basename(path)

    m = PROJECT_NAME_AND_VERSION.match(file_name)
    if m:
        package_name = m.group(1)
        return package_name, file_name
    else:
        raise Exception("File name %s is not supported!" % file_name)


def generate_index(
    s3=None, package_name=None, work_dir="/tmp", max_entry=MAX_ENTRY, dry_run=False
):
    work_dir = "%s/%s" % (work_dir, package_name)
    # see comments in release.py for the reason why canonical package name is needed
    safe_package_name = safe_name(package_name)
    s3_index_path = "%s/%s" % (safe_package_name, "index.html")
    list_rs = s3.list("%s/" % safe_package_name)
    entries = []

    # loop on the S3 list resultset and populate entries
    for key in list_rs:
        file_name = os.path.basename(key.name)
        # ignore index.html
        if file_name != "index.html":
            entries.append(
                PackageItem(file_name, key.etag.strip('"'), key.last_modified, key.size)
            )

    if not entries:
        print("Package %s has never been released, exit!" % package_name)
        return

    # sort the list based on object last_modified
    entries.sort(key=lambda x: x.date)

    # make sure work dir exists
    if not os.path.exists(work_dir):
        os.makedirs(work_dir)

    old = "%s/%s" % (work_dir, OLD_INDEX_FILENAME)
    new = "%s/%s" % (work_dir, NEW_INDEX_FILENAME)

    # download index.html if exists, for information only
    if s3.exists(s3_index_path):
        s3.download(s3_index_path, old)

    # generate index.html, remove older entries if the total entries exceed max_retry
    # S3 objects return in alphabetical order, we will re-order based on last modified time
    with open(new, "w") as fn:
        top = INDEX_HTML_TOP_TMPL % (package_name, package_name)
        fn.write("%s\n" % top)

        # skip the top x entries if exceed max_entry
        start = 0
        if max_entry and max_entry < len(entries):
            start = 0 + len(entries) - max_entry
        for i in range(start, len(entries)):
            new_entry = NEW_ENTRY_TMPL % (
                safe_package_name,
                entries[i].name,
                entries[i].md5,
                entries[i].name,
                entries[i].date,
                entries[i].size,
            )
            fn.write("%s\n" % new_entry)

        fn.write(INDEX_HTML_BOTTOM_TMPL)

    if dry_run:
        print(
            "Dryrun only, otherwise should have no problem to regenerate index for %s"
            % package_name
        )
        return

    # finally upload new index
    s3.upload(s3_index_path, new)
    s3.wait_until_available(s3_index_path)
    if safe_package_name != package_name:
        s3_original_index_path = "%s/%s" % (package_name, "index.html")
        s3.upload(s3_original_index_path, new)
        s3.wait_until_available(s3_original_index_path)

    print("Successfully re-generated index for package %s" % package_name)


def gen_md5(file_path, block_size=2 ** 20):
    with open(file_path, "rb") as fn:
        md5 = hashlib.md5()
        while True:
            data = fn.read(block_size)
            if not data:
                break
            md5.update(data)
        return md5.hexdigest()


def generate_new_index(
    work_dir,
    package_name,
    safe_package_name,
    file_name,
    file_path,
    first_package,
    max_entry,
):
    old = "%s/%s" % (work_dir, OLD_INDEX_FILENAME)
    new = "%s/%s" % (work_dir, NEW_INDEX_FILENAME)

    size = os.path.getsize(file_path)
    date = datetime.datetime.utcnow().isoformat()[:-3] + "Z"
    md5 = gen_md5(file_path)
    new_entry = NEW_ENTRY_TMPL % (
        safe_package_name,
        file_name,
        md5,
        file_name,
        date,
        size,
    )

    if first_package:
        with open(new, "w") as fn:
            top = INDEX_HTML_TOP_TMPL % (package_name, package_name)
            fn.write("%s\n%s\n%s" % (top, new_entry, INDEX_HTML_BOTTOM_TMPL))
            return

    # copy most of the entries over, append the new entry in the end
    # remove the first entry if the total entries exceed max_retry, unless it is 0
    entries = []
    with open(old) as fo:
        for line in fo:
            if ENTRY_PATTERN.match(line):
                if file_name not in line:
                    entries.append(line)
                else:
                    print("Skip the existing entry for %s" % file_name)

    with open(new, "w") as fn:
        top = INDEX_HTML_TOP_TMPL % (package_name, package_name)
        fn.write("%s\n" % top)

        # skip the top x entries if exceed max_entry
        start = 0
        if 0 < max_entry <= len(entries):
            start = 0 + len(entries) - max_entry + 1
            print(
                "Entries exceeded max allowed %d, skip the top %d entry"
                % (max_entry, start)
            )

        for i in range(start, len(entries)):
            fn.write("%s" % entries[i])

        fn.write("%s\n" % new_entry)
        fn.write(INDEX_HTML_BOTTOM_TMPL)


def release(
    s3=None,
    file_path=None,
    work_dir="/tmp",
    max_entry=MAX_ENTRY,
    dry_run=False,
    force=False,
):
    package_name, file_name = extract_package_name(file_path)
    work_dir = "%s/%s" % (work_dir, package_name)

    # pip 6.0+ will query package in its canonical format, i.e. [a-z0-9\-]+
    # so "pip install X_y" become "pip install x-y", to support this behavior,
    # for every package we release, if its name is not in canonical format, we would
    # need to generate 2 entries, one uses original name, one uses canonical name, so that
    # we support both pip 6.0- and pip 6.0+
    safe_package_name = safe_name(package_name)
    s3_file_path = "%s/%s" % (safe_package_name, file_name)
    s3_index_path = "%s/%s" % (safe_package_name, "index.html")

    # make sure file not exist in index already
    if not force and s3.exists(s3_file_path):
        raise Exception("%s existed already, use --force if release again!" % file_name)

    old = "%s/%s" % (work_dir, OLD_INDEX_FILENAME)
    new = "%s/%s" % (work_dir, NEW_INDEX_FILENAME)
    # make sure dir exists
    if not os.path.exists(work_dir):
        os.makedirs(work_dir)

    # download index.html if exists
    first_package = False
    if not s3.exists(s3_index_path):
        print("Release %s the first time!" % package_name)
        first_package = True
    else:
        s3.download(s3_index_path, old)

    # generate the new index.html first
    generate_new_index(
        work_dir,
        package_name,
        safe_package_name,
        file_name,
        file_path,
        first_package,
        max_entry,
    )

    if dry_run:
        print("Dryrun only, otherwise should have no problem to release %s" % file_path)
        return

    # finally upload both the package and new index
    s3.upload(s3_file_path, file_path)
    s3.wait_until_available(s3_file_path)

    # then upload the new index
    s3.upload(s3_index_path, new)
    s3.wait_until_available(s3_index_path)
    if safe_package_name != package_name:
        s3_original_index_path = "%s/%s" % (package_name, "index.html")
        s3.upload(s3_original_index_path, new)
        s3.wait_until_available(s3_original_index_path)

    print("Successfully released %s" % file_path)


def main(
    file_path,
    aws_access_key_id,
    aws_secret_access_key,
    bucket,
    package_name,
    work_dir,
    max_entry=0,
    regenerate_index=False,
    force=False,
    dry_run=False,
):

    s3 = S3(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        bucket=bucket,
    )

    if regenerate_index:
        if not package_name:
            raise ValueError("Package name is required when regenerating an index")
        generate_index(
            s3=s3,
            package_name=package_name,
            work_dir=work_dir,
            max_entry=max_entry,
            dry_run=dry_run,
        )
    else:
        if not file_path:
            raise ValueError("File path is required when releasing a package")
        release(
            s3=s3,
            file_path=file_path,
            work_dir=work_dir,
            max_entry=max_entry,
            dry_run=dry_run,
            force=force,
        )
