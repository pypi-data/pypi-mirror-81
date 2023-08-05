# Copyright 2020 Aptpod, Inc.
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
from collections import namedtuple
from unittest import TestCase

import pandas as pd
import pytz

from intdash import timeutils


class TestTimeutils(TestCase):
    def test_timestamp2unixmicro(self):

        Input = namedtuple("Input", ("ts",))
        Case = namedtuple("Case", ("input", "exp"))

        cases = [
            Case(
                input=Input(
                    ts=pd.Timestamp(
                        year=2020,
                        month=1,
                        day=1,
                        hour=23,
                        minute=59,
                        second=59,
                        microsecond=999_999,
                        nanosecond=999,
                        tzinfo=pytz.utc,
                    )
                ),
                exp=1_577_923_199_999_999,
            )
        ]

        for i, case in enumerate(cases):
            act = timeutils.timestamp2unixmicro(**case.input._asdict())
            self.assertEqual(act, case.exp, f"\n#{i}:\n exp={case.exp}\n act={act}")

    def test_timestamp2unix(self):

        Input = namedtuple("Input", ("ts",))
        Case = namedtuple("Case", ("input", "exp"))

        cases = [
            Case(
                input=Input(
                    ts=pd.Timestamp(
                        year=2020,
                        month=1,
                        day=1,
                        hour=23,
                        minute=59,
                        second=59,
                        microsecond=999_999,
                        nanosecond=999,
                        tzinfo=pytz.utc,
                    )
                ),
                exp=(1_577_923_199, 999_999_999),
            )
        ]

        for i, case in enumerate(cases):
            act = timeutils.timestamp2unix(**case.input._asdict())
            self.assertEqual(act, case.exp, f"\n#{i}:\n exp={case.exp}\n act={act}")

    def test_unix2timestamp(self):

        Input = namedtuple("Input", ("unix_sec", "unix_nano"))
        Case = namedtuple("Case", ("input", "exp"))

        cases = [
            Case(
                input=Input(unix_sec=1_577_923_199, unix_nano=999_999_999),
                exp=pd.Timestamp(
                    year=2020,
                    month=1,
                    day=1,
                    hour=23,
                    minute=59,
                    second=59,
                    microsecond=999_999,
                    nanosecond=999,
                    tzinfo=pytz.utc,
                ),
            )
        ]

        for i, case in enumerate(cases):
            act = timeutils.unix2timestamp(**case.input._asdict())
            self.assertEqual(act, case.exp, f"\n#{i}:\n exp={case.exp}\n act={act}")

    def test_timedelta2micro(self):

        Input = namedtuple("Input", ("td",))
        Case = namedtuple("Case", ("input", "exp"))

        cases = [
            Case(
                input=Input(td=pd.Timedelta(days=1, seconds=999, microseconds=999_999)),
                exp=int((1 * 60 * 60 * 24 + 999) * 1e6 + 999_999),
            )
        ]

        for i, case in enumerate(cases):
            act = timeutils.timedelta2micro(**case.input._asdict())
            self.assertEqual(act, case.exp, f"\n#{i}:\n exp={case.exp}\n act={act}")

    def test_micro2timedelta(self):

        Input = namedtuple("Input", ("micro",))
        Case = namedtuple("Case", ("input", "exp"))

        cases = [
            Case(
                input=Input(micro=(1 * 60 * 60 * 24 + 999) * 1e6 + 999_999),
                exp=pd.Timedelta(days=1, seconds=999, microseconds=999_999),
            )
        ]

        for i, case in enumerate(cases):
            act = timeutils.micro2timedelta(**case.input._asdict())
            self.assertEqual(act, case.exp, f"\n#{i}:\n exp={case.exp}\n act={act}")

    def test_timestamp2str(self):

        Input = namedtuple("Input", ("ts",))
        Case = namedtuple("Case", ("input", "exp"))

        cases = [
            Case(
                input=Input(
                    ts=pd.Timestamp(
                        year=2020,
                        month=1,
                        day=1,
                        hour=23,
                        minute=59,
                        second=59,
                        microsecond=999_999,
                        nanosecond=999,
                        tzinfo=pytz.utc,
                    )
                ),
                exp="2020-01-01T23:59:59.999999999Z",
            )
        ]

        for i, case in enumerate(cases):
            act = timeutils.timestamp2str(**case.input._asdict())
            self.assertEqual(act, case.exp, f"\n#{i}:\n exp={case.exp}\n act={act}")

    def test_str2timestamp(self):

        Input = namedtuple("Input", ("s",))
        Case = namedtuple("Case", ("input", "exp"))

        cases = [
            Case(
                input=Input(s="2020-01-01T23:59:59.999999999Z"),
                exp=pd.Timestamp(
                    year=2020,
                    month=1,
                    day=1,
                    hour=23,
                    minute=59,
                    second=59,
                    microsecond=999_999,
                    nanosecond=999,
                    tzinfo=pytz.utc,
                ),
            )
        ]

        for i, case in enumerate(cases):
            act = timeutils.str2timestamp(**case.input._asdict())
            self.assertEqual(act, case.exp, f"\n#{i}:\n exp={case.exp}\n act={act}")

    def test_str2timestamp_invalid(self):

        Input = namedtuple("Input", ("s",))
        Case = namedtuple("Case", ("input", "exp"))

        cases = [Case(input=Input(s="0001-01-01T00:00:00Z"), exp=pd.NaT)]

        for i, case in enumerate(cases):
            act = timeutils.str2timestamp(**case.input._asdict())
            self.assertTrue(pd.isnull(act), f"\n#{i}:\n exp={case.exp}\n act={act}")
