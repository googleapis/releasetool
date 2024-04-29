# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/gcp-releasetool/#history

## [2.0.1](https://github.com/googleapis/releasetool/compare/v2.0.0...v2.0.1) (2024-04-29)


### Bug Fixes

* Release trigger URL for google-cloud-php ([#542](https://github.com/googleapis/releasetool/issues/542)) ([872bb0d](https://github.com/googleapis/releasetool/commit/872bb0ddf5900904251b5aabc79f7619c2111de1))
* Update fusion url to fusion2 ([#539](https://github.com/googleapis/releasetool/issues/539)) ([40688f9](https://github.com/googleapis/releasetool/commit/40688f914e0b06299fdb4f52eee5aad4bbec12b7))

## [2.0.0](https://github.com/googleapis/releasetool/compare/v1.17.0...v2.0.0) (2024-03-07)


### ⚠ BREAKING CHANGES

* Require cryptography 42.x.x

### Features

* Add support for python 3.12 ([18ad023](https://github.com/googleapis/releasetool/commit/18ad023ac61aca23419bec57253b76ee3057e9ff))


### Bug Fixes

* Add minimum requirements for gcp-releasetool ([18ad023](https://github.com/googleapis/releasetool/commit/18ad023ac61aca23419bec57253b76ee3057e9ff))
* Drop usage of `pkg_resources` ([18ad023](https://github.com/googleapis/releasetool/commit/18ad023ac61aca23419bec57253b76ee3057e9ff))
* Drop usage of `pkgutil` ([18ad023](https://github.com/googleapis/releasetool/commit/18ad023ac61aca23419bec57253b76ee3057e9ff))
* Require cryptography 42.x.x ([18ad023](https://github.com/googleapis/releasetool/commit/18ad023ac61aca23419bec57253b76ee3057e9ff))
* Require python 3.8+ ([18ad023](https://github.com/googleapis/releasetool/commit/18ad023ac61aca23419bec57253b76ee3057e9ff))
* Update dependencies in requirements.txt and requirements-dev.txt ([18ad023](https://github.com/googleapis/releasetool/commit/18ad023ac61aca23419bec57253b76ee3057e9ff))

## [1.17.0](https://github.com/googleapis/releasetool/compare/v1.16.0...v1.17.0) (2024-01-17)


### Features

* Add appengine-plugins to repo list ([#530](https://github.com/googleapis/releasetool/issues/530)) ([ae19e0e](https://github.com/googleapis/releasetool/commit/ae19e0e11d4d060599992b326af4a7ef21b7baf5))
* Update PHP tags ([#518](https://github.com/googleapis/releasetool/issues/518)) ([cdc159b](https://github.com/googleapis/releasetool/commit/cdc159ba86c22be9d6eba64a1b69f14200bcd4eb))

## [1.16.0](https://github.com/googleapis/releasetool/compare/v1.15.0...v1.16.0) (2023-07-14)


### Features

* Add new Ruby OpenTelemetry repo ([02b6653](https://github.com/googleapis/releasetool/commit/02b6653bbf0238c6f192c86ebb9fa079276d94aa))

## [1.15.0](https://github.com/googleapis/releasetool/compare/v1.14.0...v1.15.0) (2023-06-27)


### Features

* Remove Ruby from Kokoro tagger ([#511](https://github.com/googleapis/releasetool/issues/511)) ([57acf88](https://github.com/googleapis/releasetool/commit/57acf88d49053d67ceb79317e68287f691d45482))


### Bug Fixes

* Update kokoro release job name for google-cloudevents-ruby ([#515](https://github.com/googleapis/releasetool/issues/515)) ([9e98088](https://github.com/googleapis/releasetool/commit/9e980883df4397fa9517911545de5de514876c61))

## [1.14.0](https://github.com/googleapis/releasetool/compare/v1.13.0...v1.14.0) (2023-05-09)


### Features

* Cpp support ([#506](https://github.com/googleapis/releasetool/issues/506)) ([499ae54](https://github.com/googleapis/releasetool/commit/499ae54162045cf844a96956a639e4f4110bd0b4))

## [1.13.0](https://github.com/googleapis/releasetool/compare/v1.12.0...v1.13.0) (2023-05-08)


### Features

* **ruby:** Support the googleapis/google-cloudevents-ruby repo ([#507](https://github.com/googleapis/releasetool/issues/507)) ([f9dd48e](https://github.com/googleapis/releasetool/commit/f9dd48ee5a8f828d0a7b856f8a8d4ef228a07386))

## [1.12.0](https://github.com/googleapis/releasetool/compare/v1.11.0...v1.12.0) (2023-04-25)


### Features

* Add support for triggering go release jobs ([#504](https://github.com/googleapis/releasetool/issues/504)) ([db7dba1](https://github.com/googleapis/releasetool/commit/db7dba1455d96a85c294b2a894ae3d65826b9f4c))

## [1.11.0](https://github.com/googleapis/releasetool/compare/v1.10.5...v1.11.0) (2023-03-24)


### Features

* Add multi_scm option for build proto ([#502](https://github.com/googleapis/releasetool/issues/502)) ([3d6d907](https://github.com/googleapis/releasetool/commit/3d6d90775e7fb1a3102e1dd54667cac70e0ddbb5))

## [1.10.5](https://github.com/googleapis/releasetool/compare/v1.10.4...v1.10.5) (2023-02-15)


### Bug Fixes

* **deps:** Bump cryptography from 38.0.4 to 39.0.1 ([#497](https://github.com/googleapis/releasetool/issues/497)) ([b36d07d](https://github.com/googleapis/releasetool/commit/b36d07df2cef3123ec61a52fe093d30c1c98adb1))

## [1.10.4](https://github.com/googleapis/releasetool/compare/v1.10.3...v1.10.4) (2023-02-03)


### Bug Fixes

* Skip entire tag workflow for languages not in the allowlist ([#495](https://github.com/googleapis/releasetool/issues/495)) ([118f203](https://github.com/googleapis/releasetool/commit/118f2032f811e8152b4d165c7ecf2c34190dd2d0))

## [1.10.3](https://github.com/googleapis/releasetool/compare/v1.10.2...v1.10.3) (2023-01-31)


### Bug Fixes

* Add special case for release languages ([#493](https://github.com/googleapis/releasetool/issues/493)) ([2400f3b](https://github.com/googleapis/releasetool/commit/2400f3bb871a558c587aa64f9af91b25e811aa59))

## [1.10.2](https://github.com/googleapis/releasetool/compare/v1.10.1...v1.10.2) (2022-12-16)


### Bug Fixes

* **java:** Specifying kokoro release job location for cloud java repositories ([#475](https://github.com/googleapis/releasetool/issues/475)) ([035e3ea](https://github.com/googleapis/releasetool/commit/035e3ea41d7867ab67e0dfde3425532aa625dc85))

## [1.10.1](https://github.com/googleapis/releasetool/compare/v1.10.0...v1.10.1) (2022-12-13)


### Bug Fixes

* **ruby:** Check repo name exact match ([#474](https://github.com/googleapis/releasetool/issues/474)) ([7b8e5bb](https://github.com/googleapis/releasetool/commit/7b8e5bb3037d25eefd371dd145b6e94231b52ad8))
* **ruby:** Switch monorepo check to exact repo name match ([#472](https://github.com/googleapis/releasetool/issues/472)) ([fd9b870](https://github.com/googleapis/releasetool/commit/fd9b870183ee01eab0f42875d959557937834f06))

## [1.10.0](https://github.com/googleapis/releasetool/compare/v1.9.1...v1.10.0) (2022-11-15)


### Features

* **php:** Enable release trigger for cloud rad kokoro job ([#458](https://github.com/googleapis/releasetool/issues/458)) ([66d6b67](https://github.com/googleapis/releasetool/commit/66d6b675eb19a24c7b18de2f11f5e4d06e67fa73))

## [1.9.1](https://github.com/googleapis/releasetool/compare/v1.9.0...v1.9.1) (2022-11-02)


### Bug Fixes

* **deps:** Update dependency cryptography to v38.0.3 [security] ([#455](https://github.com/googleapis/releasetool/issues/455)) ([375bc65](https://github.com/googleapis/releasetool/commit/375bc650a5a183537139f2e3f52a39a45cf90db2))

## [1.9.0](https://github.com/googleapis/releasetool/compare/v1.8.10...v1.9.0) (2022-10-26)


### Features

* **ruby:** Add new repo ruby-spanner to Ruby client and mono repos ([#450](https://github.com/googleapis/releasetool/issues/450)) ([1675bfa](https://github.com/googleapis/releasetool/commit/1675bfa53c8acf3af1d1421561f5a4299e180da5))

## [1.8.10](https://github.com/googleapis/releasetool/compare/v1.8.9...v1.8.10) (2022-10-03)


### Bug Fixes

* **build:** Pin deps for python3.6 ([#419](https://github.com/googleapis/releasetool/issues/419)) ([d25da4d](https://github.com/googleapis/releasetool/commit/d25da4d678721d922966c0b020d629483a34e9f3))

## [1.8.9](https://github.com/googleapis/releasetool/compare/v1.8.8...v1.8.9) (2022-09-30)


### Bug Fixes

* **build:** pin requirements ([b331495](https://github.com/googleapis/releasetool/commit/b3314957a0dc6170c951525bc698fb8734fcf788))

## [1.8.8](https://github.com/googleapis/releasetool/compare/v1.8.7...v1.8.8) (2022-09-16)


### Bug Fixes

* Configure kokoro jobs for functions-framework-java release  ([#414](https://github.com/googleapis/releasetool/issues/414)) ([f0b6328](https://github.com/googleapis/releasetool/commit/f0b6328560cf34c613a29088d1b8001f1b4c1670))

## [1.8.7](https://github.com/googleapis/releasetool/compare/v1.8.6...v1.8.7) (2022-08-30)


### Bug Fixes

* implement kokoro_job_name helper for dotnet ([#410](https://github.com/googleapis/releasetool/issues/410)) ([6cab0f8](https://github.com/googleapis/releasetool/commit/6cab0f81530db5b90608ca1ba0b13808e0648c30))

## [1.8.6](https://github.com/googleapis/releasetool/compare/v1.8.5...v1.8.6) (2022-06-09)


### Bug Fixes

* Specifying kokoro release job location for google-cloud-spanner-hibernate ([#406](https://github.com/googleapis/releasetool/issues/406)) ([bd31541](https://github.com/googleapis/releasetool/commit/bd3154170b20a15f72f9cc6efb531fd77c9ae2cc))

## [1.8.5](https://github.com/googleapis/releasetool/compare/v1.8.4...v1.8.5) (2022-06-06)


### Bug Fixes

* **deps:** pin protobuf to 3.x ([#401](https://github.com/googleapis/releasetool/issues/401)) ([c33052d](https://github.com/googleapis/releasetool/commit/c33052d882080a312ea3813d6bbf03301aec525b))

### [1.8.4](https://github.com/googleapis/releasetool/compare/v1.8.3...v1.8.4) (2022-04-14)


### Bug Fixes

* parse v13 release notes header from CHANGELOG.md ([21c2904](https://github.com/googleapis/releasetool/commit/21c290405f427bb7b6241c8e47ad90b3ca6e15ca))
* **ruby:** try to parse release-please v13 branch names ([#396](https://github.com/googleapis/releasetool/issues/396)) ([21c2904](https://github.com/googleapis/releasetool/commit/21c290405f427bb7b6241c8e47ad90b3ca6e15ca))

### [1.8.3](https://github.com/googleapis/releasetool/compare/v1.8.2...v1.8.3) (2022-03-09)


### Bug Fixes

* **debug:** add additional debug information for Ruby ([#391](https://github.com/googleapis/releasetool/issues/391)) ([80f4306](https://github.com/googleapis/releasetool/commit/80f43069f6dc40b58ded713f42c7fd4098921fe2))
* handle release-please v13 pull requests ([#383](https://github.com/googleapis/releasetool/issues/383)) ([cf5b0c0](https://github.com/googleapis/releasetool/commit/cf5b0c0f4834b1b20093d81e8e0082a78258945c))
* remove python from the allowlist ([#386](https://github.com/googleapis/releasetool/issues/386)) ([eea8422](https://github.com/googleapis/releasetool/commit/eea8422cec9dc2139e6feb2e2cc8901c2c232e05))
* **ruby:** Remove hack pointing at legacy release jobs for the Ruby Apiary clients repo ([#376](https://github.com/googleapis/releasetool/issues/376)) ([78d88ca](https://github.com/googleapis/releasetool/commit/78d88ca7d85194d437e16ee1ef9aea9b4e9d24ea))
* stop running autorelease tag for php and python_tool ([#388](https://github.com/googleapis/releasetool/issues/388)) ([0441687](https://github.com/googleapis/releasetool/commit/0441687d56b30e07016199aab2048bde9eeb417e))

### [1.8.2](https://www.github.com/googleapis/releasetool/compare/v1.8.1...v1.8.2) (2021-09-15)


### Bug Fixes

* **nodejs:** stop autorelease for nodejs ([#363](https://www.github.com/googleapis/releasetool/issues/363)) ([c35144b](https://www.github.com/googleapis/releasetool/commit/c35144b3b4c191a59c95c49468c23c38a846e671))
* triggering a single release PR should not use the language allowlist ([#366](https://www.github.com/googleapis/releasetool/issues/366)) ([fcf0077](https://www.github.com/googleapis/releasetool/commit/fcf00770701876c8ef0662776dffcc532809d6c4))

### [1.8.1](https://www.github.com/googleapis/releasetool/compare/v1.8.0...v1.8.1) (2021-09-14)


### Bug Fixes

* handle installation id for GCP org ([#364](https://www.github.com/googleapis/releasetool/issues/364)) ([ee33b52](https://www.github.com/googleapis/releasetool/commit/ee33b52d535561f407bda2274c2f4e708bcd6e3f))
* **ruby:** Fix Kokoro job mapping for several Ruby repos ([#357](https://www.github.com/googleapis/releasetool/issues/357)) ([22751cc](https://www.github.com/googleapis/releasetool/commit/22751cc095d226959c5068120fe34ae7a197e5aa))
* **ruby:** Identify additional Ruby monorepos ([#360](https://www.github.com/googleapis/releasetool/issues/360)) ([7986ae4](https://www.github.com/googleapis/releasetool/commit/7986ae490269afeedae918d0a2476bfc39bf22b0))
* stop handling java repos - they are migrated to release-please/release-trigger ([#362](https://www.github.com/googleapis/releasetool/issues/362)) ([0ce5788](https://www.github.com/googleapis/releasetool/commit/0ce578853ccfa61f5c59bec6229042fc704e56bb))

## [1.8.0](https://www.github.com/googleapis/releasetool/compare/v1.7.0...v1.8.0) (2021-08-25)


### Features

* **ruby:** Kokoro job mapping for additional Ruby repos ([#354](https://www.github.com/googleapis/releasetool/issues/354)) ([f3ee8c8](https://www.github.com/googleapis/releasetool/commit/f3ee8c877fac0f636e985794898d419e16d899fd))

## [1.7.0](https://www.github.com/googleapis/releasetool/compare/v1.6.2...v1.7.0) (2021-08-16)


### Features

* add command for triggering a single kokoro job by PR url ([#349](https://www.github.com/googleapis/releasetool/issues/349)) ([9fa3e06](https://www.github.com/googleapis/releasetool/commit/9fa3e0697c4ab110958e86007a04d2e59cc8c4ad))
* **autorelease:** use ADC if no explicit service account specified ([#342](https://www.github.com/googleapis/releasetool/issues/342)) ([f9e6d6b](https://www.github.com/googleapis/releasetool/commit/f9e6d6b7817c537b59c2d018ba5fbd5823a61c5f))


### Bug Fixes

* fix path in setup.py for template files ([#351](https://www.github.com/googleapis/releasetool/issues/351)) ([970990f](https://www.github.com/googleapis/releasetool/commit/970990ff1028f9c234ec4043a19d95052ce266b5))

### [1.6.2](https://www.github.com/googleapis/releasetool/compare/v1.6.1...v1.6.2) (2021-06-29)


### Bug Fixes

* include jinja template in released package ([#340](https://www.github.com/googleapis/releasetool/issues/340)) ([281cd20](https://www.github.com/googleapis/releasetool/commit/281cd2061ccb7e4ddb1b5575c6612cbbb607f213))

### [1.6.1](https://www.github.com/googleapis/releasetool/compare/v1.6.0...v1.6.1) (2021-05-11)


### Bug Fixes

* **deps:** lock click to 7.x ([#333](https://www.github.com/googleapis/releasetool/issues/333)) ([1cc456c](https://www.github.com/googleapis/releasetool/commit/1cc456c3457304a8301f64b03941f05648b96642))
* limit autorelease trigger job to recent release PRs ([#328](https://www.github.com/googleapis/releasetool/issues/328)) ([3674d7c](https://www.github.com/googleapis/releasetool/commit/3674d7c94aa396925e5d7c5bf97d35563a112d2b))
* only trigger Kokoro jobs once ([#331](https://www.github.com/googleapis/releasetool/issues/331)) ([83b0cae](https://www.github.com/googleapis/releasetool/commit/83b0caec767f8dc540f83f3e54c895d82901ea01))
* revert to using importlib for dynamic module loading ([#326](https://www.github.com/googleapis/releasetool/issues/326)) ([56a75c8](https://www.github.com/googleapis/releasetool/commit/56a75c800875e7420405559f626683731e56fb5b))

## [1.6.0](https://www.github.com/googleapis/releasetool/compare/v1.5.0...v1.6.0) (2021-05-03)


### Features

* add autorelease.trigger command ([#314](https://www.github.com/googleapis/releasetool/issues/314)) ([9feb650](https://www.github.com/googleapis/releasetool/commit/9feb650c697784aad624c01c74e83510e585a63f))


### Bug Fixes

* add allowlist for autorelease.tag command ([#312](https://www.github.com/googleapis/releasetool/issues/312)) ([065efad](https://www.github.com/googleapis/releasetool/commit/065efadd80582793a269491099a572f99f9a9525))
* **java:** allow java builds in autorelease.trigger ([#323](https://www.github.com/googleapis/releasetool/issues/323)) ([1f25b14](https://www.github.com/googleapis/releasetool/commit/1f25b14c5d2ba10924c4bf8e1eb4b3e3987b7468))
* **ruby:** Trigger new Ruby release job from google-cloud-ruby ([#320](https://www.github.com/googleapis/releasetool/issues/320)) ([d813aa7](https://www.github.com/googleapis/releasetool/commit/d813aa713c6569c2aac3cd247bb689b19e31e984))
* run autorelease tag against googleapis and GCP organizations ([#316](https://www.github.com/googleapis/releasetool/issues/316)) ([2463b15](https://www.github.com/googleapis/releasetool/commit/2463b15e0e30292e70a3a920553f579e1622f53e))

## [1.5.0](https://www.github.com/googleapis/releasetool/compare/v1.4.0...v1.5.0) (2021-03-24)


### Features

* **node:** switch to manifest based publication for apiary/repo-automation-bots ([#308](https://www.github.com/googleapis/releasetool/issues/308)) ([ee7c140](https://www.github.com/googleapis/releasetool/commit/ee7c14067cd6f22909cd82e110bf3f69cf22dd58))


### Bug Fixes

* **build:** use trampoline/docker for autorelease job ([#302](https://www.github.com/googleapis/releasetool/issues/302)) ([da7972c](https://www.github.com/googleapis/releasetool/commit/da7972c5c69da6bc1f8e9bb80718eebb15a3c9f1))
* **java:** fix Kokoro job triggering ([#305](https://www.github.com/googleapis/releasetool/issues/305)) ([e68b90d](https://www.github.com/googleapis/releasetool/commit/e68b90d7cce9d2f478845dcfee4342e860dd44f0))
* **java:** use release-please for java tagging ([#303](https://www.github.com/googleapis/releasetool/issues/303)) ([58a17d5](https://www.github.com/googleapis/releasetool/commit/58a17d5271de8a88950b3012408a50367808a2fe))
* **java:** use token file for release-please ([#304](https://www.github.com/googleapis/releasetool/issues/304)) ([19ca380](https://www.github.com/googleapis/releasetool/commit/19ca380986690c501342ee6f183381c0768df5c4))
* **manifest:** defer to manifest releaser for version/CHANGELOG ([#310](https://www.github.com/googleapis/releasetool/issues/310)) ([a1bb40d](https://www.github.com/googleapis/releasetool/commit/a1bb40dc4d3c4155ba5d9e7aff3bc3c327ab1458))
* switch to using search API for finding merged release PRs ([#306](https://www.github.com/googleapis/releasetool/issues/306)) ([19cb029](https://www.github.com/googleapis/releasetool/commit/19cb0291ccd4a2f54f70c28fc9abbe739c8f28f3))
* treat docuploader as a python repo ([#298](https://www.github.com/googleapis/releasetool/issues/298)) ([34b0666](https://www.github.com/googleapis/releasetool/commit/34b066654d97ec5decf2c07669ab5cfea0faa2a0))


### Reverts

* "refactor(java): delegate tagging to release-please" ([#301](https://www.github.com/googleapis/releasetool/issues/301)) ([d646a1b](https://www.github.com/googleapis/releasetool/commit/d646a1bdd7c17c0882f8df087cb73fd7d4c7d740))

## [1.4.0](https://www.github.com/googleapis/releasetool/compare/v1.3.0...v1.4.0) (2021-01-06)


### Features

* **ruby:** Support releases of split ruby apiary packages ([#295](https://www.github.com/googleapis/releasetool/issues/295)) ([0b61bd0](https://www.github.com/googleapis/releasetool/commit/0b61bd0c5396e437f67878b62ec332d8603ace78))

## [1.3.0](https://www.github.com/googleapis/releasetool/compare/v1.2.0...v1.3.0) (2021-01-05)


### Features

* **nodejs:** googleapis release is handled by actions ([#291](https://www.github.com/googleapis/releasetool/issues/291)) ([b210db6](https://www.github.com/googleapis/releasetool/commit/b210db63b5b27177b22eccd32f6b624afda0a024))


### Bug Fixes

* Make the .NET tagging regex stricter ([#290](https://www.github.com/googleapis/releasetool/issues/290)) ([7aebab9](https://www.github.com/googleapis/releasetool/commit/7aebab9d3399d3997c837131b3a90db05f52353b))
* Remove spurious method call when exchanging JWT for an access token ([#296](https://www.github.com/googleapis/releasetool/issues/296)) ([b2b9b83](https://www.github.com/googleapis/releasetool/commit/b2b9b83dfef3e1abfb0897be69b2012afdb4d901))
* **nodejs:** semver digits are not optional ([#289](https://www.github.com/googleapis/releasetool/issues/289)) ([579a4e9](https://www.github.com/googleapis/releasetool/commit/579a4e94ea4ec05819ae03568046267fae6db28c))


### Documentation

* recommend installing from PyPI ([#285](https://www.github.com/googleapis/releasetool/issues/285)) ([c1729b7](https://www.github.com/googleapis/releasetool/commit/c1729b7198afe189fde11e2ec54373c895bfafff))

## [1.2.0](https://www.github.com/googleapis/releasetool/compare/v1.1.3...v1.2.0) (2020-09-30)


### Features

* Allow the .NET autorelease process to work across multiple repositories ([c7e4bf8](https://www.github.com/googleapis/releasetool/commit/c7e4bf85495b0ebd86586546e78c8b8638b3d0a0))


### Bug Fixes

* **ruby:** Cut problematic text from release PR body ([#277](https://www.github.com/googleapis/releasetool/issues/277)) ([9e39a71](https://www.github.com/googleapis/releasetool/commit/9e39a7191b2db48c4e8e485136990233c2a13bcf))
* paths in kokoro build scripts ([#275](https://www.github.com/googleapis/releasetool/issues/275)) ([005e779](https://www.github.com/googleapis/releasetool/commit/005e779092b04b42d6cbb5c0ed188fabadcf97cc))

### [1.1.3](https://www.github.com/googleapis/releasetool/compare/v1.1.2...v1.1.3) (2020-08-26)


### Bug Fixes

* **build:** fix permissions for publish reporter ([#272](https://www.github.com/googleapis/releasetool/issues/272)) ([638ca66](https://www.github.com/googleapis/releasetool/commit/638ca6628b419e185ac2204739bb513c9f38c3e5))

### [1.1.2](https://www.github.com/googleapis/releasetool/compare/v1.1.1...v1.1.2) (2020-08-26)


### Bug Fixes

* referenced github_token rather than github_token_raw ([#270](https://www.github.com/googleapis/releasetool/issues/270)) ([2bb815a](https://www.github.com/googleapis/releasetool/commit/2bb815a00dfc96cc574fe1b714dc20b47a914698))

### [1.1.1](https://www.github.com/googleapis/releasetool/compare/v1.1.0...v1.1.1) (2020-08-26)


### Bug Fixes

* **nodejs:** move back to autorelease for publishes ([#267](https://www.github.com/googleapis/releasetool/issues/267)) ([a693434](https://www.github.com/googleapis/releasetool/commit/a693434d9dfe34d59d5197761d780785391f3eca))
* continue to accept string token ([#266](https://www.github.com/googleapis/releasetool/issues/266)) ([21fc63a](https://www.github.com/googleapis/releasetool/commit/21fc63a2ea17215bf96dff9f15146af304d5af80))

## [1.1.0](https://www.github.com/googleapis/releasetool/compare/v1.0.2...v1.1.0) (2020-08-26)


### Features

* add support for GitHub  JWT auth ([#262](https://www.github.com/googleapis/releasetool/issues/262)) ([ff891a4](https://www.github.com/googleapis/releasetool/commit/ff891a41001f95ed10046adf252bad3bb1b289a8))

### [1.0.2](https://www.github.com/googleapis/releasetool/compare/v1.0.1...v1.0.2) (2020-08-24)


### Bug Fixes

* correct version in setup.py ([#260](https://www.github.com/googleapis/releasetool/issues/260)) ([f81af0a](https://www.github.com/googleapis/releasetool/commit/f81af0a87c9a2a733e52ab28676fc667570dbe3b))

### [1.0.1](https://www.github.com/googleapis/releasetool/compare/v1.0.0...v1.0.1) (2020-08-24)


### Bug Fixes

* swallow exceptions to the GitHub proxy so we don't show the url ([#257](https://www.github.com/googleapis/releasetool/issues/257)) ([616a8a8](https://www.github.com/googleapis/releasetool/commit/616a8a86062bf2ef50ae5e0fcf78d8f34fe62ad2))

## 2019.06.14

06-14-2019 09:09 PDT


### Implementation Changes
- fix: fix last release detection for non-cloud packages in Ruby ([#208](https://github.com/googleapis/releasetool/pull/208))

### Documentation
- docs: add section to README about auth ([#206](https://github.com/googleapis/releasetool/pull/206))

## 2019.06.06.1

06-06-2019 15:41 PDT

### Implementation Changes
- Java: autorelease by default ([#204](https://github.com/googleapis/releasetool/pull/204))
- Enable autorelease for all java projects ([#202](https://github.com/googleapis/releasetool/pull/202))
- fix: update key name of releasetool magictoken ([#201](https://github.com/googleapis/releasetool/pull/201))
- Java: add prompt for autorelease when creating PR ([#200](https://github.com/googleapis/releasetool/pull/200))

## 2019.06.06

06-06-2019 09:50 PDT


### Implementation Changes
- fix: release extraction regex was not handling patch releases properly ([#193](https://github.com/googleapis/releasetool/pull/193))
- Fix changelog detection for Ruby. ([#192](https://github.com/googleapis/releasetool/pull/192))
- fix: Ruby tagging for google-cloud package ([#190](https://github.com/googleapis/releasetool/pull/190))
- ruby: Update start create_release_pr() ([#186](https://github.com/googleapis/releasetool/pull/186))
- Update releasetool.commands.common.setup_github_context ([#188](https://github.com/googleapis/releasetool/pull/188))
- ruby: Add checkout_master() to finish of start ([#187](https://github.com/googleapis/releasetool/pull/187))
- Fix incorrect path to magic github proxy api key. ([#197](https://github.com/googleapis/releasetool/pull/197))
- Use magic github proxy for releasetool reporter ([#166](https://github.com/googleapis/releasetool/pull/166))

### New Features
- Java: detect current working branch to use for release ([#196](https://github.com/googleapis/releasetool/pull/196))
- Allow user to specify no version bump so you can just run the version replace ([#194](https://github.com/googleapis/releasetool/pull/194))

## 2019.05.02

05-02-2019 12:40 PDT


### Implementation Changes
- Fix ruby start#determine_last_release. ([#184](https://github.com/googleapis/releasetool/pull/184))
- ctx is populated by reference. ([#183](https://github.com/googleapis/releasetool/pull/183))
- Detect language python when a directory src/google exists. ([#180](https://github.com/googleapis/releasetool/pull/180))

### New Features
- Java: support updating dependencies.properties. ([#178](https://github.com/googleapis/releasetool/pull/178))
- Add support for conventionalcommits.org CHANGELOG template. ([#181](https://github.com/googleapis/releasetool/pull/181))

## 2019.04.04

04-04-2019 12:52 PDT


### Implementation Changes
- Make setup.py update robust to different quote marks ([#175](https://github.com/googleapis/releasetool/pull/175))
- handle errors in delete branch ([#169](https://github.com/googleapis/releasetool/pull/169))
- Ruby delete branch ([#163](https://github.com/googleapis/releasetool/pull/163))
- Allow underscores in package name ([#162](https://github.com/googleapis/releasetool/pull/162))

### New Features
- [RUBY] support non-google-cloud repos ([#173](https://github.com/googleapis/releasetool/pull/173))

### Documentation
- Re-add manual `releasetool tag` instructions ([#172](https://github.com/googleapis/releasetool/pull/172))
- Update releasetool tag instructions ([#171](https://github.com/googleapis/releasetool/pull/171))

## 2019.01.25

01-25-2019 15:24 PST


### Implementation Changes
- change target_committish to target_commitish ([#160](https://github.com/googleapis/releasetool/pull/160))
- Fix go start ([#156](https://github.com/googleapis/releasetool/pull/156))
- use release_tag for tag_name ([#158](https://github.com/googleapis/releasetool/pull/158))
- Fix ruby regex for matching tag ([#157](https://github.com/googleapis/releasetool/pull/157))
- update ruby tag regex ([#155](https://github.com/googleapis/releasetool/pull/155))
- change ruby bullet points to * ([#154](https://github.com/googleapis/releasetool/pull/154))
- Correct name of repo, kokoro job and remove autorelease: pending label from PR ([#152](https://github.com/googleapis/releasetool/pull/152))

### New Features
- prepare ruby for autorelease ([#151](https://github.com/googleapis/releasetool/pull/151))
- Make releasetool tag trigger stage job for google-auth-java-library ([#150](https://github.com/googleapis/releasetool/pull/150))

### Documentation
- Clarify installation steps in README ([#147](https://github.com/googleapis/releasetool/pull/147))

## 2018.12.10

12-10-2018 15:26 PST


### Implementation Changes
- fix: run releasetool as module ([#140](https://github.com/GoogleCloudPlatform/releasetool/pull/140))
- fix(node): kokoro job name ([#139](https://github.com/GoogleCloudPlatform/releasetool/pull/139))
- fix: publish_reporter.sh runs releasetool as python3 module ([#138](https://github.com/GoogleCloudPlatform/releasetool/pull/138))
- Make Node.js use the context to determine repo name for Kokoro job ([#135](https://github.com/GoogleCloudPlatform/releasetool/pull/135))
- Don't try to commit samples/package.json if it doesn't exist ([#131](https://github.com/GoogleCloudPlatform/releasetool/pull/131))
- Go commit msg ([#128](https://github.com/GoogleCloudPlatform/releasetool/pull/128))

### New Features
- node: add autorelease: pending label for releasetool start ([#127](https://github.com/GoogleCloudPlatform/releasetool/pull/127))
- Enable Autorelease for Python ([#132](https://github.com/GoogleCloudPlatform/releasetool/pull/132))
- Make nodejs releasetool tag work in non-interactive mode ([#126](https://github.com/GoogleCloudPlatform/releasetool/pull/126))
- Make releasetool tag for Python work in non-interactive mode ([#129](https://github.com/GoogleCloudPlatform/releasetool/pull/129))

### Documentation
- Update README.md

## 2018.11.07.2

11-07-2018 13:32 PST

### Implementation Changes

- Change the autorelease label names, add labeling to 'tag' for python-tool ([#124](https://github.com/googleapis/releasetool/pull/124))

## 2018.11.07.1

11-07-2018 12:25 PST

### Implementation Changes

- Catch requests exceptions when checking if a release exists (#122)

## 2018.11.07

11-07-2018 10:30 PST

### Implementation Changes

- Make tag idempotent ([#118](https://github.com/googleapis/releasetool/pull/118))
- Add steps for tagging the merged commit for the release ([#119](https://github.com/googleapis/releasetool/pull/119))
- Use a different method of ignoring errors when reporting release status ([#117](https://github.com/googleapis/releasetool/pull/117))

### Internal / Testing Changes

- Use yoshi-automation GitHub account ([#120](https://github.com/googleapis/releasetool/pull/120))

## 2018.11.05

11-05-2018 10:50 PST

### Implementation Changes

- Prompt when a calver release collides with the most recent release tag. ([#112](https://github.com/googleapis/releasetool/pull/112))
- Fix release reporter's determination of the GitHub token ([#113](https://github.com/googleapis/releasetool/pull/113))

### Internal / Testing Changes

- Install releasetool from source in the release job ([#115](https://github.com/googleapis/releasetool/pull/115))
- Update github issue templates ([#114](https://github.com/googleapis/releasetool/pull/114))

## 2018.11.02.2

11-02-2018 15:25 PDT

### Implementation Changes

- Allow version regex to include more than 3 segements. Matches PEP440. ([#109](https://github.com/googleapis/releasetool/pull/109))

## 2018.11.02.1

11-02-2018 14:47 PDT

### Internal / Testing Changes

- Added github bot token to build

## 2018.11.02

11-02-2018 14:27 PDT

### Implementation Changes

- Only include merged PRs in release PR list ([#104](https://github.com/googleapis/releasetool/pull/104))
- Update package name and version regex ([#105](https://github.com/googleapis/releasetool/pull/105))
- Let reporter figure out the github token location instead of needing to manually specify it ([#102](https://github.com/googleapis/releasetool/pull/102))

### New Features

- Add release reporter script. ([#101](https://github.com/googleapis/releasetool/pull/101))

## 2018.11.01

11-01-2018 10:16 PDT

### New Features

- Add reporting commands for release builds ([#99](https://github.com/googleapis/releasetool/pull/99))

## 2018.10.31

10-31-2018 13:54 PDT

### Implementation Changes

- Only apply autorelease tag for python-tool (for now). ([#97](https://github.com/googleapis/releasetool/pull/97))
- Fix typo in ruby command
- Allow remotes that don't end in .git ([#92](https://github.com/googleapis/releasetool/pull/92))
- Create tag context and move publish_via_kokoro to common ([#91](https://github.com/googleapis/releasetool/pull/91))
- Only use calver for python_tools, not python ([#94](https://github.com/googleapis/releasetool/pull/94))

### New Features

- Finish up autorelease support for python-tool ([#87](https://github.com/googleapis/releasetool/pull/87))

## 2018.10.25

10-25-2018 13:18 PDT

### New Features

- Allow python-tool tag to be executed with external context.

### Internal / Testing Changes

- Fix lint errors around bad escape characters

## 2018.10.23

10-23-2018 13:02 PDT

### Implementation Changes

- Use CalVer for Python Tools ([#80](https://github.com/googleapis/releasetool/pull/80))

### New Features

- Add command to reset GitHub API key ([#79](https://github.com/googleapis/releasetool/pull/79))

## 0.10.0

10-09-2018 14:29 PDT

### Implementation Changes
- Cut release branch from master, warn when master != upstream/master. ([#76](https://github.com/GoogleCloudPlatform/releasetool/pull/76))
- fix(nodejs): change output from PyPI -> npm ([#75](https://github.com/GoogleCloudPlatform/releasetool/pull/75))

### New Features
- Java: support multiple versions per release ([#74](https://github.com/GoogleCloudPlatform/releasetool/pull/74))
- Autodetect java if a root pom.xml file exists ([#73](https://github.com/GoogleCloudPlatform/releasetool/pull/73))
- Add start command for Go ([#67](https://github.com/GoogleCloudPlatform/releasetool/pull/67))

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
