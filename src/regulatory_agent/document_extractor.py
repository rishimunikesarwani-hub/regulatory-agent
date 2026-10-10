"""Extract bounded source locations in an isolated process without operational content logs."""
import csv
from io import BytesIO, StringIO
import json
import logging
import math
import sys
import xml.etree.ElementTree as ET
import zipfile


class Rejected(ValueError):
    pass


def extract(kind, data):
    passages = []
    pages = 0
    size = 0

    def add(location, text):
        nonlocal size
        if text.strip():
            size += len(text.encode("utf-8")) + (1 if passages else 0)
            if size > 400_000:
                raise Rejected("extraction_limit")
            passages.append({"location": location, "text": text})

    if kind in {"txt", "csv"}:
        text = data.decode("utf-8-sig")
        if text.startswith(("%PDF-", "PK\x03\x04")) or any(ord(c) < 32 and c not in "\n\r\t" for c in text):
            raise Rejected("invalid_document")
        if kind == "txt":
            for index, line in enumerate(text.splitlines(), 1):
                add(f"Line {index}", line)
        else:
            csv.field_size_limit(400_000)
            lines = text.splitlines(keepends=True)
            reader = csv.reader(StringIO(text, newline=""), strict=True)
            previous = 0
            for index, _row in enumerate(reader, 1):
                end = reader.line_num
                location = f"Row {index}" if end == previous + 1 else f"Row {index} (lines {previous + 1}-{end})"
                add(location, "".join(lines[previous:end]).rstrip("\r\n"))
                previous = end
    elif kind == "docx":
        with zipfile.ZipFile(BytesIO(data)) as archive:
            def part(name):
                info = archive.getinfo(name)
                if info.flag_bits & 1 or info.file_size > 10_000_000:
                    raise Rejected("invalid_document")
                content = archive.read(name)
                if b"<!DOCTYPE" in content.upper() or b"<!ENTITY" in content.upper():
                    raise Rejected("invalid_document")
                return ET.fromstring(content)
            if any(name.lower().endswith("vbaproject.bin") for name in archive.namelist()):
                raise Rejected("invalid_document")
            types = part("[Content_Types].xml")
            if not any(node.get("PartName") == "/word/document.xml" and node.get("ContentType") ==
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml" for node in types):
                raise Rejected("invalid_document")
            root = part("word/document.xml")
            namespace = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
            if root.tag != namespace + "document":
                raise Rejected("invalid_document")
            for index, paragraph in enumerate(root.iter(namespace + "p"), 1):
                text = "".join(node.text or "" if node.tag == namespace + "t" else "\t" if node.tag == namespace + "tab"
                               else "\n" if node.tag == namespace + "br" else "" for node in paragraph.iter())
                add(f"Paragraph {index}", text)
    elif kind == "pdf":
        from pypdf import PdfReader, filters
        if not data.startswith(b"%PDF-"):
            raise Rejected("invalid_document")
        filters.MAX_OUTPUT_LENGTH = 10_000_000
        reader = PdfReader(BytesIO(data), strict=True)
        if reader.is_encrypted:
            raise Rejected("encrypted_document")
        pages = len(reader.pages)
        if not 1 <= pages <= 100:
            raise Rejected("extraction_limit")
        decoded_size = 0
        for index, page in enumerate(reader.pages, 1):
            stream = page.get_contents()
            decoded_size += len(stream.get_data()) if stream else 0
            if decoded_size > 10_000_000:
                raise Rejected("extraction_limit")
            text = page.extract_text()
            if not text or not text.strip():
                raise Rejected("unreadable_document")
            add(f"Page {index}", text)
    else:
        raise Rejected("unsupported_format")
    if not passages:
        raise Rejected("unreadable_document")
    return {"passages": passages, "units": max(pages, math.ceil(size / 4000)), "text_bytes": size}


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    try:
        data = sys.stdin.buffer.read(10_000_001)
        if not 0 < len(data) <= 10_000_000:
            raise Rejected("invalid_document")
        result = extract(sys.argv[1], data)
    except Rejected as error:
        result = {"error": str(error)}
    except Exception:
        result = {"error": "invalid_document"}
    sys.stdout.write(json.dumps(result, ensure_ascii=True))
