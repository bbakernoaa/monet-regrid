# monet-regrid Release Checklist v0.5.0

## Pre-Release Validation
- [x] All tests pass (`pytest tests/`)
- [x] Package builds successfully (`python -m build`)
- [x] Distribution files pass twine check (`twine check dist/*`)
- [x] Package installs correctly (`pip install -e .`)
- [x] Import and basic functionality verified

## Documentation Updates
- [x] CHANGELOG.md updated with release notes
- [x] CITATION.cff updated for new package name
- [x] All references updated from xarray-regrid to monet-regrid
- [x] License notices updated across all files

## Code Quality
- [x] All source files have Apache 2.0 license headers
- [x] Proper modification notices for derivative work
- [x] Code style compliance maintained
- [x] No remaining old package references

## Release Preparation
- [x] Version updated to 0.5.0 in package
- [x] All classifiers in pyproject.toml verified
- [x] README and documentation reflect new branding
- [x] Environment files updated with new package name

## Git Operations
1. Commit all changes:
   ```bash
   git add .
   git commit -m "chore: finalize monet-regrid v0.5.0 release"
   ```

2. Tag the release:
   ```bash
   git tag -a v0.5.0 -m "Release monet-regrid v0.5.0 - Full rebranding and curvilinear support"
   ```

3. Push changes and tags:
   ```bash
   git push origin main
   git push origin v0.5.0
   ```

## PyPI Release
1. Upload to TestPyPI first:
   ```bash
   twine upload --repository testpypi dist/*
   ```

2. Verify on TestPyPI: https://test.pypi.org/project/monet-regrid/

3. Upload to PyPI:
   ```bash
   twine upload dist/*
   ```

## Post-Release
- [ ] Verify package available on PyPI: https://pypi.org/project/monet-regrid/
- [ ] Verify documentation builds correctly
- [ ] Update Zenodo record if needed
- [ ] Announce release in relevant channels
- [ ] Verify installation works from PyPI: `pip install monet-regrid`

## Repository Cleanup
- [ ] Close relevant issues and pull requests
- [ ] Update any project boards or tracking systems
- [ ] Prepare next development iteration if applicable