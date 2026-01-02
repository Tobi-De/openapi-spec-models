"""Framework-agnostic OpenAPI 3.0 specification models and render plugins.

This package provides:
- Complete OpenAPI 3.0 spec dataclass models
- Multiple documentation UI render plugins (Swagger, Redoc, Scalar, etc.)
- Framework-agnostic design that works with any Python web framework
"""

from . import spec
from .plugins import (
    JsonRenderPlugin,
    OpenAPIRenderPlugin,
    RapidocRenderPlugin,
    RedocRenderPlugin,
    ScalarRenderPlugin,
    StoplightRenderPlugin,
    SwaggerRenderPlugin,
    YamlRenderPlugin,
)
from .spec import (
    Callback,
    Components,
    Contact,
    Discriminator,
    Encoding,
    Example,
    ExternalDocumentation,
    Info,
    License,
    Link,
    OAuthFlow,
    OAuthFlows,
    OpenAPI,
    OpenAPIFormat,
    OpenAPIHeader,
    OpenAPIMediaType,
    OpenAPIResponse,
    OpenAPIType,
    Operation,
    Parameter,
    PathItem,
    Paths,
    Reference,
    RequestBody,
    Responses,
    Schema,
    SecurityRequirement,
    SecurityScheme,
    Server,
    ServerVariable,
    Tag,
    XML,
)

__version__ = "0.1.0"

__all__ = (
    # Version
    "__version__",
    # Spec module
    "spec",
    # Spec models
    "Callback",
    "Components",
    "Contact",
    "Discriminator",
    "Encoding",
    "Example",
    "ExternalDocumentation",
    "Info",
    "License",
    "Link",
    "OAuthFlow",
    "OAuthFlows",
    "OpenAPI",
    "OpenAPIFormat",
    "OpenAPIHeader",
    "OpenAPIMediaType",
    "OpenAPIResponse",
    "OpenAPIType",
    "Operation",
    "Parameter",
    "PathItem",
    "Paths",
    "Reference",
    "RequestBody",
    "Responses",
    "Schema",
    "SecurityRequirement",
    "SecurityScheme",
    "Server",
    "ServerVariable",
    "Tag",
    "XML",
    # Render plugins
    "OpenAPIRenderPlugin",
    "JsonRenderPlugin",
    "YamlRenderPlugin",
    "RapidocRenderPlugin",
    "RedocRenderPlugin",
    "ScalarRenderPlugin",
    "StoplightRenderPlugin",
    "SwaggerRenderPlugin",
)
