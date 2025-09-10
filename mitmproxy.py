from mitmproxy import http
import base64
import zlib
import urllib.parse

def decode_saml_request(encoded_request: str) -> str:
    decoded = urllib.parse.unquote(encoded_request)
    data = base64.b64decode(decoded)
    try:
        xml = zlib.decompress(data, -15).decode("utf-8")
    except zlib.error:
        xml = data.decode("utf-8")
    return xml

def decode_saml_response(encoded_response: str) -> str:
    data = base64.b64decode(encoded_response)
    return data.decode("utf-8")

def request(flow: http.HTTPFlow) -> None:
    if "SAMLRequest" in flow.request.query:
        saml_req = flow.request.query["SAMLRequest"]
        print("\n===== SAMLRequest (SP → ADFS) =====")
        print(decode_saml_request(saml_req))

def response(flow: http.HTTPFlow) -> None:
    if flow.request.method == "POST" and flow.request.urlencoded_form:
        if "SAMLResponse" in flow.request.urlencoded_form:
            saml_resp = flow.request.urlencoded_form["SAMLResponse"]
            print("\n===== SAMLResponse (ADFS → SP) =====")
            print(decode_saml_response(saml_resp))
