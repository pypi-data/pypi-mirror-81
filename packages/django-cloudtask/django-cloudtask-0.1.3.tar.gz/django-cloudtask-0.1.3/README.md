# django-cloudtask
A django package for managing long running tasks via Cloud Run and Cloud Scheduler

[![CircleCI](https://circleci.com/gh/kogan/django-cloudtask.svg?style=svg)](https://circleci.com/gh/kogan/django-cloudtask)

## Should I be using this package?

Probably not.

## Configuration

Make sure these are in your django settings:

 - `PROJECT_ID`
   - the GCP project
 - `PROJECT_REGION`
   - GCP region
 - `TASK_SERVICE_ACCOUNT`
   - Service account which will be authenticated against
 - `TASK_DOMAIN`
   - domain which receives tasks (cloud run)
 - `TASK_DEFAULT_QUEUE`
   - default queue tasks will be added to

## Contributing

We use `pre-commit <https://pre-commit.com/>` to enforce our code style rules
locally before you commit them into git. Once you install the pre-commit library
(locally via pip is fine), just install the hooks::

    pre-commit install -f --install-hooks

The same checks are executed on the build server, so skipping the local linting
(with `git commit --no-verify`) will only result in a failed test build.

Current style checking tools:

- flake8: python linting
- isort: python import sorting
- black: python code formatting

Note:

    You must have python3.6 available on your path, as it is required for some
    of the hooks.
