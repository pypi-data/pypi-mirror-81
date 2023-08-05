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
import io
import uuid
from collections import namedtuple
from unittest import TestCase

import pandas as pd
import pytz

from intdash import data, protocol
from intdash.protocol import filter


class TestProtocol(TestCase):
    def test_elements(self):

        Case = namedtuple("Case", ("elem",))

        cases = [
            Case(
                elem=protocol.UpstreamSpecRequest(
                    req_id=1,
                    specs=[
                        protocol.UpstreamSpec(
                            stream_id=2,
                            store=True,
                            resend=True,
                            measurement_uuid=uuid.UUID(
                                "{11111111-1234-5678-1234-567812345678}"
                            ),
                            src_edge_uuid=uuid.UUID(
                                "{22222222-1234-5678-1234-567812345678}"
                            ),
                            dst_edge_uuids=[
                                uuid.UUID("{33333333-1234-5678-1234-567812345678}")
                            ],
                        ),
                        protocol.UpstreamSpec(
                            stream_id=3,
                            store=False,
                            resend=False,
                            measurement_uuid=uuid.UUID(
                                "{44444444-1234-5678-1234-567812345678}"
                            ),
                            src_edge_uuid=uuid.UUID(
                                "{55555555-1234-5678-1234-567812345678}"
                            ),
                            dst_edge_uuids=[],
                        ),
                    ],
                )
            ),
            Case(
                elem=protocol.UpstreamSpecResponse(
                    req_id=1, result_code=protocol.ResultCode.OK
                )
            ),
            Case(
                elem=protocol.DownstreamSpecRequest(
                    req_id=1,
                    specs=[
                        protocol.DownstreamSpec(
                            stream_id=2,
                            src_edge_uuid=uuid.UUID(
                                "{11111111-1234-5678-1234-567812345678}"
                            ),
                            dst_edge_uuid=uuid.UUID(
                                "{22222222-1234-5678-1234-567812345678}"
                            ),
                        ),
                        protocol.DownstreamSpec(
                            stream_id=3,
                            src_edge_uuid=uuid.UUID(
                                "{33333333-1234-5678-1234-567812345678}"
                            ),
                            dst_edge_uuid=uuid.UUID(
                                "{44444444-1234-5678-1234-567812345678}"
                            ),
                        ),
                    ],
                )
            ),
            Case(
                elem=protocol.DownstreamSpecResponse(
                    req_id=1, result_code=protocol.ResultCode.OK
                )
            ),
            Case(
                elem=protocol.MeasurementIDRequest(
                    req_id=1,
                    edge_uuid=uuid.UUID("{11111111-1234-5678-1234-567812345678}"),
                )
            ),
            Case(
                elem=protocol.MeasurementIDResponse(
                    req_id=1,
                    result_code=protocol.ResultCode.OK,
                    measurement_uuid=uuid.UUID(
                        "{11111111-1234-5678-1234-567812345678}"
                    ),
                )
            ),
            Case(elem=protocol.SOSMarker(stream_id=1, serial_number=2)),
            Case(elem=protocol.EOSMarker(stream_id=1, final=True, serial_number=2)),
            Case(
                elem=protocol.SectionAck(
                    stream_id=1, result_code=protocol.ResultCode.OK, serial_number=2
                )
            ),
        ]

        bio = io.BytesIO()
        bwr = io.BufferedWriter(bio)
        wr = protocol.Writer(bwr)

        for i, case in enumerate(cases):
            wr.write_elem(case.elem)

        bio.seek(0)
        brd = io.BufferedReader(bio)
        rd = protocol.Reader(brd)

        for i, case in enumerate(cases):
            act = rd.read_elem()
            exp = case.elem
            self.assertEqual(act, exp, f"\n#{i}:\n exp={exp}\n act={act}")

    def test_downstream_filters(self):

        Case = namedtuple("Case", ("elem",))

        cases = [
            Case(
                elem=protocol.DownstreamFilterRequest(
                    req_id=1,
                    filters=[
                        protocol.DownstreamFilter(
                            stream_id=2,
                            downstream_data_filters=[
                                protocol.DownstreamDataFilter(
                                    channel=3,
                                    filter=filter.Can.from_ids(
                                        ["00000001", "ffffffff"]
                                    ),
                                ),
                                protocol.DownstreamDataFilter(
                                    channel=3,
                                    filter=filter.Generic.from_ids(
                                        ["00000001", "ffffffff"]
                                    ),
                                ),
                            ],
                        ),
                        protocol.DownstreamFilter(
                            stream_id=3,
                            downstream_data_filters=[
                                protocol.DownstreamDataFilter(
                                    channel=3,
                                    filter=filter.Nmea.from_ids(["GPRMC", "GPGGA"]),
                                ),
                                protocol.DownstreamDataFilter(
                                    channel=3,
                                    filter=filter.GeneralSensor.from_ids(
                                        ["0001", "ffff"]
                                    ),
                                ),
                                protocol.DownstreamDataFilter(
                                    channel=3,
                                    filter=filter.Float.from_ids(["fff1", "fff2"]),
                                ),
                                protocol.DownstreamDataFilter(
                                    channel=3,
                                    filter=filter.Int.from_ids(["iii1", "iii2"]),
                                ),
                                protocol.DownstreamDataFilter(
                                    channel=3,
                                    filter=filter.String.from_ids(["sss1", "sss2"]),
                                ),
                                protocol.DownstreamDataFilter(
                                    channel=3,
                                    filter=filter.Bytes.from_ids(["bbb1", "bbb2"]),
                                ),
                            ],
                        ),
                    ],
                )
            ),
            Case(
                elem=protocol.DownstreamFilterResponse(
                    req_id=1, result_code=protocol.ResultCode.OK
                )
            ),
        ]

        bio = io.BytesIO()
        bwr = io.BufferedWriter(bio)
        wr = protocol.Writer(bwr)

        for i, case in enumerate(cases):
            wr.write_elem(case.elem)

        bio.seek(0)
        brd = io.BufferedReader(bio)
        rd = protocol.Reader(brd)

        for i, case in enumerate(cases):
            act = rd.read_elem()
            exp = case.elem
            self.assertEqual(act, exp, f"\n#{i}:\n exp={exp}\n act={act}")

    def test_units(self):

        Case = namedtuple("Case", ("elem",))

        cases = [
            Case(
                elem=protocol.Unit(
                    stream_id=1,
                    channel=2,
                    elapsed_time=pd.Timedelta(seconds=3),
                    data=data.CAN(
                        decimal_id=3, data=b"\x00\x01\x02\x03\x04\x05\x06\x07"
                    ),
                )
            ),
            Case(
                elem=protocol.Unit(
                    stream_id=1,
                    channel=2,
                    elapsed_time=pd.Timedelta(seconds=3),
                    data=data.NMEA(string="GPRMC"),
                )
            ),
            Case(
                elem=protocol.Unit(
                    stream_id=1,
                    channel=2,
                    elapsed_time=pd.Timedelta(seconds=3),
                    data=data.Generic(
                        decimal_id=3, data=b"\x00\x01\x02\x03\x04\x05\x06\x07"
                    ),
                )
            ),
            Case(
                elem=protocol.Unit(
                    stream_id=1,
                    channel=2,
                    elapsed_time=pd.Timedelta(seconds=3),
                    data=data.GeneralSensor(
                        decimal_id=3, data=b"\x00\x01\x02\x03\x04\x05\x06\x07"
                    ),
                )
            ),
            Case(
                elem=protocol.Unit(
                    stream_id=1,
                    channel=2,
                    elapsed_time=pd.Timedelta(seconds=3),
                    data=data.Controlpad(
                        decimal_id=3, data=b"\x00\x01\x02\x03\x04\x05\x06\x07"
                    ),
                )
            ),
            Case(
                elem=protocol.Unit(
                    stream_id=1,
                    channel=2,
                    elapsed_time=pd.Timedelta(seconds=3),
                    data=data.Basetime(
                        type=1,
                        basetime=pd.Timestamp(
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
                    ),
                )
            ),
        ]

        bio = io.BytesIO()
        bwr = io.BufferedWriter(bio)
        wr = protocol.Writer(bwr)

        for i, case in enumerate(cases):
            wr.write_elem(case.elem)

        bio.seek(0)
        brd = io.BufferedReader(bio)
        rd = protocol.Reader(brd)

        for i, case in enumerate(cases):
            act = rd.read_elem()
            exp = case.elem
            self.assertEqual(
                act, exp, f"\n#{i}:\n exp={exp.data.__dict__}\n act={act.data.__dict__}"
            )
