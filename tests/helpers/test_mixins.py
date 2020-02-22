import pytest
from helpers.mixins import IsIncludeMetaInfoMixin


@pytest.mark.parametrize(
    "include_meta_info",
    [True, False]
)
def test_inlclude_meta_info(settings, include_meta_info):
    if include_meta_info:
        settings.MIDDLEWARE =[ "helpers.middleware.ResponseMetaInformationInJsonMiddleware"]
    else:
        settings.MIDDLEWARE = []

    mixin = IsIncludeMetaInfoMixin()
    assert mixin._is_include_meta_info == include_meta_info
