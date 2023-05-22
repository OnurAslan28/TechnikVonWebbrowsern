import socket
import ssl
import gzip


def request(url, allow_compressed=True):
    scheme, url = url.split("://", 1)
    assert scheme in ["http", "https", "file"], \
        "Unknown scheme {}".format(scheme)
    port = 80 if scheme == "http" else 443

    # File Urls (Exercise 1.2)
    if scheme == "file":
        f = open(url, "r")
        ftext = f.read()
        return {}, ftext

    if "/" in url:
        host, path = url.split("/", 1)
        path = "/" + path
    else:
        host = url
        path = "/"

    if ":" in host:
        host, port = host.split(":", 1)
        port = int(port)

    s = socket.socket(
        family=socket.AF_INET,
        type=socket.SOCK_STREAM,
        proto=socket.IPPROTO_TCP,
    )

    s.connect((host, port))
    if scheme == "https":
        ctx = ssl.create_default_context()
        s = ctx.wrap_socket(s, server_hostname=host)

    send_headers = {
        "User-Agent: ": "frosted browser",
        "Connection: ": "close"
    }
    if allow_compressed:
        send_headers["Accept-Encoding: "] = "gzip"

    header_string = ""
    for x, y in send_headers.items():
        header_string = header_string + x + y + "\r\n"

    s.send("GET {} HTTP/1.1\r\n".format(path).encode("utf8")
           + "Host: {}\r\n".format(host).encode("utf8")
           + header_string.encode("utf8")
           + b"\r\n")

    response = s.makefile("rb", encoding="utf8", newline="\r\n")
    statusline = response.readline().decode("utf-8").strip("\r\n")
    version, status, explanation = statusline.split(" ", 2)
    assert status == "200", "{}: {}".format(status, explanation)
    headers = {}
    while True:
        line = response.readline().decode("utf-8")
        if line == "\r\n":
            break
        header, value = line.split(":", 1)
        headers[header.lower()] = value.strip()

    body = response.read()
    if headers.keys().__contains__("transfer-encoding"):
        assert headers["transfer-encoding"] == "chunked"
        body = dechunk(body)

    if headers.keys().__contains__("content-encoding"):
        assert headers["content-encoding"] == "gzip"
        body = gzip.decompress(body).decode("utf-8")
    else:
        body = body.decode("utf-8")
    s.close()
    return headers, body


def dechunk(chunked_body):
    chunks = []
    while True:
        next_length, chunked_body = chunked_body.split(b'\r\n', 1)
        length = int(next_length.decode("utf-8"), base=16)
        if length == 0:
            assert chunked_body == b'\r\n'
            break
        chunks.append(chunked_body[0:length])
        chunked_body = chunked_body[length + 2:]
    body = b''.join(chunks)
    return body
