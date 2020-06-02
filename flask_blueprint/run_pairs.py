import os, sys, pathlib
import argparse

from apps.settings.settings_pairs import *
from apps.app_quant.pairs import *

# ==============================================================================


# ==============================================================================

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', action="store", dest="p", nargs=1, default=[PORT])
    parser.add_argument('-d', action="store", dest="d", nargs=1, default=[DEBUG_PLOT])
    args = parser.parse_args()

    port = int(args.p[0])
    debug_plot = int(args.d[0])

    # app.run(host='0.0.0.0', port=80)
    app.run_server(debug=debug_plot, port=port)
