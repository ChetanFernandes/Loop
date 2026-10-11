# Pytest file (suggested path: tests/test_notebook_functions.py)
# This test file loads the Jupyter notebook at the repo root and executes its code
# cells into a temporary namespace, skipping interactive cells. It asserts the
# presence and behavior of a couple of public functions observed in the notebook
# (reverse, vowels_check). Adjust the notebook filename/path if necessary.

import os
import nbformat

# Tokens that make cells interactive or unsafe to execute in CI; such cells are skipped
SKIP_TOKENS = (
    'input(',
    'getpass',
    'ipywidgets',
    'from ipywidgets',
    'interact(',
    '%',
    '%%',
)


def _load_notebook_namespace(nb_path):
    """Read notebook at nb_path and execute its code cells into a fresh dict.

    - Skips non-code cells.
    - Skips cells containing any pattern in SKIP_TOKENS.
    - Ignores exceptions raised when executing a cell (continues to next cell).

    Returns the resulting globals dict.
    """
    nb = nbformat.read(nb_path, as_version=4)
    ns = {}
    for cell in nb.cells:
        if cell.cell_type != 'code':
            continue
        src = cell.source
        # simple heuristic: skip cell if it contains any skip token
        if any(tok in src for tok in SKIP_TOKENS):
            continue
        try:
            exec(src, ns)
        except Exception:
            # do not fail here; many notebook cells are demonstration prints
            continue
    return ns


def _notebook_path():
    # Notebook is expected at repository root next to tests/ when tests run
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    nb_name = '06_oct_Loop assignemnet.ipynb'
    return os.path.join(repo_root, nb_name)


def test_notebook_exists():
    nb_path = _notebook_path()
    assert os.path.exists(nb_path), f'Notebook not found at expected path: {nb_path}'


def test_reverse_function():
    nb_path = _notebook_path()
    ns = _load_notebook_namespace(nb_path)
    assert 'reverse' in ns, 'Expected function "reverse" not found in notebook namespace'
    assert ns['reverse']('PrepBytes') == 'setyBperP'


def test_vowels_check_function():
    nb_path = _notebook_path()
    ns = _load_notebook_namespace(nb_path)
    # Notebook appears to include a "vowels_check" implementation. If absent,
    # this test will fail and should be adjusted to match the actual function name.
    assert 'vowels_check' in ns, 'Expected function "vowels_check" not found in notebook namespace'
    assert ns['vowels_check']('guava') is True
    assert ns['vowels_check']('kiwi') is False
