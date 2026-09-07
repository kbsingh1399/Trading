# -*- coding: utf-8 -*-
import re, pathlib

src = pathlib.Path(r'Engine\strategy\run_18_asset_parallel_oos.py')
txt = src.read_bytes().decode('utf-8', errors='replace')
# Replace the broken bar line with ASCII
txt = re.sub(r"bar = .*int\(pr / 10\).*\n", "bar = \"#\" * int(pr / 10) + \".\" * (10 - int(pr / 10))\n", txt)
src.write_text(txt, encoding='utf-8')
print('Done')
