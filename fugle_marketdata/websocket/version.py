from ..constants import FUGLE_MARKETDATA_WS_SUPPORTED_VERSIONS

#: Appended to `base_url` rejections, pointing at the option that owns the version.
VERSION_OPTION_HINT = (
    "The version comes from the `version` option, e.g. version={'futopt': 'v1.1'}."
)


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

    Omitted entirely, an empty mapping, or omitted for this product all mean the
    same thing: that product's latest. Nothing is ever silently clamped — asking
    for a version a product doesn't serve raises rather than quietly handing back
    an older one.

    A bare version string used to be accepted as "this version for every
    product", but which product it applied to wasn't known until a client was
    taken off the factory, so an unsupported pairing only surfaced then — and
    with the products serving different version sets, the only scalar that never
    raises is the one every product happens to share. The mapping form says the
    same thing without the trap.
    """
    if version is None:
        return latest_version(product)

    if isinstance(version, str):
        alternatives = _products_supporting(version)
        suggestion = (
            'Use version={'
            + ', '.join(f"'{p}': '{version}'" for p in alternatives)
            + '}.'
            if alternatives
            else f'No product serves {version}.'
        )
        raise TypeError(
            f"version must be a per-product mapping, not the bare string "
            f"'{version}'. {suggestion}"
        )

    requested = version.get(product)
    if requested is None:
        return latest_version(product)

    _assert_supported(
        product,
        requested,
        f"Remove it from the version mapping to use {latest_version(product)}.",
    )
    return requested
