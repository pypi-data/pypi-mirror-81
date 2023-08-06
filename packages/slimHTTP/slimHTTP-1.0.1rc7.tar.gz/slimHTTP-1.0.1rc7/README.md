# <img src="https://github.com/Torxed/slimHTTP/raw/master/docs/_static/slimHTTP.png" alt="drawing" width="200"/>
A no-dependency, simple, minimal and flexible HTTP server written in Python.<br>
Supports: REST, WebSocket¹, vhosts, reverse proxy and static file delivery.

 * slimHTTP [documentation](https://slimhttp.readthedocs.io/en/master)
 * slimHTTP [discord](https://discord.gg/CMjZbwR) server

## Features

 * No dependencies or additional requirements
 * REST routes *(`@http.route('/some/endpoint')`)*
 * websockets using plugin [spiderWeb](https://github.com/Torxed/spiderWeb) ¹
 * Can emulate files via `@http.route('/example.html')`
 * vhosts
 * TLS *(SSL)*
 * reverse proxy
 * `.py` extensions in web-root/vhosts without having to use FastCGI
 * No threads used by default *(fully relies on `epoll()` and `select()` on Windows)*
 * flexible runtime configuration and re-configuration *(using annotation `@http.configuration`)*

## Installation

The project is hosted on PyPi and can be installed with `pip`.

    sudo pip install slimHTTP

But it can also be cloned manually *(or downloaded)*

    git clone https://github.com/Torxed/slimHTTP

## Minimal example

```py
import slimHTTP

http = slimHTTP.host(slimHTTP.HTTP)
http.run()
```

Serves any files under `/srv/http` by default in `HTTP` mode.

## Footnote

It's not pretty down here. But it'll do in a pinch.
