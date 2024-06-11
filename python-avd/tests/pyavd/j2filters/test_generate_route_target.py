# Copyright (c) 2023-2024 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from pyavd.j2filters.generate_route_target import generate_route_target
from tests.pyavd.j2filters.filter_utils import convert_esi_short_to_route_target_format


class TestEsiManagementFilter:
    @pytest.mark.parametrize(
        "esi_short, route_target", 
        [
            ("0303:0202:0101", "03:03:02:02:01:01"),
            (None, None),
            ("ESI_SHORT", "ES:I_:SH:OR"),
            ("", "")
        ]
    )
    def test_generate_route_target(self, esi_short, route_target):
        # route_target_format_esi = convert_esi_short_to_route_target_format(ESI_SHORT)
        resp = generate_route_target(esi_short)
        assert resp == route_target
        # resp1 = generate_route_target(None)
        # assert resp1 is None

    # def test_test_generate_route_target_string(self):
    #     resp = generate_route_target("ESI_SHORT")
    #     assert resp == "ES:I_:SH:OR"
