#!/usr/bin/env bash

cleanup() {
    rv=$?
    # on exit code 1 this is normal (some tests failed), do not stop the build
    if [ "$rv" = "1" ]; then
        exit 0
    else
        exit $rv
    fi
}

trap "cleanup" INT TERM EXIT

if [ "${TRAVIS_PYTHON_VERSION}" = "3.5" ] && [ "${PYTEST_VERSION}" = "" ]; then
    # full
    # First the raw for coverage
    echo -e "\n\n****** Running tests : 1/2 RAW******\n\n"
    coverage run --source pytest_pilot -m pytest -v pytest_pilot/test_cases/basic/
    # other runs with flags
    coverage run --append --source pytest_pilot -m pytest -v pytest_pilot/test_cases/basic/ -Z
    coverage run --append --source pytest_pilot -m pytest -v pytest_pilot/test_cases/basic/ --hf
    coverage run --append --source pytest_pilot -m pytest -v pytest_pilot/test_cases/basic/ --envid=env1 --flavour=yellow
    # python -m pytest --cov-report term-missing --cov=./pytest_pilot -v pytest_pilot/test_cases/

    # Then the meta (appended)
    echo -e "\n\n****** Running tests : 2/2 META******\n\n"
    coverage run --append --source pytest_pilot -m pytest --junitxml=reports/junit/junit.xml --html=reports/junit/report.html -v pytest_pilot/tests/
    # buggy
    # python -m pytest --junitxml=reports/junit/junit.xml --html=reports/junit/report.html --cov-report term-missing --cov=./pytest_pilot --cov-append -v pytest_pilot/tests/
else
    # faster - skip coverage and html report but keep junit (because used in validity threshold)
    echo -e "\n\n****** Running tests******\n\n"
    python -m pytest --junitxml=reports/junit/junit.xml -v pytest_pilot/tests/
fi
