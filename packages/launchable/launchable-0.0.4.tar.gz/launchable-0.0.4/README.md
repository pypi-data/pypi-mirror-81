# Installation

```shell
git clone https://github.com/launchableinc/launchable-cli
cd launchable-cli
pip install -U .
```

## Set your API token

```shell
export LAUNCHABLE_TOKEN=set_your_token
```

# How to use

### Collect commit

```shell
launchable commit
```

### Collect build

```shell
launchable build --build BUILD_NUMBER --commit REPO_NAME=REPO_GIT_HASH
```