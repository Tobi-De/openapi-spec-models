# OpenAPI Spec Models

> [!Note]
> This code was shamelessly stolen from [Litestar](https://github.com/litestar-org/litestar/tree/main/litestar/openapi), and Claude Code did the work to make it framework-agnostic.

Framework-agnostic OpenAPI 3.0 specification models and render plugins for Python.

## Features

- **Complete OpenAPI 3.0 Spec Models**: Full dataclass-based implementation of the OpenAPI 3.0 specification
- **Multiple Documentation UIs**: Built-in render plugins for Swagger UI, Redoc, Scalar, RapiDoc, and Stoplight Elements
- **Framework-Agnostic**: Works with any Python web framework (Django, Flask, FastAPI, Litestar, etc.)
- **Type-Safe**: Full type annotations with mypy support
- **Lightweight**: Minimal dependencies (only `typing-extensions` required)
- **Zero Runtime Overhead**: Pure Python dataclasses with no heavy dependencies

## Installation

```bash
pip install openapi-spec-models
```

For YAML support:

```bash
pip install openapi-spec-models[yaml]
```

## Quick Start

### Creating an OpenAPI Specification

```python
from openapi_spec_models import OpenAPI, Info, PathItem, Operation, OpenAPIResponse

# Create an OpenAPI spec
spec = OpenAPI(
    openapi="3.0.3",
    info=Info(
        title="My API",
        version="1.0.0",
        description="A sample API"
    ),
    paths={
        "/users": PathItem(
            get=Operation(
                summary="List users",
                responses={
                    "200": OpenAPIResponse(description="Success")
                }
            )
        )
    }
)

# Convert to dictionary
spec_dict = spec.to_schema()
```

### Using Render Plugins

The package includes several render plugins for generating beautiful API documentation:

```python
from openapi_spec_models.plugins import (
    SwaggerRenderPlugin,
    RedocRenderPlugin,
    ScalarRenderPlugin,
)

# Create plugins
swagger = SwaggerRenderPlugin(path="/swagger")
redoc = RedocRenderPlugin(path="/redoc")
scalar = ScalarRenderPlugin(path="/scalar")

# Render documentation
html = swagger.render(spec_dict)
```

## Available Render Plugins

- **JsonRenderPlugin**: Renders the spec as JSON
- **YamlRenderPlugin**: Renders the spec as YAML (requires `pyyaml`)
- **SwaggerRenderPlugin**: Interactive Swagger UI
- **RedocRenderPlugin**: Redoc documentation UI
- **ScalarRenderPlugin**: Modern Scalar API documentation
- **RapidocRenderPlugin**: RapiDoc UI
- **StoplightRenderPlugin**: Stoplight Elements UI

## OpenAPI Spec Models

The package provides complete dataclass models for the OpenAPI 3.0 specification:

- `OpenAPI`: Root OpenAPI document
- `Info`, `Contact`, `License`: API metadata
- `Server`, `ServerVariable`: Server configuration
- `PathItem`, `Operation`: Endpoint definitions
- `Parameter`, `RequestBody`, `OpenAPIResponse`: Request/response models
- `Schema`: JSON Schema for data types
- `Components`: Reusable components
- `SecurityScheme`, `SecurityRequirement`: Security definitions
- And many more...

## Framework Integration

This package is framework-agnostic. Here's how you might integrate it with different frameworks:

### Django

```python
from django.http import HttpResponse
from openapi_spec_models.plugins import SwaggerRenderPlugin

plugin = SwaggerRenderPlugin(path="/swagger")

def swagger_view(request):
    # Generate your OpenAPI spec dict
    openapi_spec_dict = {...}

    html = plugin.render(openapi_spec_dict)
    return HttpResponse(html, content_type=plugin.media_type)
```

### Flask

```python
from flask import Response
from openapi_spec_models.plugins import RedocRenderPlugin

plugin = RedocRenderPlugin(path="/redoc")

@app.route("/redoc")
def redoc():
    # Generate your OpenAPI spec dict
    openapi_spec_dict = {...}

    html = plugin.render(openapi_spec_dict)
    return Response(html, mimetype=plugin.media_type)
```

### FastAPI

While FastAPI has its own OpenAPI implementation, you can use these models for advanced customization:

```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from openapi_spec_models.plugins import ScalarRenderPlugin

plugin = ScalarRenderPlugin(path="/scalar")

@app.get("/scalar", response_class=HTMLResponse)
async def scalar():
    spec = app.openapi()
    html = plugin.render(spec)
    return html
```

## Development

```bash
# Clone the repository
git clone https://github.com/yourusername/openapi-spec-models.git
cd openapi-spec-models

# Install with uv
uv sync

# Run tests
just test

# Run tests with coverage
just test-cov

# Format code
just format

# Check code quality
just check
```

### Available Commands (using `just`)

This project uses [just](https://github.com/casey/just) for task automation. Here are the available commands:

**Development:**
- `just install` - Install package in development mode
- `just install-dev` - Install development dependencies
- `just test` - Run tests
- `just test-cov` - Run tests with coverage
- `just format` - Format code with black and isort
- `just format-check` - Check code formatting
- `just typecheck` - Run mypy type checking
- `just check` - Run all checks (format, typecheck, tests)

**Building:**
- `just build` - Build distribution packages
- `just clean` - Clean build artifacts

**Version Management:**
- `just version-get` - Display current version
- `just version-bump-patch` - Bump patch version (0.1.0 → 0.1.1)
- `just version-bump-minor` - Bump minor version (0.1.0 → 0.2.0)
- `just version-bump-major` - Bump major version (0.1.0 → 1.0.0)

**Releasing:**
- `just release-patch` - Bump patch version, commit, and create tag
- `just release-minor` - Bump minor version, commit, and create tag
- `just release-major` - Bump major version, commit, and create tag

### Release Process

This package uses PyPI Trusted Publishers for automated releases:

1. Create a release using just:
   ```bash
   just release-patch  # or release-minor, release-major
   ```

2. Push the commit and tag:
   ```bash
   git push origin main
   git push origin v0.1.1  # replace with your version
   ```

3. GitHub Actions will automatically build and publish to PyPI when the tag is pushed.

**First-time setup:** Configure the PyPI Trusted Publisher in your PyPI project settings:
- Publisher: GitHub
- Owner: `yourusername`
- Repository: `openapi-spec-models`
- Workflow: `publish.yml`
- Environment: `pypi`

## Credits

This package is derived from and inspired by [Litestar's](https://github.com/litestar-org/litestar) OpenAPI implementation, adapted to be framework-agnostic.

## License

MIT License - see LICENSE file for details.
