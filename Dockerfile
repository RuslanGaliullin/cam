# MIT License
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
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

FROM yegor256/cam

ENV DEBIAN_FRONTEND=noninteractive

SHELL ["/bin/bash", "--login", "-c"]

RUN apt-get install openjdk-11-jdk -y
RUN java --version

RUN pip install aiofiles

WORKDIR /cam
COPY Makefile /cam
COPY requirements.txt /cam
COPY steps/install.sh /cam/steps/
COPY help/* /cam/help/
COPY tests/* /cam/tests/

RUN rm -rf /cam/metrics/authors.sh /cam/metrics/jpeek.sh /cam/metrics/ast.py

COPY . /cam
# RUN chmod a+rx /cam/metrics/mine_metric.py

# docker run --detach --name=cam --rm --volume "$(pwd):/dataset"   -e "TOKEN=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" -e "REPO=yegor256/tojos" -e "TARGET=/dataset" custom_methods "make -e >/dataset/make.log 2>&1"

# docker run --detach --name=cam --rm --volume "$(pwd):/dataset"   -e "TOKEN=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" -e "TOTAL=1000" -e "TARGET=/dataset" paper "make -e >/dataset/make.log 2>&1"