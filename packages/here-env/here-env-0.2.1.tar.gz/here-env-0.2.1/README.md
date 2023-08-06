# here-env

Small helper to create and activate virtual environments.

## Usage

```sh
eval $(here-env)
```

This will create a venv in `$PWD/.venv` or in `$GIT_ROOT/.venv` (if currently
in a Git repository) and activate it.

You can also create a simple `here` shell alias:

```sh
alias here='eval $(here-env)'
```
