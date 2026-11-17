"""Remove the com.springsource.bundlor.maven plugin blocks from a pom.

Usage: strip-bundlor.py <input pom> <output pom>
"""
import re
import sys

src, dst = sys.argv[1], sys.argv[2]
with open(src, encoding="utf-8") as f:
    pom = f.read()

pattern = re.compile(
    r"[ \t]*<plugin>\s*<groupId>com\.springsource\.bundlor</groupId>.*?</plugin>[ \t]*\n",
    re.DOTALL,
)
pom, removed = pattern.subn("", pom)
if removed == 0 or "com.springsource.bundlor" in pom:
    sys.exit("bundlor plugin blocks not found or not fully removed (removed=%d)" % removed)

# maven-jar-plugin reads the MANIFEST.MF that bundlor wrote into target/classes;
# without bundlor that file never exists, so let the jar plugin write its default one.
manifest_ref = "<manifestFile>${manifest.file}</manifestFile>"
if manifest_ref not in pom:
    sys.exit("expected %s in the parent pom" % manifest_ref)
pom = re.sub(r"[ \t]*" + re.escape(manifest_ref) + r"[ \t]*\n", "", pom)

with open(dst, "w", encoding="utf-8") as f:
    f.write(pom)
print("removed %d bundlor plugin block(s) -> %s" % (removed, dst))
