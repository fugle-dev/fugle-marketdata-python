# Changelog

## [2.6.0](https://github.com/fugle-dev/fugle-marketdata-python/compare/2.5.0...2.6.0) (2026-08-20)


### Features

* add stock ownership institutional_trades, director_holdings & tdcc_distribution REST endpoints ([b265df1](https://github.com/fugle-dev/fugle-marketdata-python/commit/b265df140aecb68a83baf96f506cb71d8ad29b2d))


### Bug Fixes

* accept `from_` as an alias for the reserved-word `from` query param in REST requests ([b265df1](https://github.com/fugle-dev/fugle-marketdata-python/commit/b265df140aecb68a83baf96f506cb71d8ad29b2d))

## [2.5.0](https://github.com/fugle-dev/fugle-marketdata-python/compare/2.4.1...2.5.0) (2026-08-14)


### Features

* **websocket:** add futopt streaming version option, defaulting futopt to v1.1 with trial frames ([a49552c](https://github.com/fugle-dev/fugle-marketdata-python/commit/a49552c20ad30cf0f25188beed635e8c96f61188))
* **client:** expose the resolved endpoint on rest and websocket clients ([e359dde](https://github.com/fugle-dev/fugle-marketdata-python/commit/e359ddeb8e2f50cb78fb31bded7a46eb28df4b31))
* url-encode futopt symbols for spread contracts + trial trades filter ([8bbf1b4](https://github.com/fugle-dev/fugle-marketdata-python/commit/8bbf1b4aa9e472929cc381f3e0bc12594943afcf))
* add stock ownership etf_holdings REST endpoint ([b120d57](https://github.com/fugle-dev/fugle-marketdata-python/commit/b120d5787e5802a42c6da50c585bac01c2cd5440))
* **websocket:** freshness-based health check with disconnect reason ([eedc9d3](https://github.com/fugle-dev/fugle-marketdata-python/commit/eedc9d389e447d8df320ada3952f8047dc35554e))


### Bug Fixes

* **client:** separate base_url from the API version ([77aee12](https://github.com/fugle-dev/fugle-marketdata-python/commit/77aee127afbae7a8c6976bf1caa0c228323869bf))
* **websocket:** clamp max_missed_pongs to a minimum of 1 ([2b622f7](https://github.com/fugle-dev/fugle-marketdata-python/commit/2b622f717872701f6327f4905401feb26d4fdff8))


### Code Refactoring

* **etf:** remove code query param from etf-holdings to match server MR !376 ([fa43524](https://github.com/fugle-dev/fugle-marketdata-python/commit/fa4352484df68e00c2797cab613b52c0d26e1ecc))


### Upgrading from 2.4.x

* **futopt streaming now connects to v1.1 by default.** v1.1 adds trial-matching frames (TAIFEX I022/I082), which arrive on the existing trade and candle channels marked `isTrial: True`. Handlers that do not check that flag will treat trial prices and volumes as real fills. Pass `version={'futopt': 'v1.0'}` to the client to stay on the previous stream.
* **`base_url` must not include a version segment.** It now carries the host and path prefix only — the version comes from the `version` option, and the SDK appends it. A `base_url` ending in `/v1.0` is rejected with a `TypeError` naming the prefix to use instead.
* **The scalar `version` form is removed.** Use the per-product mapping, e.g. `version={'futopt': 'v1.1'}`. Products serve different version sets, so a bare string only ever named a version by accident.
* **Both REST and WebSocket clients expose the endpoint they resolved** — `client.stock.base_url` and `client.futopt.url` — so the composed URL can be asserted rather than guessed.

## [2.4.1](https://github.com/fugle-dev/fugle-marketdata-python/compare/2.4.0...2.4.1) (2026-01-12)


### Features

* add corporate actions REST API endpoints ([191c939](https://github.com/fugle-dev/fugle-marketdata-python/commit/191c939b214fde7c209f59617f1c40157be54139))

# [2.4.0](https://github.com/fugle-dev/fugle-marketdata-python/compare/2.3.0...2.4.0) (2025-11-18)


### Bug Fixes

* add error handling for API requests ([414bf89](https://github.com/fugle-dev/fugle-marketdata-python/commit/414bf89464abb34c3c96bb344f06abf1c85d7a28))


### Features

* add SDK token authentication and custom base URL support ([17508e7](https://github.com/fugle-dev/fugle-marketdata-python/commit/17508e74d7e90556e3a0ce719427f7081580b65c))
* add WebSocket health check with ping/pong ([c16f73d](https://github.com/fugle-dev/fugle-marketdata-python/commit/c16f73dadf55d0b152c2fdece2220e302ed685e4))
* enhance API error handling with detailed debugging information ([c635dda](https://github.com/fugle-dev/fugle-marketdata-python/commit/c635ddad0ef5fa361c1642ec11c655b0ab9b9f8c))


### Performance Improvements

* migrate WebSocket JSON handling from json to orjson ([7604273](https://github.com/fugle-dev/fugle-marketdata-python/commit/76042732c6ea776435f3987498f123be6ccdb9c4))

## [2.3.1](https://github.com/fugle-dev/fugle-marketdata-python/compare/2.3.0...2.3.1) (2025-07-18)


### Bug Fixes

* add error handling for API requests ([414bf89](https://github.com/fugle-dev/fugle-marketdata-python/commit/414bf89464abb34c3c96bb344f06abf1c85d7a28))


### Features

* add SDK token authentication and custom base URL support ([17508e7](https://github.com/fugle-dev/fugle-marketdata-python/commit/17508e74d7e90556e3a0ce719427f7081580b65c))

# [2.3.0](https://github.com/fugle-dev/fugle-marketdata-python/compare/2.2.0...2.3.0) (2024-10-23)


### Features

* add REST endpoints for stock technical API ([e9a2f59](https://github.com/fugle-dev/fugle-marketdata-python/commit/e9a2f597d7fc63c19bee4b6247f508ef11744452))

# [2.2.0](https://github.com/fugle-dev/fugle-marketdata-python/compare/2.1.1...2.2.0) (2024-07-30)


### Features

* add REST methods for fetching intraday and historical data for futures and options ([1405f90](https://github.com/fugle-dev/fugle-marketdata-python/commit/1405f909226212e95c3b43df05151aaf81564559))

## [2.1.1](https://github.com/fugle-dev/fugle-marketdata-python/compare/2.1.0...2.1.1) (2024-03-11)

# [2.1.0](https://github.com/fugle-dev/fugle-marketdata-python/compare/2.0.0...2.1.0) (2024-03-04)


### Features

* add subscriptions method for WebSocket client ([5176960](https://github.com/fugle-dev/fugle-marketdata-python/commit/5176960ce4c24f25ee1064f45306f3bcc6c27447))

# [2.0.0](https://github.com/fugle-dev/fugle-marketdata-python/compare/1.1.0...2.0.0) (2024-01-18)


### Refactors

* WebSocket originally used asyncio, now switched to synchronous ([3384741](https://github.com/fugle-dev/fugle-marketdata-python/commit/3384741fe009b81c5a2b8cf9b66d004b3b4381ea))

# [1.1.0](https://github.com/fugle-dev/fugle-marketdata-python/compare/1.0.2...1.1.0) (2023-12-19)


### Features

* add ping method to WebSocket client ([2cd4e74](https://github.com/fugle-dev/fugle-marketdata-python/commit/2cd4e7409036101993bae927bcc900aac1d77ba3))

## [1.0.2](https://github.com/fugle-dev/fugle-marketdata-python/compare/1.0.1...1.0.2) (2023-11-13)


### Bug Fixes

* wording in docs and tweak import path ([3eeecbb](https://github.com/fugle-dev/fugle-marketdata-python/commit/3eeecbbc14514606c75968b1c797c086bce22c45))

## [1.0.1](https://github.com/fugle-dev/fugle-marketdata-python/compare/b0bbb3ba12026fcd82b20f6da4242ffc0c306133...1.0.1) (2023-08-30)


### Bug Fixes

* fix on close error ([7e17736](https://github.com/fugle-dev/fugle-marketdata-python/commit/7e17736e476c32c58187e79b485772881bb316fc))
