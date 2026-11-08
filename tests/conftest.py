import os
import tempfile

# Isolate the app's data directory before any project module is imported.
os.environ.setdefault('PEABOX_DATA_DIR', tempfile.mkdtemp(prefix='peabox_test_'))
