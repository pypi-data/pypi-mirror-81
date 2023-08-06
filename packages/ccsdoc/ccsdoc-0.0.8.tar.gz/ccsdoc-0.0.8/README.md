CCS command documentation helper
================================

[![License][license-badge]][license-web]
[![CI][ci-badge]][ci-web]

List the available commands information such as the name, the level, the type and the description.

[ci-web]: https://github.com/aboucaud/command-doc-generator/actions
[ci-badge]: https://github.com/aboucaud/command-doc-generator/workflows/test%20suite/badge.svg?style=flat
[license-badge]: https://img.shields.io/badge/license-BSD-blue.svg?style=flat
[license-web]: https://choosealicense.com/licenses/bsd-3-clause/

Usage
-----

#### parse

Use the command-line tool `ccsdoc` to list the commands either on a given file or in a directory.

- on a single file
    ```
    ccsdoc parse --path JavaFile.java
    ```
- on a full directory to process recursively all .java files
    ```
    ccsdoc parse --path java_project_dir
    ```

Commands can be output to a CSV file.
```
ccsdoc parse --path JavaFile.java --to javafile_commands.csv
```

#### convert

The CSV table containing the commands can be converted to the desired format using [`pandoc`][pandoc]
```
# e.g. here to Microsoft Word
ccsdoc convert javafile_commands.csv --to docx
```

[pandoc]: https://pandoc.org/


Examples
--------

#### Working example

```bash
$ ccsdoc parse --path SimuEPOSController.java
SimuEPOSController.java:
Command(name=setPosition, type=ACTION, level=ENGINEERING1, desc=For simulator only : Update position with a position given as argument.)
Command(name=checkFault, type=QUERY, level=ENGINEERING1, desc=Check if the Controller is in fault.)
```

#### Missing argument example

```bash
$ ccsdoc parse --path SimuLoaderStandalonePlutoGateway.java
SimuLoaderStandalonePlutoGateway.java:
=> simulation/SimuLoaderStandalonePlutoGateway.java: issue at line 39: Missing command argument 'description'.
```

Installation
------------
```
pip install git+https://github.com/aboucaud/command-doc-generator.git
```

Author
------
Alexandre Boucaud <aboucaud@apc.in2p3.fr>
