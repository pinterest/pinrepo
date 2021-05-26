#!/usr/bin/env python
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
import argparse
import logging

import pypi_release.main as api

# Configure logging for this package
__LOGGER__ = logging.getLogger("pypi_release")
__HANDLER__ = logging.StreamHandler()
__HANDLER__.setLevel(logging.DEBUG)
__LOGGER__.setLevel(logging.DEBUG)
__LOGGER__.addHandler(__HANDLER__)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-f",
        "--file-path",
        dest="file_path",
        help="the full path of the package to be released",
    )
    parser.add_argument(
        "-i",
        "--aws-access-key-id",
        dest="aws_access_key_id",
        help="AWS access key id; if not provided, will use environment variable "
        "AWS_ACCESS_KEY_ID",
    )
    parser.add_argument(
        "-k",
        "--aws-secret-access-key",
        dest="aws_secret_access_key",
        help="AWS secret access key; if not provided, will use environment "
        "variable AWS_SECRET_ACCESS_KEY",
    )
    parser.add_argument(
        "-b",
        "--bucket",
        dest="bucket",
        required=True,
        help="AWS bucket holding all the python packages.",
    )
    parser.add_argument(
        "-m",
        "--max-entry",
        type=int,
        dest="max_entry",
        default=0,
        help="the max number of versions to keep in index.html, "
        "default is unlimited.",
    )
    parser.add_argument(
        "--regenerate-index",
        dest="regenerate_index",
        action="store_true",
        help="[re]generate the index.html for a package, package_name is needed.",
    )
    parser.add_argument(
        "-p",
        "--package_name",
        dest="package_name",
        help="the name of the package to regenerate index.html for",
    )
    parser.add_argument(
        "-d",
        "--work-dir",
        dest="work_dir",
        default="/tmp",
        help="the directory to save intermediate files, default is /tmp.",
    )
    parser.add_argument(
        "--force",
        dest="force",
        action="store_true",
        help="force to release the same version again, will overwrite the "
        "existing one.",
    )
    parser.add_argument(
        "--dry-run",
        dest="dry_run",
        action="store_true",
        help="will not update anything, just a sanity test.",
    )
    args = parser.parse_args()

    api.main(
        file_path=args.file_path,
        aws_access_key_id=args.aws_access_key_id,
        aws_secret_access_key=args.aws_secret_access_key,
        bucket=args.bucket,
        package_name=args.package_name,
        work_dir=args.work_dir,
        max_entry=args.max_entry,
        regenerate_index=args.regenerate_index,
        force=args.force,
        dry_run=args.dry_run,
    )


main()
