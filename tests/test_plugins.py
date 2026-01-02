"""Test render plugins."""

import json


def test_json_plugin_render():
    """Test JsonRenderPlugin renders JSON correctly."""
    from openapi_spec_models.plugins import JsonRenderPlugin

    plugin = JsonRenderPlugin(path="/openapi.json")

    spec = {
        "openapi": "3.0.3",
        "info": {"title": "Test API", "version": "1.0.0"},
        "paths": {},
    }

    result = plugin.render(spec)

    assert isinstance(result, bytes)
    parsed = json.loads(result)
    assert parsed["openapi"] == "3.0.3"
    assert parsed["info"]["title"] == "Test API"


def test_swagger_plugin_render():
    """Test SwaggerRenderPlugin renders HTML."""
    from openapi_spec_models.plugins import SwaggerRenderPlugin

    plugin = SwaggerRenderPlugin(path="/swagger")

    spec = {
        "openapi": "3.0.3",
        "info": {"title": "Test API", "version": "1.0.0"},
        "paths": {},
    }

    result = plugin.render(spec)

    assert isinstance(result, bytes)
    html = result.decode("utf-8")
    assert "<!DOCTYPE html>" in html
    assert "swagger-ui" in html
    assert "Test API" in html


def test_redoc_plugin_render():
    """Test RedocRenderPlugin renders HTML."""
    from openapi_spec_models.plugins import RedocRenderPlugin

    plugin = RedocRenderPlugin(path="/redoc")

    spec = {
        "openapi": "3.0.3",
        "info": {"title": "Test API", "version": "1.0.0"},
        "paths": {},
    }

    result = plugin.render(spec)

    html = result.decode("utf-8")
    assert "<!DOCTYPE html>" in html
    assert "redoc" in html.lower()
    assert "Test API" in html


def test_plugin_multiple_paths():
    """Test plugin with multiple paths."""
    from openapi_spec_models.plugins import JsonRenderPlugin

    plugin = JsonRenderPlugin(path=["/openapi.json", "/schema.json"])

    assert len(plugin.paths) == 2
    assert plugin.has_path("/openapi.json")
    assert plugin.has_path("/schema.json")
    assert not plugin.has_path("/other.json")
