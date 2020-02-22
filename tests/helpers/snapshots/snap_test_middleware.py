# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_response_meta_info_in_json Meta info in json'] = {
    '_meta_info': {
        'application_version': '0.0.1',
        'response_hash': '349a579265843f4412d30d59a70e3711',
        'timestamp': '2020-01-01T00:00:00.000000Z'
    },
    'detail': 'Everything works'
}

snapshots['test_response_meta_info_in_headers Response'] = {
    'detail': 'Everything works'
}

snapshots['test_response_meta_info_in_headers Meta info with headers'] = {
    'content-type': (
        'Content-Type',
        'application/json'
    ),
    'h-application-version': (
        'H-Application-Version',
        '0.0.1'
    ),
    'h-response-hash': (
        'H-Response-Hash',
        '24fd28cf7040211c3efef84aeeec4df1'
    ),
    'h-timestamp': (
        'H-Timestamp',
        '2020-01-01T00:00:00.000000Z'
    )
}

snapshots['test_not_response_meta_info[ResponseMetaInformationInHeadersMiddleware] Response'] = {
    'detail': 'Everything works'
}

snapshots['test_not_response_meta_info[ResponseMetaInformationInHeadersMiddleware] Meta info with headers'] = {
    'content-type': (
        'Content-Type',
        'application/json'
    )
}

snapshots['test_not_response_meta_info[ResponseMetaInformationInJsonMiddleware] Response'] = {
    'detail': 'Everything works'
}

snapshots['test_not_response_meta_info[ResponseMetaInformationInJsonMiddleware] Meta info with headers'] = {
    'content-type': (
        'Content-Type',
        'application/json'
    )
}
