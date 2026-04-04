import argparse
import subprocess
from pathlib import Path


CSS = """
@page {
  size: Letter;
  margin: 0.64in 0.72in 0.68in 0.72in;
}

:root {
  /* Colors */
  --text: #222222;
  --muted: #5a5a5a;

  /* Type scale */
  --fs-base: 10pt;
  --fs-h1: 2.8rem;
  --fs-h2: 1.28rem;
  --fs-h3: 1.06rem;
  --fs-h4: 0.92rem;
  --fs-meta: 0.94rem;
  --fs-small: 0.78rem;

  /* Line heights */
  --lh-body: 1.19;
  --lh-tight: 1.1;
  --lh-title: 1.06;
  --lh-name: 0.98;

  /* Spacing scale */
  --space-0: 0;
  --space-1: 0.12rem;
  --space-2: 0.22rem;
  --space-3: 0.36rem;
  --space-4: 0.56rem;
  --space-5: 0.84rem;
  --space-6: 1.2rem;
}

html {
  font-size: var(--fs-base);
}

body {
  margin: 0;
  font-family: "Noto Sans", sans-serif;
  color: var(--text);
  line-height: var(--lh-body);
}

body > :first-child {
  margin-top: 0 !important;
}

h1, h2, h3, h4, p, ul, ol, li {
  orphans: 2;
  widows: 2;
}

h2, h3, h4 {
  page-break-after: avoid;
}

/* Base block rhythm */
p {
  margin: 0 0 var(--space-3) 0;
}

ul,
ol {
  margin: var(--space-2) 0 var(--space-4) 0.72rem;
  padding: 0;
}

li {
  margin: 0 0 var(--space-1) 0;
  padding: 0;
}

p,
li {
  max-width: none;
}

ul li::marker {
  content: "– ";
}

/* Links */
a {
  color: inherit;
  text-decoration-thickness: 0.01em;
  text-underline-offset: 0.1em;
}

strong {
  font-weight: 600;
}

/* Headings */
h1 {
  font-size: var(--fs-h1);
  line-height: var(--lh-name);
  font-weight: 700;
  letter-spacing: -0.032em;
  margin: 0 0 var(--space-5) 0;
}

h2 {
  font-size: var(--fs-h2);
  line-height: var(--lh-title);
  font-weight: 700;
  letter-spacing: -0.008em;
  margin: var(--space-6) 0 var(--space-4) 0;
}

h3 {
  font-size: var(--fs-h3);
  line-height: var(--lh-tight);
  font-weight: 700;
  margin: var(--space-5) 0 var(--space-2) 0;
}

h4 {
  font-size: var(--fs-h4);
  line-height: var(--lh-tight);
  font-weight: 400;
  color: var(--muted);
  margin: 0 0 var(--space-1) 0;
}

/* Experience description spacing */
h4 + p {
  margin-top: var(--space-3);
}

/* Header block from pure markdown */
h1 + p {
  font-size: var(--fs-meta);
  line-height: 1.12;
  margin-bottom: var(--space-4);
}

h1 + p + p {
  font-size: var(--fs-meta);
  line-height: 1.14;
  color: var(--muted);
  margin-bottom: var(--space-4);
}

h1 + p + p + p {
  margin-bottom: var(--space-5);
}

/* Floaty arXiv publication links */
h2 + ul a {
  font-size: 0.68em;
  vertical-align: super;
  white-space: nowrap;
  letter-spacing: 0;
  display: inline-block;
  line-height: 1;
  color: var(--muted);
}

/* Publication list */
h2 + ul {
  margin-top: var(--space-1);
}

h2 + ul li {
  margin-bottom: var(--space-2);
}

/* Reduce excess gap when a section starts with an employer/institution */
h2 + h3 {
  margin-top: 0;
}
"""


HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>{title}</title>
  <style>{css}</style>
</head>
<body>
{body}
</body>
</html>
"""


def run_command(args: list[str]) -> None:
    subprocess.run(args, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a minimalist PDF resume from Markdown.")
    parser.add_argument("input", type=Path, help="Input file (markdown)")
    parser.add_argument("output", type=Path, help="Output file (pdf)")
    parser.add_argument("--title", default="Thom Lake: Resume")
    args = parser.parse_args()

    input_file: Path = args.input.resolve()
    output_file: Path = args.output.resolve()
    output_file.parent.mkdir(parents=True, exist_ok=True)

    build_dir = Path("./build")
    body_html = build_dir / "body.html"
    full_html = build_dir / "resume.html"

    # Convert Markdown -> HTML fragment.
    run_command([
        "pandoc",
        str(input_file),
        "--from", "gfm",
        "--to", "html5",
        "--standalone=false",
        "-o", str(body_html),
    ])

    body = body_html.read_text(encoding="utf-8")
    html = HTML_TEMPLATE.format(title=args.title, css=CSS, body=body)
    full_html.write_text(html, encoding="utf-8")

    # HTML -> PDF.
    run_command(["weasyprint", str(full_html), str(output_file)])

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
