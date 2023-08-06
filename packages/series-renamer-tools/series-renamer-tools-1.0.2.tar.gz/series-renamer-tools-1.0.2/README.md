# Series Renamer

## Table of Contents

- [Requirement](#requirement)
- [Installation](#installation)
  - [Installing from Git](#installing-from-git)
- [Usage](#usage)
  - [Options](#options)
  - [YAML Input](#yaml-input)
- [License](#license)

## Requirement

- Python 3.6+

## Installation

### Installing from Git

```sh
sudo python3 setup.py install
```

## Usage

```sh
series-renamers --directory [path/to/target/directory] --prefix 'Series S01 E' [--dry-run]
```

### Options
| Name                | Type      | Description              | Required | Default           |
| ------------------- | --------- | ------------------------ | -------- |-------------------|
| `--directory`, `-d` | `string`  | path to target directory | `false`  | current directory |
| `--prefix`, `-p`    | `string`  | new file name prefix     | `true`   |                   |
| `--dry-run`, `-dr`  | `boolean` | only preview the results | `false`  | `false`           |
