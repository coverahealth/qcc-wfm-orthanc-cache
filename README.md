# Poetry Template Project


## Template Instructions
This project can be used as a template for creating new covera repos that adhere to our general repo file structure and includes a Justfile, covera-ddtrace file, Dockerfile, and more.
Remove this section and subsections when creating the new project README. Project README guidance
is provided following this main section.

Supported Python Version: 3.10.6

### Setup

```shell
just setup
just test-coverage
```

### Pytest Configuration

This template has its pytest configuration defined in `pyproject.toml` under `[tool.pytest.ini_options]`.

There you will notice the following commented-out options:

`asyncio_mode`

This is only applicable if the [`pytest-asyncio`](https://pytest-asyncio.readthedocs.io/en/latest/index.html) plugin is installed.

`filterwarnings::'ignore:.*/var/run/secrets.*'`

This will prevent warnings arising from a missing `/var/run/secrets` directory, which is not necessary for running tests.
This is only applicable to projects with a secrets directory, such as the [`qcc-agent-controller`](https://github.com/coverahealth/qcc-agent-controller/blob/cc1b87866b9d6c52818df7f36229925b91fe025d/src/qcc_agent_controller/config.py#L54).


`filterwarnings::'ignore:.*/var/app/secrets/execution_engine.*'`

This will prevent warnings arising from a missing execution engine secrets directory.
This is only applicable to projects using the [`qcc-execution-wrapper`](https://github.com/coverahealth/qcc-execution-wrapper/blob/bb83c13dda5983640596d1689c4085b2fea77a4c/src/wrapper/config.py#L30-L32).

## Overview

Please provide a brief description of the project and how it's used withing the QCC gateway

## Dependencies

List and describe third party dependencies required for the project (docker, nats cli, etc)

## Quickstart

Provide examples of setting up the project, running tests, running locally, etc.
This is executed using the `just quickstart` recipe.

## Additional Documentation

- [Data Contract](./docs/data-contract.md)
- [Design](./docs/design.md)
- [Testing](./docs/testing.md)