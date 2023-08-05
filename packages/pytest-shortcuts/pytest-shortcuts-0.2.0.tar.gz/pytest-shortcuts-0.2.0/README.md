# pytest-shortcuts

Expand command-line shortcuts listed in pytest configuration

This [pytest](https://github.com/pytest-dev/pytest) plugin was generated with [Cookiecutter](https://github.com/audreyr/cookiecutter) along with @hackebrot's [cookiecutter-pytest-plugin](https://github.com/pytest-dev/cookiecutter-pytest-plugin) template.

## Getting Started

Install using your favourite python package manager:

```no-highlight
$ pip install pytest-shortcuts
```

Add some shortcuts to your pytest configuration:

```no-highlight
[pytest]
shortcuts =
    --live: -m "live and not slow"
    --slow: -m "live and slow"
    --offline: --disable-socket -m "not live"
```

Now when you run your tests with eg `--live`, it will be as if you provided `-m "live and not slow"`.


## Bonus: including dotenv files

For each shortcut, you can also define a dotenv file to load with custom configuration:

```no-highlight
[pytest]
shortcuts =
    --live: -m "live and not slow" --envfile=.live.env
    --slow: -m "live and slow"
```

> Note that this dotenv file loads the environment very early, but any pytest-plugins
> will have already been imported by then. Any plugin that relies on an environment
> variable during module import (and not eg at runtime) may not see values loaded from
> this file.


## License

Distributed under the terms of the [BSD-3 license](http://opensource.org/licenses/BSD-3-Clause), "pytest-shortcuts" is free and open source software


  [Cookiecutter]: https://github.com/audreyr/cookiecutter
  [@hackebrot]: https://github.com/hackebrot
  [MIT]: http://opensource.org/licenses/MIT
  [BSD-3]: http://opensource.org/licenses/BSD-3-Clause
  [GNU GPL v3.0]: http://www.gnu.org/licenses/gpl-3.0.txt
  [Apache Software License 2.0]: http://www.apache.org/licenses/LICENSE-2.0
  [cookiecutter-pytest-plugin]: https://github.com/pytest-dev/cookiecutter-pytest-plugin
  [file an issue]: https://github.com/willhardy/pytest-shortcuts/issues
  [pytest]: https://github.com/pytest-dev/pytest
  [tox]: https://tox.readthedocs.io/en/latest/
  [pip]: https://pypi.org/project/pip/
  [PyPI]: https://pypi.org/project
