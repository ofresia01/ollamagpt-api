# [1.2.0](https://github.com/ofresia01/ollama-fastapi-rs/compare/v1.1.0...v1.2.0) (2025-02-16)


### Features

* **model-lifecycle:** added functions for creating and deleting the model, handled by fastapi context manager ([50b3822](https://github.com/ofresia01/ollama-fastapi-rs/commit/50b38221403b5d339afc50b1388ea6d26be94d8b))
* **programmatic-model-creation:** creating ollama model with ollama api, with parameterized system prompts ([8e08675](https://github.com/ofresia01/ollama-fastapi-rs/commit/8e08675d7eaa756fa134e8a700ea225d58463a70))

# [1.1.0](https://github.com/ofresia01/ollama-fastapi-rs/compare/v1.0.1...v1.1.0) (2025-02-16)


### Features

* **bypass-validation:** added header as flag for bypassing input validation ([2822430](https://github.com/ofresia01/ollama-fastapi-rs/commit/28224304ba42bb49739401b6a35b426c2074e798))

## [1.0.1](https://github.com/ofresia01/ollama-fastapi-rs/compare/v1.0.0...v1.0.1) (2025-02-16)


### Bug Fixes

* **tag-deployment.yml:** renamed to release.yml, removed unnecessary permissions ([91b90fc](https://github.com/ofresia01/ollama-fastapi-rs/commit/91b90fc20f97e9ced5f42877ad837d94e7f4f8f6))

# 1.0.0 (2025-02-16)


### Bug Fixes

* **start.sh:** relative reference to prometheus config file ([e138170](https://github.com/ofresia01/ollama-fastapi-rs/commit/e13817078ed0757856315108abc228bae8e5271a))
* **tag-deployment.yml:** changed commands for installing and verifying to run with no package-lock.json ([8c90bd7](https://github.com/ofresia01/ollama-fastapi-rs/commit/8c90bd7ddf418806512abd7a840ad4fcde418913))
* **tag-deployment.yml:** installing lts version of node, verifying deps, one reference for npm and github token, configured permissions ([147ad07](https://github.com/ofresia01/ollama-fastapi-rs/commit/147ad07054ee755533f3b6ed8b49cbd5c60162dd))


### Features

* **github-actions:** added semantic versioning ([6278dfe](https://github.com/ofresia01/ollama-fastapi-rs/commit/6278dfe3831a81725daaabe95b961ab572ffd852))
* initial release ([fcfc554](https://github.com/ofresia01/ollama-fastapi-rs/commit/fcfc554beba08bf7972963ef362ef9fadbcb88db))
