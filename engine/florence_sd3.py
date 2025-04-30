from gradio_client import Client, handle_file
from utils.exceptions import ServerError503

def florence_sd3(path, hf_token=None):
    client = Client("gokaygokay/Florence-2-SD3-Captioner", hf_token=hf_token) if hf_token else Client("gokaygokay/Florence-2-SD3-Captioner")
    result = client.predict(
        image=handle_file(path),
        api_name="/run_example"
    )
    print(result)
    if type(result) == str:
        return result
    else:
        raise ServerError503('Server Error')