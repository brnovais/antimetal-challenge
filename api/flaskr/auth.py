import base64


def extract_user(request):
    auth = request.headers.get("Authorization")
    if auth is not None:
        auth_seg = auth.split(" ")
        if len(auth_seg) == 2:
            return base64.b64decode(auth_seg[1]).decode("utf-8")

    return None
