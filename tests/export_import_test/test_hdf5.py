"""Test output to and import from hdf5."""

import io_test
import os
import pickle
import pytest
import warnings
import tempfile
from tenpy.tools import io
import numpy as np

datadir_hdf5 = [f for f in io_test.datadir_files if f.endswith('.hdf5')]

try:
    import h5py
except ImportError:
    h5py = None


def export_to_datadir():
    filename = io_test.get_datadir_filename("exported_from_tenpy_{0}.hdf5")
    data = io_test.gen_example_data()
    f = h5py.File(filename, 'w')
    io.dump_to_hdf5(f, data)


@pytest.mark.skipif(h5py is None, reason="h5py not available")
def test_hdf5_export_import():
    """Try subsequent export and import to pickle."""
    data = io_test.gen_example_data()
    with tempfile.TemporaryFile() as tf:
        with h5py.File(tf, 'w') as f:
            io.dump_to_hdf5(f, data)
        tf.seek(0)  # reset pointer to beginning of file for reading
        with h5py.File(tf, 'r') as f:
            data_imported = io.load_from_hdf5(f)
    io_test.assert_equal_data(data_imported, data)


@pytest.mark.skipif(h5py is None, reason="h5py not available")
@pytest.mark.parametrize('fn', datadir_hdf5)
def test_import_from_datadir(fn):
    print("import ", fn)
    filename = os.path.join(io_test.datadir, fn)
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=FutureWarning)
        with h5py.File(filename, 'r') as f:
            data = io.load_from_hdf5(f)
    if 'version' in data:
        data_expected = io_test.gen_example_data(data['version'])
    else:
        data_expected = io_test.gen_example_data('0.4.0')
    io_test.assert_equal_data(data, data_expected)


if __name__ == "__main__":
    export_to_datadir()