# signaldeck_sdk/context.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol, Optional, Any

class FileService(Protocol):
    def save(self, file: Any, path: str) -> str:
        """Persist an uploaded file to `path` and return the final path."""
        ...

class Renderer(Protocol):
    def render(self, template: str, **kwargs) -> str:
        """Render a template with kwargs and return HTML."""
        ...

class UrlResolver(Protocol):
    def forFile(self, pluginName: str, filePath: str) -> str:
        """Return a URL for a file given its plugin name and path."""
        ...

@dataclass(frozen=True)
class ApplicationContext:
    """
    SDK-level context: only contracts/types, no Flask imports.
    Concrete implementation is provided by signaldeck-core.
    """
    renderer: Renderer
    url: UrlResolver
    files: FileService
    values: Any  # can be typed to ValueProvider later
    logger: Any  # can be typed later (logging.Logger)

    def render(self, template: str, **kwargs) -> str:
        return self.renderer.render(template, **kwargs)
