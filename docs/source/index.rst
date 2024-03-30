Зависимости
===========

Требуемое ПО:

1. Docker для контейнеризации – |link_docker|

.. |link_docker| raw:: html

   <a href="https://www.docker.com" target="_blank">Docker Desktop</a>

2. Для работы с системой контроля версий – |link_git|

.. |link_git| raw:: html

   <a href="https://github.com/git-guides/install-git" target="_blank">Git</a>

3. IDE для работы с исходным кодом – |link_pycharm| (Опционально)

.. |link_pycharm| raw:: html

    <a href="https://www.jetbrains.com/ru-ru/pycharm/download" target="_blank">PyCharm</a>


Установка
=========

Clone the repository to your computer:

.. code:: bash

   git clone https://github.com/kmalahov/python-course-favorite-places

1. To configure the application copy `.env.sample` into `.env` file:

    .. code-block:: console

        cp .env.sample .env

    This file contains environment variables that will share their values
    across the application. The sample file (`.env.sample`) contains a
    set of variables with default values. So it can be configured
    depending on the environment.

2. Build the container using Docker Compose:

    .. code-block:: console

        docker compose build

    This command should be run from the root directory where `Dockerfile`
    is located. You also need to build the docker container again in case
    if you have updated `requirements.txt`.

3. To run application correctly set up the database. Apply migrations to create tables in the database:

    .. code-block:: console

        docker compose run favorite-places-app alembic upgrade head

4. To run application correctly set up the database. Apply migrations to create tables in the database:

    .. code-block:: console

        docker compose up

    When containers are up server starts at http://0.0.0.0:8010/docs. You can open it in your browser.

Использование
=============

To first initialize migration functionality run:

    .. code-block:: console

        docker compose exec favorite-places-app alembic init -t async migrations

    This command will create a directory with configuration files to set up asynchronous migrations' functionality.

To create new migrations that will update database tables according updated models run this command:

    .. code-block:: console

        docker compose run favorite-places-app alembic revision --autogenerate  -m "your description"

To apply created migrations run:

    .. code-block:: console

        docker compose run favorite-places-app alembic upgrade head

Автоматизация
=============

The project contains a special `Makefile` that provides shortcuts for
a set of commands:

1. Build the Docker container:

    .. code-block:: console

        make build

2. Generate Sphinx documentation run:

    .. code-block:: console

        make docs-html

3. Autoformat source code:

    .. code-block:: console

        make format

4. Static analysis (linters):

    .. code-block:: console

        make lint

5. Autotests:

    .. code-block:: console

        make test

   The test coverage report will be located at
   `src/htmlcov/index.html`. So you can estimate the quality of
   automated test coverage.

6. Run autoformat, linters and tests in one command:

    .. code-block:: console

        make all

    Run these commands from the source directory where `Makefile` is
    located.

Documentation
-------------

The project integrated with the
`Sphinx <https://www.sphinx-doc.org/en/master/>`__ documentation engine.
It allows the creation of documentation from source code. So the source
code should contain docstrings in
`reStructuredText <https://docutils.sourceforge.io/rst.html>`__ format.

To create HTML documentation run this command from the source directory
where `Makefile` is located:
    .. code-block:: console

        make docs-html

After generation documentation can be opened from a file
`docs/build/html/index.html`.