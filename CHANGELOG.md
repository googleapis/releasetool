# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/gcp-releasetool/#history

## 0.9.0

10-05-2018 09:09 PDT

### Implementation Changes
- Move edit_release_notes to common ([#58](https://github.com/GoogleCloudPlatform/releasetool/pull/58))

### New Features
- Default to yes for opening build page, copy commitish to clipboard ([#64](https://github.com/GoogleCloudPlatform/releasetool/pull/64))
- Add release dates to changelog ([#57](https://github.com/GoogleCloudPlatform/releasetool/pull/57))

### Dependencies
- Require python>=3.6 ([#71](https://github.com/GoogleCloudPlatform/releasetool/pull/71))

### Internal / Testing Changes
- Fix Ruby start ([#63](https://github.com/GoogleCloudPlatform/releasetool/pull/63))
- Fix failing tests ([#61](https://github.com/GoogleCloudPlatform/releasetool/pull/61))
- Set up CI ([#60](https://github.com/GoogleCloudPlatform/releasetool/pull/60))
- Use new Nox ([#59](https://github.com/GoogleCloudPlatform/releasetool/pull/59))

## 0.8.0

### Implementation Changes
- make release.sh executable ([#50](https://github.com/GoogleCloudPlatform/releasetool/pull/50))

### New Features
- Add link to Kokoro release job for python tools ([#55](https://github.com/GoogleCloudPlatform/releasetool/pull/55))

### Documentation
- Update instructions to be more clear ([#51](https://github.com/GoogleCloudPlatform/releasetool/pull/51))

## 0.7.0

### Implementation Changes
- fix: `tag` detects default language ([#45](https://github.com/GoogleCloudPlatform/releasetool/pull/45))
- fix: nodejs tag ([#44](https://github.com/GoogleCloudPlatform/releasetool/pull/44))

### New Features
- Add --version flag ([#47](https://github.com/GoogleCloudPlatform/releasetool/pull/47))

### Internal / Testing Changes
- add .kokoro release job ([#48](https://github.com/GoogleCloudPlatform/releasetool/pull/48))

## 0.6.0

### Implementation Changes
- Fix error on missing ~/.cache
- fix(nodejs): tag name is just the version for Node.js ([#42](https://github.com/GoogleCloudPlatform/releasetool/pull/42))
- Fix release name, tag, and release notes ([#34](https://github.com/GoogleCloudPlatform/releasetool/pull/34))

### New Features
- feat(nodejs): bump package version in samples/package.json as well ([#41](https://github.com/GoogleCloudPlatform/releasetool/pull/41))
- Add support for google-cloud-ruby libraries ([#37](https://github.com/GoogleCloudPlatform/releasetool/pull/37))
- Add links to pull requests ([#39](https://github.com/GoogleCloudPlatform/releasetool/pull/39))

### Dependencies
- Fix missing packaging dependency

### Internal / Testing Changes
- Blacken

## 0.5.0

### New Features

- Add java start and tag commands (#29)

## 0.4.0

### Implementation Changes

- Correctly handle multiple possible upstreams and correctly compute the upstream change summary (#30)

### New Features

- Automatically detect the language. (#31)

## 0.3.0

### New Features

- Check for updates (#24)
- Add support for multiple GitHub remotes and releasing across forks (#22)

### Internal / Testing Changes

- Use new Nox
- Blacken and fixup type issues (#23)

## 0.2.1

### Implementation Changes

- Adjust tagging logic for Node (#15)
- Fix Node CHANGELOG.md npm packages link (#17)

## 0.2.0

- Customize start for Node.js (#6)
- Better editor support
- Duplicate Python logic for Node.js (#5)

## 0.1.0

Initial release

