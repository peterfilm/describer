from gradio_client import Client, handle_file
from utils.exceptions import ServerError503

def florence(path, hf_token=None):
    client = Client("gokaygokay/Florence-2", hf_token=hf_token) if hf_token else Client("gokaygokay/Florence-2")
    result = client.predict(
        image=handle_file(path),
        task_prompt="More Detailed Caption",
        text_input=None,
        model_id="microsoft/Florence-2-large",
        api_name="/process_image"
    )[0]
    if type(result) == str:
        return result[29:-2]
    else:
        raise ServerError503('Server Error')