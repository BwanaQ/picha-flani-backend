import json

from rest_framework.renderers import JSONRenderer


class APIJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        # If we receive a `token` key as part of the response, it will be a
        # byte object. Byte objects don't serialize well, so we need to
        # decode it before rendering the User object.

            # Also as mentioned above, we will decode `token` if it is of type
            # bytes.
  
        # Get the status code from the renderer context
        response_status_code = renderer_context['response'].status_code

        # Finally, we can render our data along with the status code
        response_data = {'status_code': response_status_code, "data":data}
        return super().render(response_data, media_type, renderer_context)