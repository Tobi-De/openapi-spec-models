"""Test that all modules can be imported successfully."""


def test_import_main_package():
    """Test importing the main package."""
    import openapi_spec_models

    assert hasattr(openapi_spec_models, "__version__")
    assert openapi_spec_models.__version__ == "0.1.0"


def test_import_spec_models():
    """Test importing spec models."""
    from openapi_spec_models import (
        Components,
        Contact,
        Info,
        License,
        OpenAPI,
        Operation,
        Parameter,
        PathItem,
        Reference,
        Schema,
        Server,
    )

    # Just verify they're importable
    assert Info is not None
    assert OpenAPI is not None
    assert Schema is not None


def test_import_plugins():
    """Test importing render plugins."""
    from openapi_spec_models.plugins import (
        JsonRenderPlugin,
        OpenAPIRenderPlugin,
        RedocRenderPlugin,
        ScalarRenderPlugin,
        SwaggerRenderPlugin,
        YamlRenderPlugin,
    )

    # Verify they're importable
    assert OpenAPIRenderPlugin is not None
    assert JsonRenderPlugin is not None
    assert SwaggerRenderPlugin is not None


def test_create_simple_spec():
    """Test creating a simple OpenAPI spec."""
    from openapi_spec_models import Info, OpenAPI, OpenAPIResponse, Operation, PathItem

    spec = OpenAPI(
        openapi="3.0.3",
        info=Info(title="Test API", version="1.0.0"),
        paths={
            "/test": PathItem(
                get=Operation(
                    summary="Test endpoint", responses={"200": OpenAPIResponse(description="Success")}
                )
            )
        },
    )

    # Convert to dict
    spec_dict = spec.to_schema()

    assert spec_dict["openapi"] == "3.0.3"
    assert spec_dict["info"]["title"] == "Test API"
    assert spec_dict["info"]["version"] == "1.0.0"
    assert "/test" in spec_dict["paths"]
    assert "get" in spec_dict["paths"]["/test"]


def test_schema_model():
    """Test creating a Schema object."""
    from openapi_spec_models import Schema

    schema = Schema(
        type="object",
        properties={
            "name": Schema(type="string"),
            "age": Schema(type="integer"),
        },
        required=["name"],
    )

    schema_dict = schema.to_schema()

    assert schema_dict["type"] == "object"
    assert "name" in schema_dict["properties"]
    assert "age" in schema_dict["properties"]
    assert schema_dict["required"] == ["name"]


def test_json_plugin_instantiation():
    """Test that JsonRenderPlugin can be instantiated."""
    from openapi_spec_models.plugins import JsonRenderPlugin

    plugin = JsonRenderPlugin(path="/openapi.json")

    assert plugin.paths == ["/openapi.json"]
    assert plugin.media_type == "application/json"
    assert plugin.has_path("/openapi.json")
    assert not plugin.has_path("/other.json")


def test_swagger_plugin_instantiation():
    """Test that SwaggerRenderPlugin can be instantiated."""
    from openapi_spec_models.plugins import SwaggerRenderPlugin

    plugin = SwaggerRenderPlugin(path="/swagger")

    assert plugin.paths == ["/swagger"]
    assert plugin.media_type == "text/html"
    assert "swagger-ui-dist" in plugin.js_url
    assert "swagger-ui-dist" in plugin.css_url
