Development
===========
This package leverages poetry for dependencies and packaging. To install poetry, run the following command:

:command:`pip install poetry`

How to run the tests
--------------------
All tests are located in the `tests` directory. To run the tests, run the following command:

:command:`poetry run python3 -m unittest discover tests`

How to run the linter
---------------------
To run the linter, run the following command:

:command:`python3 -m flake8 canonicalwebteam tests && python3 -m black --line-length 79 --check canonicalwebteam tests`


How to Contribute
-----------------
To improve this module or report issues, you can visit the `GitHub repository <https://github.com/canonical/canonicalwebteam.store-base>`_.
