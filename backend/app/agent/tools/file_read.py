import os
from pathlib import Path
from typing import Dict, Any
from app.core.config import settings

class FileReadTool:
    name = "file_read"
    display_name = "File Read"
    description = "Safely read files from the sandboxed storage directory with path traversal protection."
    is_sensitive = False

    @classmethod
    def execute(cls, file_path: str) -> Dict[str, Any]:
        # Path traversal security check
        normalized_path = os.path.normpath(file_path)
        
        # Check for traversal sequences
        if ".." in normalized_path or normalized_path.startswith("/") or (len(normalized_path) > 1 and normalized_path[1] == ":"):
            # Check if it attempts to escape sandbox
            full_path = (settings.SANDBOX_DIR / normalized_path.lstrip("/\\")).resolve()
        else:
            full_path = (settings.SANDBOX_DIR / normalized_path).resolve()

        # Strict containment verification
        sandbox_resolved = settings.SANDBOX_DIR.resolve()
        if not str(full_path).startswith(str(sandbox_resolved)):
            return {
                "success": False,
                "error": "SECURITY VIOLATION (ASI02): Path traversal blocked. Access outside sandbox directory is prohibited.",
                "attempted_path": file_path,
                "sanitized_path": str(full_path),
                "blocked": True
            }

        if not full_path.exists():
            return {
                "success": False,
                "error": f"File not found in sandbox: {file_path}",
                "attempted_path": file_path,
                "blocked": False
            }

        try:
            with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            return {
                "success": True,
                "content": content[:4000],
                "file_size": len(content),
                "path": str(full_path.relative_to(sandbox_resolved)),
                "blocked": False
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Read error: {str(e)}",
                "blocked": False
            }
