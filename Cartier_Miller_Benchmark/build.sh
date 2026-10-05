#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-2.0-or-later
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p bin
g++ -O3 -std=c++17 -pthread \
  harvey_adapter.cpp upstream/recurrences_ntl.cpp upstream/hypellfrob.cpp \
  -lntl -lgmp -o bin/harvey_adapter
python3 - <<'PY'
import datetime,json,subprocess
from pathlib import Path
record={'compiler_version':subprocess.check_output(['g++','--version'],text=True),
        'compiler_command':'g++ -O3 -std=c++17 -pthread harvey_adapter.cpp upstream/recurrences_ntl.cpp upstream/hypellfrob.cpp -lntl -lgmp -o bin/harvey_adapter',
        'utc_built':datetime.datetime.now(datetime.timezone.utc).isoformat()}
Path('bin/build_metadata.json').write_text(json.dumps(record,indent=2))
PY
