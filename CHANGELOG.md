Last Updated: 2026-04-22T14:59:20Z

# Changelog

<a name="v1.4.1a0"></a>
## [v1.4.1a0](https://github.com/carlkidcrypto/purpleair_api/compare/v1.4.0...v1.4.1a0) (2026-04-22)

### Changes

#### Bug Fixes
- fix: remove spurious modified_since key in request_sensor_historic_data; add coverage tests (#216)
- Fix: Upgrade agentic workflows from gh-aw v0.67.4 to v0.68.1 (#209)
- fix: add network/tools config to docs continuous improvement agentic workflow (#207)
- fix: use README.rst for PyPI long description (#201)

#### Documentation Updates
- docs: fix typos, grammar, and misleading docstrings (#214)

#### Maintenance
- Bump version to 1.4.1a0 and add PurpleAir API watcher workflow (#218)
- chore: add agentic workflow md files adapted for purpleair_api (#202)
- Bump coverage from 7.13.4 to 7.13.5 (#200)
- Bump black from 26.1.0 to 26.3.1 (#198)

#### Other Changes
- [coverage-autofix] Add missing test coverage for uncovered branches (#217)
- [docs-improvement] Fix typos, stale config, and misleading docstrings (#215)
- [coverage-autofix] Bring PurpleAirAPIHelpers to 100% line coverage (#206)
- Compile agentic workflow markdown files to GitHub Actions YAML (gh-aw) (#203)
- Update Buy Me a Coffee username in FUNDING.yml (#199)

---

<a name="v1.4.0"></a>
## [v1.4.0](https://github.com/carlkidcrypto/purpleair_api/compare/v1.4.0a1...v1.4.0) (2026-03-01)

### Changes

#### Bug Fixes
- Fix CI test dependency pinning to resolve macOS/Windows requests_mock failures (#195)
- Fix trusted publishing by adding environment to PyPI workflows (#178)

#### Maintenance
- Prepare stable 1.4.0 release: version bump and docs update (#194)
- Bump version to 1.4.0.a2 and expand package keywords (#193)
- Bump coverage from 7.13.2 to 7.13.4 (#191)
- Bump coverage from 7.13.1 to 7.13.2 (#189)
- Bump black from 25.12.0 to 26.1.0 (#188)
- Bump furo from 2025.9.25 to 2025.12.19 (#187)
- Bump black from 25.11.0 to 25.12.0 (#181)
- Bump furo from 2025.9.25 to 2025.12.19 (#183)
- Bump coverage from 7.12.0 to 7.13.1 (#184)
- Bump sphinx from 9.0.0 to 9.1.0 (#185)

---

<a name="v1.4.0a1"></a>
## [v1.4.0a1](https://github.com/carlkidcrypto/purpleair_api/compare/v1.3.1...v1.4.0a1) (2025-12-01)

### Changes

#### Features
- Feature/agents (#168)

#### Bug Fixes
- Fix PyPI trusted publishing workflow (#176)

#### Maintenance
- Bump sphinx from 8.2.3 to 9.0.0 (#177)
- Bump coverage from 7.11.0 to 7.12.0 (#162)
- Bump black from 25.9.0 to 25.11.0 (#160)
- Update To Support PurpleAir API v1.2.0 and Bump Version to 1.4.0.a1 (#171)

#### Other Changes
- Update templates and AI usage guide for purpleair_api
- Drop Python 3.9 support, add Python 3.14 support (#169)
- Copilot/update workflow security (#167)
- Implement hash-based SHA pinning for GitHub Actions (#166)
- Enhance documentation with comprehensive README.rst files and improved Sphinx content (#165)
- Achieve 99% test coverage and improve test quality (#164)
- Add agent role documentation for workflows, docs, and tests (#163)

---

<a name="v1.3.1"></a>
## [v1.3.1](https://github.com/carlkidcrypto/purpleair_api/compare/v1.3.0...v1.3.1) (2025-10-28)

### Changes

#### Maintenance
- Bump coverage from 7.10.7 to 7.11.0 (#147)
- Bump black from 25.1.0 to 25.9.0 (#145)
- Bump coverage from 7.10.1 to 7.10.7 (#146)
- Bump coverage from 7.8.0 to 7.10.1 (#139)
- Bump coverage from 7.6.12 to 7.8.0 (#132)
- Bump sphinx from 8.2.0 to 8.2.3 (#129)
- Bump coverage from 7.6.10 to 7.6.12 (#126)
- Bump black from 24.10.0 to 25.1.0 (#124)
- Bump sphinx from 8.1.3 to 8.2.0 (#127)

#### Other Changes
- PyPi Workflows (#157)
- Hotfix/test py pi workflow (#156)
- V1.3.1 (#155)
- Potential fix for code scanning alert no. 10: Clear-text logging of sensitive information (#154)
- Potential fix for code scanning alert no. 8: Workflow does not contain permissions (#153)
- Potential fix for code scanning alert no. 4: Workflow does not contain permissions (#152)
- Potential fix for code scanning alert no. 3: Workflow does not contain permissions (#151)
- Potential fix for code scanning alert no. 2: Workflow does not contain permissions (#150)
- Update sphinx_build.yml (#149)
- Update changed-files action to version 46.0.1 (#148)

---

<a name="v1.3.0"></a>
## [v1.3.0](https://github.com/carlkidcrypto/purpleair_api/compare/v1.2.0...v1.3.0) (2025-01-08)

### Changes

#### Features
- Feature/py versions (#122)

#### Maintenance
- Bump coverage from 7.6.9 to 7.6.10 (#121)
- Bump coverage from 7.6.7 to 7.6.9 (#119)
- Bump tj-actions/changed-files from 45.0.4 to 45.0.5 (#120)
- Bump coverage from 7.6.4 to 7.6.7 (#117)
- Bump codecov/codecov-action from 4 to 5 (#115)
- Bump sphinx-rtd-theme from 3.0.1 to 3.0.2 (#114)
- Bump tj-actions/changed-files from 45.0.3 to 45.0.4 (#113)
- Bump sphinx from 8.0.2 to 8.1.3 (#111)
- Bump coverage from 7.6.2 to 7.6.4 (#112)
- Bump coverage from 7.6.1 to 7.6.2 (#107)
- Bump psf/black from 24.8.0 to 24.10.0 (#106)
- Bump black from 24.8.0 to 24.10.0 (#105)
- Bump carlkidcrypto/os-specific-runner from 2.1.0 to 2.1.1 (#101)
- Bump sphinx-rtd-theme from 3.0.0 to 3.0.1 (#108)
- Bump sphinx-rtd-theme from 3.0.0rc4 to 3.0.0 (#104)
- Bump tj-actions/changed-files from 45.0.2 to 45.0.3 (#103)
- Bump sphinx-rtd-theme from 3.0.0rc3 to 3.0.0rc4 (#102)

---

<a name="v1.2.0"></a>
## [v1.2.0](https://github.com/carlkidcrypto/purpleair_api/compare/v1.2.0a2...v1.2.0) (2024-09-26)

### Changes

#### Maintenance
- Bump sphinx-rtd-theme from 3.0.0rc2 to 3.0.0rc3 (#99)

#### Other Changes
- Prep for 1.2.0 (#100)

---

<a name="v1.2.0a2"></a>
## [v1.2.0a2](https://github.com/carlkidcrypto/purpleair_api/compare/v1.2.0a1...v1.2.0a2) (2024-09-24)

### Changes

#### Maintenance
- Bump sphinx-rtd-theme from 3.0.0rc1 to 3.0.0rc2 (#97)

#### Tests
- test pypi workflow (#96)

#### Other Changes
- Error code 402 (#98)

---

<a name="v1.2.0a1"></a>
## [v1.2.0a1](https://github.com/carlkidcrypto/purpleair_api/compare/v1.1.4...v1.2.0a1) (2024-09-19)

### Changes

#### Maintenance
- Bump tj-actions/changed-files from 45.0.1 to 45.0.2 (#94)
- Bump tj-actions/changed-files from 45.0.0 to 45.0.1 (#93)
- Bump tj-actions/changed-files from 44.5.7 to 45.0.0 (#92)
- Bump sphinx from 7.4.7 to 8.0.2 (#88)
- Bump psf/black from 24.4.2 to 24.8.0 (#90)
- Bump coverage from 7.6.0 to 7.6.1 (#91)
- Bump tj-actions/changed-files from 44.5.6 to 44.5.7 (#89)
- Bump sphinx from 7.4.6 to 7.4.7 (#87)
- Bump tj-actions/changed-files from 44.5.5 to 44.5.6 (#86)
- Bump sphinx from 7.4.4 to 7.4.6 (#85)
- Bump coverage from 7.5.4 to 7.6.0 (#81)
- Bump sphinx from 7.3.7 to 7.4.4 (#83)
- Bump tj-actions/changed-files from 44.5.4 to 44.5.5 (#80)
- Bump tj-actions/changed-files from 44.5.1 to 44.5.4 (#78)
- Bump coverage from 7.5.3 to 7.5.4 (#79)
- Bump coverage from 7.5.1 to 7.5.3 (#74)
- Bump tj-actions/changed-files from 44.5.0 to 44.5.1 (#72)
- Bump tj-actions/changed-files from 44.3.0 to 44.4.0 (#70)
- Bump coverage from 7.5.0 to 7.5.1 (#68)
- Bump carlkidcrypto/os-specific-runner from 2.0.0 to 2.1.0 (#69)
- Bump coverage from 7.4.4 to 7.5.0 (#65)
- Bump psf/black from 24.4.0 to 24.4.2 (#67)
- Bump tj-actions/changed-files from 44.1.0 to 44.3.0 (#64)
- Bump sphinx from 7.3.6 to 7.3.7 (#63)
- Bump tj-actions/changed-files from 44.0.1 to 44.1.0 (#62)
- Bump sphinx from 7.3.5 to 7.3.6 (#61)
- Bump sphinx from 7.2.6 to 7.3.5 (#60)
- Bump psf/black from 24.3.0 to 24.4.0 (#59)
- Bump tj-actions/changed-files from 44.0.0 to 44.0.1 (#58)
- Bump requests-mock from 1.11.0 to 1.12.1 (#57)
- Bump tj-actions/changed-files from 43.0.1 to 44.0.0 (#55)
- Bump psf/black from 24.2.0 to 24.3.0 (#53)
- Bump tj-actions/changed-files from 43.0.0 to 43.0.1 (#54)
- Bump coverage from 7.4.3 to 7.4.4 (#52)
- Bump tj-actions/changed-files from 42.1.0 to 43.0.0 (#51)
- Bump tj-actions/changed-files from 42.0.7 to 42.1.0 (#50)
- Bump tj-actions/changed-files from 42.0.6 to 42.0.7 (#49)
- Bump tj-actions/changed-files from 42.0.5 to 42.0.6 (#48)
- Bump tj-actions/changed-files from 42.0.4 to 42.0.5 (#46)
- Bump coverage from 7.4.2 to 7.4.3 (#47)

#### Other Changes
- 75 add new api endpoints (#95)
- --- (#71)

---

<a name="v1.1.4"></a>
## [v1.1.4](https://github.com/carlkidcrypto/purpleair_api/compare/v1.1.3...v1.1.4) (2024-02-21)

### Changes

#### Maintenance
- Bump (#45)
- Bump coverage from 7.4.1 to 7.4.2 (#44)
- Bump tj-actions/changed-files from 42.0.2 to 42.0.4 (#43)
- Bump psf/black from 24.1.1 to 24.2.0 (#42)
- Bump codecov/codecov-action from 3 to 4 (#41)
- Bump tj-actions/changed-files from 42.0.0 to 42.0.2 (#37)
- Bump coverage from 7.4.0 to 7.4.1 (#39)
- Bump psf/black from 23.12.1 to 24.1.1 (#40)
- Bump tj-actions/changed-files from 41.0.1 to 42.0.0 (#35)

---

<a name="v1.1.3"></a>
## [v1.1.3](https://github.com/carlkidcrypto/purpleair_api/compare/v1.1.2...v1.1.3) (2024-01-04)

### Changes

#### Maintenance
- Bump coverage from 7.3.4 to 7.4.0 (#31)
- Bump psf/black from 23.12.0 to 23.12.1 (#30)
- Bump coverage from 7.3.3 to 7.3.4 (#29)
- Bump coverage from 7.3.2 to 7.3.3 (#27)
- Bump psf/black from 23.11.0 to 23.12.0 (#26)
- Bump actions/setup-python from 4 to 5 (#25)

#### Other Changes
- Release/v1.1.3 (#32)
- Update README.md
- Update tests.yml (#28)
- Workflows
- YML & Reqs

---

<a name="v1.1.2"></a>
## [v1.1.2](https://github.com/carlkidcrypto/purpleair_api/compare/v1.1.1...v1.1.2) (2023-11-11)

### Changes

#### Features
- Feature/minor improvements to use helpers (#24)

#### Maintenance
- Bump psf/black from 23.10.1 to 23.11.0 (#23)
- Bump psf/black from 23.10.0 to 23.10.1 (#22)
- Bump psf/black from 23.9.1 to 23.10.0 (#21)

---

<a name="v1.1.1"></a>
## [v1.1.1](https://github.com/carlkidcrypto/purpleair_api/compare/v1.1.1.a0...v1.1.1) (2023-09-22)

### Changes

#### Features
- Feature/wrap up 1.1.1 release (#20)

#### Other Changes
- Update README.md

---

<a name="v1.1.1.a0"></a>
## [v1.1.1.a0](https://github.com/carlkidcrypto/purpleair_api/compare/v1.1.0...v1.1.1.a0) (2023-09-19)

### Changes

#### Features
- Feature/multiple local network sensors  (#19)

---

<a name="v1.1.0"></a>
## [v1.1.0](https://github.com/carlkidcrypto/purpleair_api/compare/v1.1.0a1...v1.1.0) (2023-09-13)

### Changes

#### Features
- Feature/work more on tests workflow (#17)
- Feature/10 unit tests (#16)

#### Maintenance
- Bump actions/checkout from 3 to 4 (#14)
- Bump psf/black from 23.7.0 to 23.9.1 (#15)
- Bump psf/black from 23.3.0 to 23.7.0 (#13)

#### Other Changes
- 12 update readme for v110 (#18)

---

<a name="v1.1.0a1"></a>
## [v1.1.0a1](https://github.com/carlkidcrypto/purpleair_api/compare/v1.0.2...v1.1.0a1) (2023-06-25)

### Changes

#### Features
- Feature/9 local paa requests (#11)

---

<a name="v1.0.2"></a>
## [v1.0.2](https://github.com/carlkidcrypto/purpleair_api/compare/v1.0.2a1...v1.0.2) (2023-06-13)

### Changes

#### Other Changes
- V1.0.2 (#8)

---

<a name="v1.0.2a1"></a>
## [v1.0.2a1](https://github.com/carlkidcrypto/purpleair_api/compare/v1.0.1...v1.0.2a1) (2023-05-17)

### Changes

#### Maintenance
- Bump psf/black from 23.1.0 to 23.3.0 (#6)

#### Other Changes
- Bugfix/reducing down mem foot print (#7)
- carlkid1499 --> to carlkidcrypto
- Update README.md

---

<a name="v1.0.1"></a>
## [v1.0.1](https://github.com/carlkidcrypto/purpleair_api/compare/v1.0.1a2...v1.0.1) (2023-02-23)

### Changes

#### Other Changes
- Update PurpleAirAPI.py
- Prep Work For V1.0.1

---

<a name="v1.0.1a2"></a>
## [v1.0.1a2](https://github.com/carlkidcrypto/purpleair_api/compare/v1.0.1a1...v1.0.1a2) (2023-02-21)

### Changes

#### Other Changes
- Encode UTF-8

---

<a name="v1.0.1a1"></a>
## [v1.0.1a1](https://github.com/carlkidcrypto/purpleair_api/compare/v1.0.1a0...v1.0.1a1) (2023-02-21)

### Changes

#### Other Changes
- Update PurpleAirAPI.py
- v1.0.1a1

---

<a name="v1.0.1a0"></a>
## [v1.0.1a0](https://github.com/carlkidcrypto/purpleair_api/compare/v1.0.0...v1.0.1a0) (2023-02-19)

### Changes

#### Other Changes
- Bugfix/fixing bugs for new data loggers feature (#5)

---

<a name="v1.0.0"></a>
## [v1.0.0](https://github.com/carlkidcrypto/purpleair_api/compare/v1.0.0a2...v1.0.0) (2023-02-18)

### Changes

#### Features
- Feature/prep for v1.0.0 release (#4)

---

<a name="v1.0.0a2"></a>
## v1.0.0a2 (2023-02-15)

### Changes

#### Features
- Feature/docs docs docs (#3)
- Feature/move latest code over (#2)

#### Other Changes
- Merge pull request #1 from carlkid1499/feature/move_purpleair_api_from_purpleair_data_logger
- Black
- More Prep Work
- Prep Work
- Cleanup and Docs
- Rename
- Initial Move
- Initial commit

---
