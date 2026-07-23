import re

from ..constants import FUGLE_MARKETDATA_WS_SUPPORTED_VERSIONS


def supported_versions(product):
    return FUGLE_MARKETDATA_WS_SUPPORTED_VERSIONS[product]


def latest_version(product):
    return supported_versions(product)[-1]


def _products_supporting(version):
    return [
        product
        for product, versions in FUGLE_MARKETDATA_WS_SUPPORTED_VERSIONS.items()
        if version in versions
    ]


def _assert_supported(product, version, hint):
    if version not in supported_versions(product):
        raise TypeError(
            f"{product} streaming does not support {version} "
            f"(supported: {', '.join(supported_versions(product))}). {hint}"
        )


def resolve_version(product, version=None):
    """Resolve the streaming version for a product from the `version` option.

    Omitted entirely, or omitted for this product in the mapping form, means the
    product's latest. Nothing is ever silently clamped: asking for a version a
    product doesn't serve raises rather than quietly handing back an older one.
    """
    if version is None:
        return latest_version(product)

    if isinstance(version, str):
        alternatives = _products_supporting(version)
        hint = (
            f"Use version={{'{alternatives[0]}': '{version}'}} to target a single product."
            if alternatives
            else f"No product serves {version}."
        )
        _assert_supported(product, version, hint)
        return version

    requested = version.get(product)
    if requested is None:
        return latest_version(product)

    _assert_supported(
        product,
        requested,
        f"Remove it from the version mapping to use {latest_version(product)}.",
    )
    return requested


_VERSION_SEGMENT = re.compile(r'/v\d+\.\d+$')


def apply_version_to_base_url(base_url, version):
    """Point an explicitly supplied `base_url` at `version` by swapping its
    trailing version segment (`.../marketdata/v1.0` -> `.../marketdata/v1.1`).

    A base_url without a recognizable version segment is left alone — it may be
    a proxy or an internal deployment that doesn't encode a version in its path,
    and inventing one would break it.
    """
    trimmed = base_url.rstrip('/')
    return _VERSION_SEGMENT.sub(f'/{version}', trimmed)
