"""
Django Rest Framework Settings.
This module defines how the API handles authentication, permissions, errors, pagination, parsing and schema generation.

- Every API endpoint requires a logged in user by default (authentication)
- If request has no valid auth, we return a structured error message
- JWT is used for secure token authentication
- Spectacular is used to generate OpenAPI(swagger) schema
- All list endpoints are paginated automatically
- Accepts JSON, Form and MultiPart parsers
"""


REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "EXCEPTION_HANDLER": "drf_standardized_errors.handler.exception_handler",
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "includes.helpers.APIPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ],
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Auth API",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
    "SCHEMA_PATH_PREFIX": "/api/v[0-9]",
    "COMPONENTS": {
        "securitySchemes": {
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            },
        },
    },
    "SECURITY": [
        {"bearerAuth": []},
    ],
    "SWAGGER_UI_SETTINGS": {
        "persistAuthorization": True,
    },
}

DRF_STANDARDIZED_ERRORS = {
    "EXCEPTION_HANDLER_CLASS": "drf_standardized_errors.handler.ExceptionHandler",
    "EXCEPTION_FORMATTER_CLASS": "includes.helpers. ExceptionFormatter",
    "ENABLE_IN_DEBUG_FOR_UNHANDLED_EXCEPTIONS": False,
    "NESTED_FIELD_SEPARATOR": ".",
}
