
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
BASE_PATH = ROOT / "base.html"
DATABASE_PATH = ROOT / "database.html"
OUTPUT_PATH = ROOT / "index.html"
INSERT_MARKER = "<!-- DATABASE_CONTENT -->"
DATABASE_CSS = "database.css"


def extract_scripts(source: str):
    scripts = "\n".join(
        match.group(0)
        for match in re.finditer(r"<script\b[^>]*>.*?</script>", source, flags=re.DOTALL | re.IGNORECASE)
    )
    return scripts


def extract_body(source: str):
    match = re.search(r"<body\b[^>]*>(.*)</body>", source, flags=re.DOTALL | re.IGNORECASE)
    if not match:
        raise ValueError("Could not find <body> in database.html")

    body = match.group(1).strip()
    body = re.sub(r"\s*<script\b[^>]*>.*?</script>\s*", "\n", body, flags=re.DOTALL | re.IGNORECASE)
    return body.strip()


def build_index():
    if not BASE_PATH.exists():
        raise FileNotFoundError(f"Missing base template: {BASE_PATH}")
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(f"Missing database source: {DATABASE_PATH}")

    base_html = BASE_PATH.read_text(encoding="utf-8")
    database_html = DATABASE_PATH.read_text(encoding="utf-8")

    if INSERT_MARKER not in base_html:
        raise ValueError(f"Missing insertion marker: {INSERT_MARKER}")

    scripts = extract_scripts(database_html)
    body_content = extract_body(database_html)

    result = base_html.replace("</head>", f'<link rel="stylesheet" href="{DATABASE_CSS}">\n</head>', 1)
    result = result.replace(INSERT_MARKER, body_content, 1)
    result = result.replace("</body>", f"{scripts}\n</body>", 1)

    OUTPUT_PATH.write_text(result, encoding="utf-8")
    print(f"Built {OUTPUT_PATH.name} from {BASE_PATH.name} and {DATABASE_PATH.name} with {DATABASE_CSS}")


if __name__ == "__main__":
    build_index()

