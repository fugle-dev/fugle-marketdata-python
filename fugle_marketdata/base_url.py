import re

_VERSION_SEGMENT = re.compile(r'/v\d+\.\d+$')


def with_version(base_url, version, hint=''):
    """Join a caller-supplied `base_url` with the version the SDK resolved.

    `base_url` carries the host and path prefix and nothing else; the version
    segment is always appended here. A version written into `base_url` is
    rejected rather than swapped or appended on top of, because letting two
    options decide the same path segment is what forced the old precedence
    rules — and those rules meant anyone who only wanted to change host was
    made to manage the version by hand.
    """
    trimmed = base_url.rstrip('/')
    existing = _VERSION_SEGMENT.search(trimmed)

    if existing:
        raise TypeError(
            f"base_url must not include a version segment (found '{existing.group()}'). "
            f"Pass the host and path prefix only: '{trimmed[:existing.start()]}'."
            + (f' {hint}' if hint else '')
        )

    return f'{trimmed}/{version}'
