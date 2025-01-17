# builds the container image for the component.
build: clean
    poetry build -f wheel
    echo "$ARTIFACTORY_USER" > artifactory_user.txt
    echo "$ARTIFACTORY_API_KEY" > artifactory_api_key.txt

    docker build \
     --secret id=ARTIFACTORY_USER,src=artifactory_user.txt \
     --secret id=ARTIFACTORY_API_KEY,src=artifactory_api_key.txt \
     -t covera-poetry-template:1.0.0 .

    rm artifactory_user.txt
    rm artifactory_api_key.txt

# clean removes the build output directory, /dist
clean:
    rm -rf dist/

# format executes black, isort, and docformatter against source and test code directories.
format:
    poetry run sh -c 'black . && isort . && docformatter -i -r src tests'

# format-verbose executes black, isort, and docformatter against source and test code directories, with verbose output.
format-verbose:
    poetry run sh -c 'black -v . && isort -v . && docformatter -i -r .'

# format-dryrun displays formatting diff information for source and test code directories.
format-dryrun:
    poetry run sh -c 'black --diff --color . && isort . && docformatter -i -r src tests'

# quickstart is used to execute a small end to end test case within the local enviornment.
quickstart: build
    echo "executing quickstart"

# services-log displays service logs for all or selected components. Example: services-log db-migrations.
services-log *args:
    docker compose {{args}} logs

# services-remove removes compose services, including volumes.
services-remove *args:
    docker compose {{args}} down -v

# convenience wrapper for services-remove *args.
services-remove-all:
    docker compose --profile migration --profile primary-index down -v

# services-start starts compose services with zero or more arguments. The args are passed to docker compose up.
services-start *args:
    docker compose {{args}} up -d

# services-status provides the status of the qcc-study-hall service containers.
services-status *args:
    docker compose {{args}} ps

# services-stop stops services, keeping compose volumes, networks, etc intact.
services-stop *args:
    docker compose {{args}} stop

# setup creates the project's virtual environment.
setup options="dev,test":
    poetry env use $(which python3)
    poetry install --with={{options}} --sync

# test runs pytest with the specified arguments.
test *args:
    poetry run pytest {{args}}

# test-coverage runs pytest with the coverage plugin.
test-coverage:
    poetry run pytest --cov-report term-missing --cov=src/covera_poetry_template --cov-fail-under=80 tests/

# covera-ddtrace-yml creates a yaml configuration for the Data Dog agent.
covera-ddtrace-yml:
    env DD_TRACE_ENABLED=0 \
    poetry run python3 -m covera_ddtrace.utils.generate_covera_ddtrace_yml \
        -r src/covera_poetry_template \
        -s src/ \
        -d covera-ddtrace.yml \
        -n ""


