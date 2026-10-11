"""Give custom CSS and JavaScript content-specific URLs after each build."""
from hashlib import sha256
from pathlib import Path
import re


ASSETS = (
    "stylesheets/extra.css",
    "javascripts/mathjax.js",
    "javascripts/rl-learning.js",
)
ATTRIBUTE = re.compile(r'(?P<start>\b(?:href|src)=")(?P<url>[^\"]+)(?P<end>")')


def on_post_build(config, **kwargs):
    site_dir = Path(config["site_dir"])
    versions = {}
    for relative in ASSETS:
        asset = site_dir / relative
        content = asset.read_bytes()
        digest = sha256(content).hexdigest()[:12]
        versioned = asset.with_name(f"{asset.stem}.{digest}{asset.suffix}")
        versioned.write_bytes(content)
        versions[relative] = versioned.relative_to(site_dir).as_posix()

    def replace(match):
        url = match["url"]
        # Only rewrite this project's relative custom assets.
        if "://" in url or url.startswith("//"):
            return match[0]
        for relative, versioned in versions.items():
            if url == relative or url.endswith("/" + relative):
                prefix = url[:-len(relative)]
                return match["start"] + prefix + versioned + match["end"]
        return match[0]

    for page in site_dir.rglob("*.html"):
        original = page.read_text(encoding="utf-8")
        updated = ATTRIBUTE.sub(replace, original)
        if updated != original:
            page.write_text(updated, encoding="utf-8")
