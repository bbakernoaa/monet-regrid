# SPARC Rebranding Workflow: xarray-regrid → monet-regrid

## 1. LICENSE COMPLIANCE ANALYSIS

### Apache 2.0 License Requirements (from LICENSE)
- **✅ Allowed**: Create Derivative Works with modifications
- **✅ Required**: Retain all copyright, patent, trademark, and attribution notices from Source form
- **✅ Required**: Include NOTICE file contents (if present) in Derivative Works
- **⚠️  Required**: Prominent notices stating that files were changed
- **⚠️  Required**: Give recipients a copy of Apache License 2.0
- **❌ Forbidden**: Use licensor's trademarks for endorsement without permission

### Key Compliance Points for Rebranding
1. **Preserve existing copyright headers** in all source files
2. **Add modification notice** to changed files
3. **Keep Apache 2.0 license** - cannot change license
4. **Maintain attribution** to original authors in CITATION.cff
5. **Cannot use "xarray" trademark** for endorsement

---

## 2. INVENTORY OF ALL REFERENCES

### Package Structure References
- `src/xarray_regrid/` - Main package directory
- All `from xarray_regrid.*` imports (276+ occurrences)
- `xarray_regrid` in test imports
- Package references in documentation

### Configuration Files
- `pyproject.toml` - Project name, URLs, version path
- `CITATION.cff` - Package title and repository
- `CHANGELOG.md` - Historical references
- `environment.yml` - Conda environment name

### Documentation References
- `README.md` - Multiple references in badges, usage, installation
- `docs/` directory - Sphinx config, RST files, notebooks
- `docs/assets/` - Logo files
- All notebook files with `import xarray_regrid`

### Build/Testing References
- `pyproject.toml` - Coverage paths, isort configuration
- Test files - Import statements and usage examples
- Benchmark files - Import and usage patterns

---

## 3. PYPROJECT.TOML UPDATES

### Required Changes
```toml
[project]
name = "monet-regrid"
description = 'Regridding tools using xarray and flox.'  # Keep original description

[project.urls]
Documentation = "https://github.com/EXCITED-CO2/monet-regrid#readme"
Issues = "https://github.com/EXCITED-CO2/monet-regrid/issues" 
Source = "https://github.com/EXCITED-CO2/monet-regrid"

[tool.hatch.version]
path = "src/monet_regrid/__init__.py"  # Update path

[tool.ruff.lint.isort]
known-first-party = ["monet_regrid"]  # Update package name

[tool.coverage.run]
source_pkgs = ["monet_regrid", "tests"]  # Update package name

[tool.coverage.paths]
monet_regrid = ["monet_regrid", "*/monet_regrid/monet_regrid"]  # Update paths
```

### Version Strategy
- **Keep semantic versioning** (start with 0.5.0 for rebranded version)
- **Maintain version detection** via `__init__.py` path update
- **Preserve all dependencies** - no changes needed

---

## 4. SOURCE PACKAGE RENAME STEPS

### 4.1 Directory Rename
```bash
# Step 1: Rename directory
mv src/xarray_regrid src/monet_regrid
```

### 4.2 Internal Import Updates (Pseudocode)
```python
MODULES_TO_UPDATE = [
    "src/monet_regrid/__init__.py",
    "src/monet_regrid/core.py", 
    "src/monet_regrid/regrid.py",
    "src/monet_regrid/methods/*.py",
    "src/monet_regrid/curvilinear.py",
    "src/monet_regrid/utils.py",
    "src/monet_regrid/constants.py",
    "src/monet_regrid/interpolation_engine.py"
]

def update_internal_imports():
    """Update all internal xarray_regrid imports to monet_regrid"""
    for module in MODULES_TO_UPDATE:
        content = read_file(module)
        # Replace internal imports only
        content = content.replace(
            "from xarray_regrid.", 
            "from monet_regrid."
        )
        content = content.replace(
            "import xarray_regrid", 
            "import monet_regrid"
        )
        write_file(module, content)
```

### 4.3 Docstring and Comment Updates
```python
def update_docstrings_and_comments():
    """Update package references in docstrings and comments"""
    for module in MODULES_TO_UPDATE:
        content = read_file(module)
        # Update docstrings mentioning xarray-regrid
        content = content.replace(
            "xarray-regrid", 
            "monet-regrid"
        )
        content = content.replace(
            "xarray_regrid", 
            "monet_regrid"
        )
        write_file(module, content)
```

### 4.4 __init__.py Special Handling
```python
# src/monet_regrid/__init__.py
from monet_regrid import methods
from monet_regrid.regrid import Regridder  
from monet_regrid.utils import Grid, create_regridding_dataset
from monet_regrid.constants import GridType
from monet_regrid.core import BaseRegridder, RectilinearRegridder, CurvilinearRegridder

__all__ = [
    "Grid",
    "Regridder", 
    "BaseRegridder",
    "RectilinearRegridder",
    "CurvilinearRegridder",
    "create_regridding_dataset",
    "GridType",
    "methods",
]

__version__ = "0.5.0"  # Update version
```

---

## 5. DOCUMENTATION AND README UPDATES

### 5.1 README.md Changes
```markdown
# monet-regrid: Regridding utilities for xarray.

[![PyPI](https://img.shields.io/pypi/v/monet-regrid.svg?style=flat)](https://pypi.python.org/pypi/monet-regrid/)

## Installation
pip install monet-regrid

## Usage  
import monet_regrid

ds.regrid.linear(ds_grid)
```

### 5.2 Documentation Updates
```python
DOCS_FILES = [
    "docs/conf.py",
    "docs/index.rst", 
    "docs/getting_started.rst",
    "docs/index_update.md",
    "docs/getting_started_update.md",
    "docs/curvilinear_examples.md"
]

def update_documentation():
    """Update all documentation references"""
    for doc_file in DOCS_FILES:
        content = read_file(doc_file)
        content = content.replace("xarray-regrid", "monet-regrid")
        content = content.replace("xarray_regrid", "monet_regrid")
        write_file(doc_file, content)
```

### 5.3 Notebook Updates
```python
NOTEBOOKS = glob("docs/notebooks/**/*.ipynb")

def update_notebooks():
    """Update Jupyter notebook imports and references"""
    for notebook in NOTEBOOKS:
        content = read_json(notebook)
        # Update code cells
        for cell in content["cells"]:
            if cell["cell_type"] == "code":
                cell["source"] = cell["source"].replace(
                    "import xarray_regrid",
                    "import monet_regrid"
                )
        write_json(notebook, content)
```

---

## 6. TEST AND BUILD VALIDATION

### 6.1 Test Import Updates
```python
TEST_FILES = glob("tests/**/*.py")
BENCHMARK_FILES = glob("*optimization.py")

def update_test_imports():
    """Update all test file imports"""
    for test_file in TEST_FILES + BENCHMARK_FILES:
        content = read_file(test_file)
        content = content.replace(
            "from xarray_regrid", 
            "from monet_regrid"
        )
        content = content.replace(
            "import xarray_regrid",
            "import monet_regrid" 
        )
        write_file(test_file, content)
```

### 6.2 Validation Test Suite
```python
def validate_rebranding():
    """Comprehensive validation of rebranding changes"""
    
    # Test 1: Import validation
    try:
        import monet_regrid
        assert hasattr(monet_regrid, 'Grid')
        assert hasattr(monet_regrid, 'Regridder')
    except ImportError:
        raise AssertionError("Package import failed")
    
    # Test 2: Core functionality
    import xarray as xr
    import numpy as np
    
    # Create test data
    ds = xr.Dataset({
        'data': (['lat', 'lon'], np.random.rand(10, 20))
    }, coords={
        'lat': np.linspace(-90, 90, 10),
        'lon': np.linspace(-180, 180, 20)
    })
    
    # Test regridding works
    target_grid = monet_regrid.Grid(resolution_lat=10, resolution_lon=10)
    target_ds = monet_regrid.create_regridding_dataset(target_grid)
    
    result = ds.regrid.linear(target_ds)
    assert result is not None
    
    # Test 3: No remaining xarray_regrid references in source
    source_files = glob("src/monet_regrid/**/*.py")
    for file in source_files:
        content = read_file(file)
        assert "xarray_regrid" not in content, f"Found xarray_regrid in {file}"
    
    print("✅ All rebranding validation tests passed")
```

### 6.3 Build System Validation
```bash
# Test build system
python -m build  # Should create monet-regrid wheel
pip install dist/monet_regrid-*.whl
python -c "import monet_regrid; print('Success')"
pytest tests/  # All tests should pass
```

---

## 7. LICENSE-COMPLIANT NOTICES

### 7.1 Modification Notice Template
```python
# Add to top of modified files:
"""
This file is part of monet-regrid.

monet-regrid is a derivative work of xarray-regrid.
Original work Copyright (c) 2023-2025 Bart Schilperoort, Yang Liu.
This derivative work Copyright (c) 2025 [Your Organization].

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Modifications: Package renamed from xarray-regrid to monet-regrid,
URLs updated, and documentation adapted for new branding.
"""
```

### 7.2 Preserved Original Headers
- **Keep all existing copyright headers** in place
- **Do not modify** original author attribution
- **Maintain** Apache 2.0 license text
- **Add** modification notice below original header

### 7.3 CITATION.cff Updates
```yaml
# Update only the title and repository
title: monet-regrid
repository-code: 'https://github.com/EXCITED-CO2/monet-regrid'

# Keep all original authors and attribution
authors:
  - given-names: Bart
    family-names: Schilperoort
    email: b.schilperoort@esciencecenter.nl
    # ... rest unchanged

# Keep Apache-2.0 license
license: Apache-2.0
```

---

## 8. IMPLEMENTATION CHECKLIST

### Phase 1: Core Package Changes
- [ ] Rename `src/xarray_regrid/` → `src/monet_regrid/`
- [ ] Update all internal imports in source files
- [ ] Update docstrings and comments
- [ ] Update `__init__.py` exports and version
- [ ] Update `pyproject.toml` configuration
- [ ] Update `CITATION.cff` title and repository

### Phase 2: Documentation Updates  
- [ ] Update `README.md` badges and references
- [ ] Update `docs/conf.py` project name
- [ ] Update all RST documentation files
- [ ] Update Jupyter notebook imports
- [ ] Update benchmark notebook references

### Phase 3: Tests and Validation
- [ ] Update all test file imports
- [ ] Update benchmark script imports
- [ ] Run full test suite
- [ ] Validate package builds correctly
- [ ] Test installation from built wheel

### Phase 4: Compliance and Release
- [ ] Add modification notices to changed files
- [ ] Verify all original copyright headers preserved
- [ ] Update CHANGELOG.md with rebranding note
- [ ] Create release notes for 0.5.0
- [ ] Validate PyPI upload works

---

## 9. RISK MITIGATION

### High Risk Areas
1. **Import circularity** - Test all import paths
2. **Test suite breakage** - Run comprehensive tests
3. **Build system** - Verify wheel creation and installation
4. **Documentation links** - Update all internal references

### Validation Strategy
1. **Automated testing** - Full pytest suite
2. **Import testing** - Verify all modules import correctly  
3. **Integration testing** - Test end-to-end regridding workflows
4. **Build validation** - Test wheel creation and installation

### Rollback Plan
- Keep original repository as backup
- Git tags for each phase completion
- Ability to revert to original xarray-regrid if needed

---

## 10. SUCCESS CRITERIA

### Functional Requirements
- [ ] All tests pass with new package name
- [ ] Package installs and imports correctly
- [ ] All regridding methods work as before
- [ ] Documentation builds without errors
- [ ] No broken links or references

### Compliance Requirements  
- [ ] Apache 2.0 license fully preserved
- [ ] All original copyright headers intact
- [ ] Proper modification notices added
- [ ] Original authors properly attributed
- [ ] No trademark violations

### Quality Requirements
- [ ] No hard-coded secrets or config values
- [ ] All files under 500 lines where possible
- [ ] Modular, maintainable code structure
- [ ] Comprehensive documentation updates
- [ ] Clean git history with proper commits