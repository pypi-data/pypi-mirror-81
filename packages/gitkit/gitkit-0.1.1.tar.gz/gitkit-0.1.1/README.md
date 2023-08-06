# gitkit
A tool for analyzing and synchronizing git repositories with github

## Installation

`python3 -m pip install gitkit --upgrade`

**Test version**

`python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps gitkit --upgrade`

## Usage
`gitkit [OPTIONS] COMMAND [ARGS]...`

### Options:

| Option           | Typ  | Description |
| ---------------- | ---- | ----------- |
| -t, --target-dir | TEXT | The local target/source path
| -u, --user       | TEXT | The github username
| -p, --password   | TEXT | The github password
| -l, --list       |      | Print results. Does not execute any command.
| --help           |      | Show this message and exit.

### Commands:

| Command | Description |
| ------- | ----------- |
| clone   | Clone repositories |
| commit  | Commit repositories |
| find    | Search local repositories |
| pull    | Pull repositories |
| push    | Push repositories |

| Description | Command |
| ----------- | ------- |
| Help | `gitkit --help`    |
| Clone all repositories.   | `gitkit -u <USERNAME> -p <PASSWORD> -t /home/pullrich/src/github clone` |
| Pull all repositories.    | `gitkit -u <USERNAME> -p <PASSWORD> -t /home/pullrich/src/github pull` |
| Push all repositories.    | `gitkit -u <USERNAME> -p <PASSWORD> -t /home/pullrich/src/github push` |
| Find all repositories     | `gitkit -t /home/pullrich/src/github find` |
| Find all repositories     | `cd /your/path/ && gitkit find` |
| Find dirty repositories   | `gitkit -t /home/pullrich/src/github find -d` |
| Find private repositories | `gitkit -t /home/pullrich/src/github find -p` |
| Find private dirty repositories | `gitkit -t /home/pullrich/src/github find -pd` |
| Find public repositories  | `gitkit -t /home/pullrich/src/github find -np` |
| Find forked repositories  | `gitkit -t /home/pullrich/src/github find -f` |
| Find owned repositories   | `gitkit -t /home/pullrich/src/github find -o` |
| Find ahead remote repositories | `gitkit -t /home/pullrich/src/github find -a` |
| Find behind remote repositories | `gitkit -t /home/pullrich/src/github find -a` |
| Find not owned repositories |`gitkit -u dotupNET -t /home/pullrich/src/github/ -l find -no`|


> Environment variable for user, password and target available
>
> `user=XYZ`
> `password=XYZ`
> `target-dir=/tmp/github`

-u <USERNAME> -p <PASSWORD> -t /home/pullrich/src/github -l push
        // "clone",
        // "--group",
        // "forks",
        // "--group",
        // "owner"

https://github.com/dotupNET/gitkit
