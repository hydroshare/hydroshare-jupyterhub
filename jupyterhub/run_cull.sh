#!/usr/bin/env bash

source ./env
export JPY_API_TOKEN='6b2ee57055123b95be0df3a3c3609e09886e419b7f032db219dc8235de93ed44'
python3 cull_idle_servers.py --url=http://jupyter.uwrl.usu.edu/hub --timeout=3600 cull_every=30

