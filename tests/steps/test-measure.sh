#!/usr/bin/env bash
# The MIT License (MIT)
#
# Copyright (c) 2021-2023 Yegor Bugayenko
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
set -e
set -o pipefail

stdout=$2

{
    repo="foo /bar test \"; "
    name="dir (with) _ long & and weird ; name /hello.java/test.java/Foo.java"
    java="${TARGET}/github/${repo}/${name}"
    mkdir -p "$(dirname "${java}")"
    echo "class Foo {}" > "${java}"
    msg=$("${LOCAL}/steps/measure.sh")
    echo "${msg}" | grep "for Foo.java (1/1)"
    echo "${msg}" | grep "All metrics calculated in 1 files"
    test -e "${TARGET}/measurements/${repo}/${name}.m"
    test ! -e "${TARGET}/measurements/${repo}/${name}.m.NHD"
} > "${stdout}" 2>&1
echo "👍🏻 Measured metrics correctly"
