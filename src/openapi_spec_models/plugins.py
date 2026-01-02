"""OpenAPI documentation render plugins for different UI frameworks."""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Sequence


__all__ = (
    "OpenAPIRenderPlugin",
    "JsonRenderPlugin",
    "YamlRenderPlugin",
    "RapidocRenderPlugin",
    "RedocRenderPlugin",
    "ScalarRenderPlugin",
    "StoplightRenderPlugin",
    "SwaggerRenderPlugin",
)

_default_favicon = "<link rel='icon' type='image/x-icon' href='data:image/x-icon;base64,AA'>"
_default_style = "<style>body { margin: 0; padding: 0 }</style>"


class OpenAPIRenderPlugin(ABC):
    """Base class for OpenAPI UI render plugins."""

    def __init__(
        self,
        *,
        path: str | Sequence[str],
        media_type: str = "text/html",
        favicon: str = _default_favicon,
        style: str = _default_style,
    ) -> None:
        """Initialize the OpenAPI UI render plugin.

        Args:
            path: Path(s) to serve this plugin at.
            media_type: HTTP media type for the response.
            favicon: HTML <link> tag for the favicon.
            style: Base styling CSS for the HTML body.
        """
        self.paths = [path] if isinstance(path, str) else list(path)
        self.media_type = media_type
        self.favicon = favicon
        self.style = style

    @staticmethod
    def render_json(openapi_schema: dict[str, Any]) -> bytes:
        """Render the OpenAPI schema as JSON.

        Args:
            openapi_schema: The OpenAPI schema as a dictionary.

        Returns:
            The rendered JSON as bytes.
        """
        return json.dumps(openapi_schema, indent=2).encode("utf-8")

    @abstractmethod
    def render(self, openapi_schema: dict[str, Any]) -> bytes:
        """Render the OpenAPI UI.

        Args:
            openapi_schema: The OpenAPI schema as a dictionary.

        Returns:
            The rendered content as bytes.
        """
        raise NotImplementedError

    def has_path(self, path: str) -> bool:
        """Check if the plugin handles a given path.

        Args:
            path: The path to check.

        Returns:
            True if the plugin handles this path.
        """
        return path in self.paths


class JsonRenderPlugin(OpenAPIRenderPlugin):
    """Render OpenAPI spec as JSON."""

    def __init__(self, path: str = "/openapi.json") -> None:
        """Initialize JSON render plugin.

        Args:
            path: Path to serve the JSON spec at.
        """
        super().__init__(path=path, media_type="application/json")

    def render(self, openapi_schema: dict[str, Any]) -> bytes:
        """Render the OpenAPI schema as JSON."""
        return self.render_json(openapi_schema)


class YamlRenderPlugin(OpenAPIRenderPlugin):
    """Render OpenAPI spec as YAML."""

    def __init__(self, path: str = "/openapi.yaml") -> None:
        """Initialize YAML render plugin.

        Args:
            path: Path to serve the YAML spec at.
        """
        super().__init__(path=path, media_type="application/x-yaml")

    def render(self, openapi_schema: dict[str, Any]) -> bytes:
        """Render the OpenAPI schema as YAML."""
        try:
            import yaml
        except ImportError as e:
            raise RuntimeError(
                "PyYAML is required to use YamlRenderPlugin. "
                "Install it with: pip install pyyaml"
            ) from e

        return yaml.dump(openapi_schema, default_flow_style=False, sort_keys=False).encode("utf-8")


class SwaggerRenderPlugin(OpenAPIRenderPlugin):
    """Render interactive Swagger UI documentation."""

    def __init__(
        self,
        path: str = "/swagger",
        version: str = "5.17.14",
        js_url: str | None = None,
        css_url: str | None = None,
        favicon: str = _default_favicon,
        **kwargs: Any,
    ) -> None:
        """Initialize Swagger UI plugin.

        Args:
            path: Path to serve Swagger UI at.
            version: Swagger UI version to load from CDN.
            js_url: Custom URL for swagger-ui-bundle.js (overrides version).
            css_url: Custom URL for swagger-ui.css (overrides version).
            favicon: HTML favicon tag.
            **kwargs: Additional arguments passed to parent.
        """
        super().__init__(path=path, favicon=favicon, **kwargs)
        self.js_url = js_url or f"https://cdn.jsdelivr.net/npm/swagger-ui-dist@{version}/swagger-ui-bundle.js"
        self.css_url = css_url or f"https://cdn.jsdelivr.net/npm/swagger-ui-dist@{version}/swagger-ui.css"

    def render(self, openapi_schema: dict[str, Any]) -> bytes:
        """Render Swagger UI HTML."""
        schema_json = json.dumps(openapi_schema)

        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{openapi_schema.get('info', {}).get('title', 'API')} - Swagger UI</title>
            <link rel="stylesheet" href="{self.css_url}">
            {self.favicon}
            {self.style}
        </head>
        <body>
            <div id="swagger-ui"></div>
            <script src="{self.js_url}"></script>
            <script>
                window.onload = function() {{
                    window.ui = SwaggerUIBundle({{
                        spec: {schema_json},
                        dom_id: '#swagger-ui',
                        deepLinking: true,
                        presets: [
                            SwaggerUIBundle.presets.apis,
                            SwaggerUIBundle.SwaggerUIStandalonePreset
                        ],
                        layout: "BaseLayout"
                    }});
                }};
            </script>
        </body>
        </html>
        """
        return html.encode("utf-8")


class RedocRenderPlugin(OpenAPIRenderPlugin):
    """Render Redoc documentation UI."""

    def __init__(
        self,
        path: str = "/redoc",
        version: str = "2.1.3",
        js_url: str | None = None,
        favicon: str = _default_favicon,
        **kwargs: Any,
    ) -> None:
        """Initialize Redoc plugin.

        Args:
            path: Path to serve Redoc at.
            version: Redoc version to load from CDN.
            js_url: Custom URL for redoc.standalone.js (overrides version).
            favicon: HTML favicon tag.
            **kwargs: Additional arguments passed to parent.
        """
        super().__init__(path=path, favicon=favicon, **kwargs)
        self.js_url = js_url or f"https://cdn.jsdelivr.net/npm/redoc@{version}/bundles/redoc.standalone.js"

    def render(self, openapi_schema: dict[str, Any]) -> bytes:
        """Render Redoc HTML."""
        schema_json = json.dumps(openapi_schema)

        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{openapi_schema.get('info', {}).get('title', 'API')} - Redoc</title>
            {self.favicon}
            {self.style}
        </head>
        <body>
            <div id="redoc"></div>
            <script src="{self.js_url}"></script>
            <script>
                Redoc.init(
                    {schema_json},
                    {{}},
                    document.getElementById('redoc')
                );
            </script>
        </body>
        </html>
        """
        return html.encode("utf-8")


class RapidocRenderPlugin(OpenAPIRenderPlugin):
    """Render RapiDoc documentation UI."""

    def __init__(
        self,
        path: str = "/rapidoc",
        version: str = "9.3.4",
        js_url: str | None = None,
        favicon: str = _default_favicon,
        **kwargs: Any,
    ) -> None:
        """Initialize RapiDoc plugin.

        Args:
            path: Path to serve RapiDoc at.
            version: RapiDoc version to load from CDN.
            js_url: Custom URL for rapidoc-min.js (overrides version).
            favicon: HTML favicon tag.
            **kwargs: Additional arguments passed to parent.
        """
        super().__init__(path=path, favicon=favicon, **kwargs)
        self.js_url = js_url or f"https://cdn.jsdelivr.net/npm/rapidoc@{version}/dist/rapidoc-min.js"

    def render(self, openapi_schema: dict[str, Any]) -> bytes:
        """Render RapiDoc HTML."""
        schema_json = json.dumps(openapi_schema)

        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{openapi_schema.get('info', {}).get('title', 'API')} - RapiDoc</title>
            {self.favicon}
            {self.style}
            <script type="module" src="{self.js_url}"></script>
        </head>
        <body>
            <rapi-doc
                spec-url=""
                render-style="read"
                theme="light"
                show-header="false"
            >
                <script type="application/json">{schema_json}</script>
            </rapi-doc>
        </body>
        </html>
        """
        return html.encode("utf-8")


class ScalarRenderPlugin(OpenAPIRenderPlugin):
    """Render Scalar API documentation UI."""

    def __init__(
        self,
        path: str = "/scalar",
        version: str = "1.24.0",
        js_url: str | None = None,
        css_url: str | None = None,
        favicon: str = _default_favicon,
        **kwargs: Any,
    ) -> None:
        """Initialize Scalar plugin.

        Args:
            path: Path to serve Scalar at.
            version: Scalar version to load from CDN.
            js_url: Custom URL for standalone.js (overrides version).
            css_url: Custom URL for style.css (overrides version).
            favicon: HTML favicon tag.
            **kwargs: Additional arguments passed to parent.
        """
        super().__init__(path=path, favicon=favicon, **kwargs)
        self.js_url = js_url or f"https://cdn.jsdelivr.net/npm/@scalar/api-reference@{version}"
        self.css_url = css_url

    def render(self, openapi_schema: dict[str, Any]) -> bytes:
        """Render Scalar HTML."""
        schema_json = json.dumps(openapi_schema)

        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{openapi_schema.get('info', {}).get('title', 'API')} - Scalar</title>
            {self.favicon}
            {self.style}
        </head>
        <body>
            <script
                id="api-reference"
                data-configuration='{{"theme": "purple"}}'
                type="application/json"
            >
                {schema_json}
            </script>
            <script src="{self.js_url}"></script>
        </body>
        </html>
        """
        return html.encode("utf-8")


class StoplightRenderPlugin(OpenAPIRenderPlugin):
    """Render Stoplight Elements documentation UI."""

    def __init__(
        self,
        path: str = "/elements",
        version: str = "8.0.4",
        js_url: str | None = None,
        css_url: str | None = None,
        favicon: str = _default_favicon,
        **kwargs: Any,
    ) -> None:
        """Initialize Stoplight Elements plugin.

        Args:
            path: Path to serve Elements at.
            version: Elements version to load from CDN.
            js_url: Custom URL for web-components.min.js (overrides version).
            css_url: Custom URL for styles.min.css (overrides version).
            favicon: HTML favicon tag.
            **kwargs: Additional arguments passed to parent.
        """
        super().__init__(path=path, favicon=favicon, **kwargs)
        self.js_url = js_url or f"https://cdn.jsdelivr.net/npm/@stoplight/elements@{version}/web-components.min.js"
        self.css_url = css_url or f"https://cdn.jsdelivr.net/npm/@stoplight/elements@{version}/styles.min.css"

    def render(self, openapi_schema: dict[str, Any]) -> bytes:
        """Render Stoplight Elements HTML."""
        schema_json = json.dumps(openapi_schema)

        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{openapi_schema.get('info', {}).get('title', 'API')} - Stoplight</title>
            <link rel="stylesheet" href="{self.css_url}">
            {self.favicon}
            {self.style}
        </head>
        <body>
            <elements-api
                apiDescriptionDocument='{schema_json}'
                router="hash"
                layout="sidebar"
            />
            <script src="{self.js_url}"></script>
        </body>
        </html>
        """
        return html.encode("utf-8")
