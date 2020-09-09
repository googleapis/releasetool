# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This module is used for reporting status via junit XML files that can be
consumed by Kokoro/Sponge."""

import io
import os

import attr
import jinja2

with open(os.path.join(os.path.dirname(__file__), "report.xml.j2"), "r") as fh:
    _TEMPLATE = jinja2.Template(fh.read())


@attr.s(auto_attribs=True, slots=True)
class Result:
    name: str
    error: bool = False
    skipped: bool = False
    _output: io.StringIO = attr.ib(factory=io.StringIO)

    @property
    def output(self):
        return self._output.getvalue()

    def print(self, *args, **kwargs):
        print(*args, **kwargs)
        print(*args, file=self._output, **kwargs)


class Reporter:
    def __init__(self, name):
        self.name = name
        self.results = []

    @property
    def failures(self):
        return len([result for result in self.results if result.error])

    @property
    def skips(self):
        return len([result for result in self.results if result.skipped])

    def add(self, result):
        self.results.append(result)

    def render(self):
        return _TEMPLATE.render(reporter=self)

    def write(self, filename):
        with open(filename, "w") as fh:
            fh.write(self.render())
