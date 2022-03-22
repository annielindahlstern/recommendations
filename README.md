# recommendations

[![Build Status](https://github.com/Recommendations-DevOps/recommendations/actions/workflows/workflow.yml/badge.svg)](https://github.com/Recommendations-DevOps/recommendations/actions)
[![Codecov](https://codecov.io/gh/Recommendations-DevOps/recommendations/branch/master/graph/badge.svg)](https://codecov.io/gh/Recommendations-DevOps/recommendations/branch/master/graph/badge.svg)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Available calls and inputs
```create_recs```  """Creates a Recommendation - This endpoint will create a Recommendation based the data in the body that is posted"""
```list_recs``` """ Lists all Recommendations - This endpoint will list all recommendations in the database."""
```def check_content_type(media_type):```     """Checks that the media type is correct"""
```get_recommendation```  """Retrieve a single recommendation - This endpoint will return a recommendation based on it's id"""
```delete_recommendations```  """Delete a Recommendations - This endpoint will delete a Recommendations based the id specified in the path"""

```init_db```         """ Initializes the database session """
```all```         """ Returns all of the RecommendationModel in the database """
```find```         """ Finds a YourResourceModel by it's ID """
```find_or_404```         """ Find a YourResourceModel by it's id """
```find_by_name```         """Returns all Recommendations with the given name
```find_by_original_product_id``` """Returns all Recommendations with the given original product ID"""
```find_by_reason```         """Returns all Recommendations with the given reason"""
    """Enumeration of Potential Reasons"""

       CROSS_SELL = 0
       UP_SELL = 1
       ACCESSORY = 2
       OTHER  = 3

```find_by_recommendation_product_id```         """Returns all Recommendations with the given recommendation product ID"""
```find_by_recommendation_product_name```         """Returns all Recommendations with the given recommendation product name"""

## Running the tests

As developers we always want to run the tests before we change any code. That way we know if we broke the code or if someone before us did. Always run the test cases first!

Run the tests using `nosetests`

```shell
$ nosetests
```

Nose is configured via the included `setup.cfg` file to automatically include the flags `--with-spec --spec-color` so that red-green-refactor is meaningful. If you are in a command shell that supports colors, passing tests will be green while failing tests will be red.

Nose is also configured to automatically run the `coverage` tool and you should see a percentage-of-coverage report at the end of your tests. If you want to see what lines of code were not tested use:

```shell
$ coverage report -m
```

This is particularly useful because it reports the line numbers for the code that have not been covered so you know which lines you want to target with new test cases to get higher code coverage.

You can also manually run `nosetests` with `coverage` (but `setup.cfg` does this already)

```shell
$ nosetests --with-coverage --cover-package=service
```

Try and get as close to 100% coverage as you can.

It's also a good idea to make sure that your Python code follows the PEP8 standard. `flake8` has been included in the `requirements.txt` file so that you can check if your code is compliant like this:

```shell
$ flake8 --count --max-complexity=10 --statistics service
```

I've also included `pylint` in the requirements. Visual Studio Code is configured to use `pylint` while you are editing. This catches a lot of errors while you code that would normally be caught at runtime. It's a good idea to always code with pylint active.

## Running the service

The project uses *honcho* which gets it's commands from the `Procfile`. To start the service simply use:

```shell
$ honcho start
```

You should be able to reach the service at: http://localhost:8000. The port that is used is controlled by an environment variable defined in the `.flaskenv` file which Flask uses to load it's configuration from the environment by default.

## Shutdown development environment

If you are using Visual Studio Code with Docker, simply exiting Visual Studio Code will stop the docker containers. They will start up again the next time you need to develop as long as you don't manually delete them.

If you are using Vagrant and VirtualBox, when you are done, you can exit and shut down the vm with:

```shell
$ exit
$ vagrant halt
```

If the VM is no longer needed you can remove it with:

```shell
$ vagrant destroy
```

## What's featured in the project?

    * app/routes.py -- the main Service routes using Python Flask
    * app/models.py -- the data model using SQLAlchemy
    * tests/test_routes.py -- test cases against the Pet service
    * tests/test_models.py -- test cases against the Pet model

## License

Copyright (c) John Rofrano. All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repo is part of the NYU masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** conceived, created and taught by *John Rofrano*
