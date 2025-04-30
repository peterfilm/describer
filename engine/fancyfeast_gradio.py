from gradio_client import Client, handle_file
from utils.exceptions import ServerError503

def fancyfeast_gradio(path, hf_token=None):
    client = Client("fancyfeast/joy-caption-pre-alpha", hf_token=hf_token) if hf_token else Client("fancyfeast/joy-caption-pre-alpha")
    result = client.predict(
        input_image=handle_file(path),
        api_name="/stream_chat"
        )
    if type(result) == str:
        return result
    else:
        raise ServerError503('Server Error')