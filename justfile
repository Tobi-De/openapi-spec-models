# List available commands
default:
    @just --list

# Get current version from pyproject.toml
# 
version-get:
    @grep '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/'

# Bump patch version (0.1.0 -> 0.1.1)
version-bump-patch:
    #!/usr/bin/env python3
    import re
    from pathlib import Path

    pyproject = Path("pyproject.toml")
    content = pyproject.read_text()

    def bump_patch(match):
        version = match.group(1)
        major, minor, patch = map(int, version.split('.'))
        return f'version = "{major}.{minor}.{patch + 1}"'

    new_content = re.sub(r'version = "(\d+\.\d+\.\d+)"', bump_patch, content)
    pyproject.write_text(new_content)

    # Get new version
    new_version = re.search(r'version = "(\d+\.\d+\.\d+)"', new_content).group(1)
    print(f"Bumped to {new_version}")

# Bump minor version (0.1.0 -> 0.2.0)
version-bump-minor:
    #!/usr/bin/env python3
    import re
    from pathlib import Path

    pyproject = Path("pyproject.toml")
    content = pyproject.read_text()

    def bump_minor(match):
        version = match.group(1)
        major, minor, patch = map(int, version.split('.'))
        return f'version = "{major}.{minor + 1}.0"'

    new_content = re.sub(r'version = "(\d+\.\d+\.\d+)"', bump_minor, content)
    pyproject.write_text(new_content)

    # Get new version
    new_version = re.search(r'version = "(\d+\.\d+\.\d+)"', new_content).group(1)
    print(f"Bumped to {new_version}")

# Bump major version (0.1.0 -> 1.0.0)
version-bump-major:
    #!/usr/bin/env python3
    import re
    from pathlib import Path

    pyproject = Path("pyproject.toml")
    content = pyproject.read_text()

    def bump_major(match):
        version = match.group(1)
        major, minor, patch = map(int, version.split('.'))
        return f'version = "{major + 1}.0.0"'

    new_content = re.sub(r'version = "(\d+\.\d+\.\d+)"', bump_major, content)
    pyproject.write_text(new_content)

    # Get new version
    new_version = re.search(r'version = "(\d+\.\d+\.\d+)"', new_content).group(1)
    print(f"Bumped to {new_version}")

# Create git tag for current version
tag:
    #!/usr/bin/env bash
    VERSION=$(just version-get)
    echo "Creating tag v${VERSION}..."
    git tag -a "v${VERSION}" -m "Release v${VERSION}"
    echo "Tag v${VERSION} created. Push with: git push origin v${VERSION}"

# Release patch version (bump, commit, tag)
release-patch:
    just version-bump-patch
    git add pyproject.toml
    git commit -m "Bump version to $(just version-get)"
    just tag
    @echo ""
    @echo "Release ready! Push with:"
    @echo "  git push origin main"
    @echo "  git push origin v$(just version-get)"

# Release minor version (bump, commit, tag)
release-minor:
    just version-bump-minor
    git add pyproject.toml
    git commit -m "Bump version to $(just version-get)"
    just tag
    @echo ""
    @echo "Release ready! Push with:"
    @echo "  git push origin main"
    @echo "  git push origin v$(just version-get)"

# Release major version (bump, commit, tag)
release-major:
    just version-bump-major
    git add pyproject.toml
    git commit -m "Bump version to $(just version-get)"
    just tag
    @echo ""
    @echo "Release ready! Push with:"
    @echo "  git push origin main"
    @echo "  git push origin v$(just version-get)"

# Install the package in development mode
install:
    uv pip install -e .

# Install development dependencies
install-dev:
    uv sync --dev

# Run tests
test:
    uv run pytest

# Run tests with coverage
test-cov:
    uv run pytest --cov=openapi_spec_models --cov-report=term-missing

# Format code with black and isort
format:
    uv run black src/ tests/
    uv run isort src/ tests/

# Check code formatting
format-check:
    uv run black --check src/ tests/
    uv run isort --check src/ tests/

# Run type checking
typecheck:
    uv run mypy src/

# Run all checks (format, typecheck, tests)
check: format-check typecheck test

# Build the package
build:
    uv build

# Clean build artifacts
clean:
    rm -rf dist/ build/ *.egg-info .pytest_cache .coverage htmlcov/
    find . -type d -name __pycache__ -exec rm -rf {} +
