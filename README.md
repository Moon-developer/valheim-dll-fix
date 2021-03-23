# Valheim desync fix
[![valheim - 0.147.3](https://img.shields.io/badge/valheim-0.147.3-4959bf)](https://)
[![python - 3.8.5](https://img.shields.io/badge/python-3.8.5-2ea44f)](https://)
[![can modify - client & server](https://img.shields.io/badge/can_modify-client_%26_server-2ea44f)](https://)

Python script to apply patch which fixes the server lag/desync issue. 

The script will stop working if they update the m_dataPerSec variable from `61440`.
I will try keep this updated as new Valheim updates show up.

The script will create a backup of the original file before modification happens.

## requirements:

You only need to have Python3 installed on your machine to execute this script.

## execution:

Before running the script confirm the config.ini file is updated so that `file_path` points to your assembly file.

Once your config is updated simply run the file:
```bash
python3 main.py
```
