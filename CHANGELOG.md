## [1.3.2](https://github.com/ofresia01/ollama-fastapi-rs/compare/v1.3.1...v1.3.2) (2025-02-22)


### Bug Fixes

* **async:** awaiting async chat request in root endpoint ([c75579b](https://github.com/ofresia01/ollama-fastapi-rs/commit/c75579bee9a4c85ed1c463e242c8ab11d82e94c8))

## [1.3.1](https://github.com/ofresia01/ollama-fastapi-rs/compare/v1.3.0...v1.3.1) (2025-02-17)


### Bug Fixes

* **routes.py:** correctly propagating exception in chat_stream and root, awaiting call to request.json() ([f637a05](https://github.com/ofresia01/ollama-fastapi-rs/commit/f637a0598fd64aeedf7ade1265402ecc151ccbf6))

# [1.3.0](https://github.com/ofresia01/ollama-fastapi-rs/compare/v1.2.0...v1.3.0) (2025-02-17)


### Bug Fixes

* **main.py:** binded custom lifecycle to fastapi app, corrected pathing of ollama utility calls ([7a61378](https://github.com/ofresia01/ollama-fastapi-rs/commit/7a61378bcf868842e2e0108ba56df49803d8013e))
* **ollama_utils:** corrected quotes syntax in downloading/tqdm logic ([0d30805](https://github.com/ofresia01/ollama-fastapi-rs/commit/0d308054ddd4f385d7d486d9f3b063283bc43c70))
* **routes.py:** corrected imports for logger, model name, and rate limiter ([5256aa5](https://github.com/ofresia01/ollama-fastapi-rs/commit/5256aa5876de657fddbf391b68b87a1bfc41c679))


### Features

* **model-lifecycle:** added handling for automatic creation, deletion, and downloading of ollama models ([0fe15e1](https://github.com/ofresia01/ollama-fastapi-rs/commit/0fe15e138c409db5b7639775628e02ccd2cc8759))

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
