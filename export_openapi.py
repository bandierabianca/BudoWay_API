from budoway_api.main import app
import json, yaml, os
out = os.getenv('OPENAPI_OUT', 'openapi.json')
with open(out, 'w', encoding='utf-8') as f:
    json.dump(app.openapi(), f, indent=2)
try:
    with open('openapi.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(app.openapi(), f)
except Exception:
    pass
print('Wrote openapi.json and openapi.yaml if pyyaml available')
