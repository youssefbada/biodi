from rest_framework.response import Response

def build_error_response(code: str, detail: str, status_code: int):
    return Response(
        {
            "code": code,
            "detail": detail,
        },
        status=status_code,
    )