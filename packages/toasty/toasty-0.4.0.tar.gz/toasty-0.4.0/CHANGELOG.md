# toasty 0.4.0 (2020-10-05)

- In WTML outputs, omit the <Place> wrapper for all-sky data sets
- When using `tile-allsky` in `plate-carree-planet` mode, use the "Planet" data
  set type
- Add `--name` options to `tile-allsky` and `tile-study`

# toasty 0.3.3 (2020-09-29)

- Make sure to close WWTL files after reading them in. May fix the test suite
  on some Windows machines.

# toasty 0.3.2 (2020-09-29)

- Switch to Cranko for versioning and release management, and Azure Pipelines
  for CI/CD, and Codecov.io for coverage monitoring.
- Fix tests on Windows, where there is no `healpy`

# 0.3.1 (2020 Sep 21)

- If PIL is missing colorspace support, don't crash with an error, but provide a
  big warning.
- Add a `plate-carree-galactic` projection type, for equirectangular images in
  Galactic coordinates.
- In the plate carrée image samplers, round nearest-neighbor pixel coordinates
  rather than truncating the fractional component. This should fix a half-pixel
  offset in TOASTed maps.
- Remove some old functionalities that are currently going unused, and not
  expected to become needed in the future.

# 0.3.0 (2020 Sep 18)

- Attempt to properly categorize Cython as a build-time-only dependency. We don't
  need it at runtime.

# 0.2.0 (2020 Sep 17)

- Add a first cut at support for OpenEXR images. This may evolve since it might
  be valuable to take more advantage of OpenEXR's support for high-dynamic-range
  imagery.
- Add cool progress reporting for tiling and cascading!
- Fix installation on Windows (hopefully).
- Add a new `make-thumbnail` utility command.
- Add `--placeholder-thumbnail` to some tiling commands to avoid the thumbnailing
  step, which can be very slow and memory-intensive for huge input images.
- Internal cleanups.

# 0.1.0 (2020 Sep 15)

- Massive rebuild of just about everything about the package.
- New CLI tool, `toasty`.

# 0.0.3 (2019 Aug 3)

- Attempt to fix ReadTheDocs build.
- Better metadata for PyPI.
- Exercise workflow documented in `RELEASE_PROCESS.md`.

# 0.0.2 (2019 Aug 3)

- Revamp packaging infrastructure
- Stub out some docs
- Include changes contributed by Clara Brasseur / STScI
