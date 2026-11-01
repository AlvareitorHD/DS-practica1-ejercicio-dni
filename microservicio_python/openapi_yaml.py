import json
import yaml

# 1. Abre el JSON descargado y cárgalo en una variable
with open("docs/openapi.json", "r", encoding="utf-8") as f:
    openapi_data = json.load(f)

# 2. Abre docs/openapi.yaml en modo escritura (encoding="utf-8")
#    y vuelca ahí el contenido
with open("docs/openapi.yaml", "w", encoding="utf-8") as f:
    yaml.safe_dump(openapi_data, f, sort_keys=False, allow_unicode=True)