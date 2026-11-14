import os
import re
from typing import List, Dict, Any

class DocumentProcessor:
    @staticmethod
    def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        words = text.split()
        if not words:
            return []
        
        chunks = []
        i = 0
        while i < len(words):
            chunk_words = words[i:i + chunk_size]
            chunks.append(" ".join(chunk_words))
            i += chunk_size - overlap
            if i >= len(words):
                break
        return chunks

    @staticmethod
    def extract_text(filename: str, content_bytes: bytes) -> str:
        ext = os.path.splitext(filename)[1].lower()
        if ext in [".txt", ".md", ".json", ".csv", ".log"]:
            return content_bytes.decode("utf-8", errors="ignore")
        elif ext == ".pdf":
            # Basic pure-python pdf text extraction
            text = content_bytes.decode("latin1", errors="ignore")
            # Extract readable streams
            streams = re.findall(r"stream[\r\n]+(.*?)[\r\n]+endstream", text, re.DOTALL)
            clean_text = " ".join(streams) if streams else text
            # Fallback to plain readable ASCII strings
            readable = "".join([c if 32 <= ord(c) <= 126 or c in "\n\t" else " " for c in clean_text])
            return " ".join(readable.split())
        else:
            # Generic binary fallback
            readable = "".join([chr(b) if 32 <= b <= 126 or b in [10, 13, 9] else " " for b in content_bytes])
            return " ".join(readable.split())
