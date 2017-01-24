import json
from rest_framework.renderers import BaseRenderer


class PrtgRenderer(BaseRenderer):
    media_type = 'application/json'
    format = 'prtg'

    def render(self, data, media_type=None, renderer_context=None):
        return json.dumps(data)
