# k3project-generator

Generates the basic structure of a multi module python project

Usage:

```
k3project-generator [-h] [-l {GPLv3,APACHE_2_0,MIT,None}]
                           [-d TARGET_DIRECTORY] [-v] [-vv]
                           project_name
```

Example:

```sh
k3project-generator hello-world-project
```

This will create a project with the following layout defined in the next chapter (nameofproject replaced with hello_world_project) and with a MIT license.  

**Note:**
* Valid project names consist of caracters a-z, 0-9, _ & -
* - will be replaced by _ in the root package name
* a valid test is created which can be run with pytest. Readme within the generated tests directory will contain more information.
* a main script (called \<project_name\>-cli) is defined that can be called when the project is installed. e.g.: hello-world-project-cli


## Standard python multi module project layout

```
README.md
LICENSE
setup.py
nameofproject/__init__.py
nameofproject/...
docs/
tests/
```

## Optional single module project layout

```
README.md
LICENSE
setup.py
nameofproject.py
docs/
tests/
```

## Referneces

[https://docs.python-guide.org/writing/structure/](https://docs.python-guide.org/writing/structure/)  
[https://packaging.python.org/tutorials/packaging-projects](https://packaging.python.org/tutorials/packaging-projects)
