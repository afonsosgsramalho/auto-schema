import base64
import requests


def mm_ink(graphbytes):
    """Given a bytes object holding a Mermaid-format graph, return a URL that will generate the image."""
    base64_bytes = base64.b64encode(graphbytes)
    base64_string = base64_bytes.decode("ascii")
    return "https://mermaid.ink/img/" + base64_string


def mm(graph):
    """Given a string containing a Mermaid-format graph, save it to file."""
    graphbytes = graph.encode("ascii")
    image_url = mm_ink(graphbytes)
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()
        with open("mermaid_diagram.png", "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print("Mermaid diagram saved to mermaid_diagram.png")
        print(f'You can also see the result in {image_url}')

    except requests.exceptions.RequestException as e:
        print(f"Error fetching or saving image: {e}")
