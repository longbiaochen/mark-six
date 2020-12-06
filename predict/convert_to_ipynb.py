from nbformat import v3, v4
import sys
import os
infilename = sys.argv[1]
outfilename = os.path.splitext(infilename)[0] + ".ipynb"
with open(infilename) as fpin:
    text = fpin.read()

text = text.replace("#%%", "# <codecell>")
text = text.replace("# %%", "# <codecell>")
text = text.replace("#<codecell>", "# <codecell>")

import re
text = re.sub(r'(# <codecell>)(.*)(\n)',
              r'# <markdowncell>\n# #### \2\n# <codecell>\n', text)

nbook = v3.reads_py(text)
nbook = v4.upgrade(nbook)
jsonform = v4.writes(nbook) + "\n"
with open(outfilename, "w") as fpout:
    fpout.write(jsonform)
