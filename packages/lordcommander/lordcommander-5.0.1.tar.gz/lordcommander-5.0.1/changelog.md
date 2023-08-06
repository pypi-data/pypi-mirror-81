# LordCommander

Changelog
-----

#### Version 5.x

- Yep, LordCommander is now a standalone python package which can be installed using **pip**. 🐉 (v5.0.0)
- Instead of saving shelve module inside the package directory (`.files`), it now uses user data folder. (v5.0.0)
- Renamed module `lordcommander` to `commander` as the main package is named LordCommander. (v5.0.0)
- `_create_data_dir()` and `_read_data()` methods are removed from `LordCommander` class and rewritten as independent functions. (v5.0.0)
- The shelve module to store data now can be passed from outside of the `LordCommander` class via constructor, which helps changing module for testing. (v5.0.0)
- Tests are added, a debt has been paid. More to go. (v5.0.0)
- Removed `lc version` command. (v5.0.1)

#### Version 4.x

- Now one instance of LordCommander can handle multiple projects. 🤹 (v4.0)
- Added new project module to handle project related tasks. (v4.0)
- Added feature to dump data to JSON file and restore from previous dumped files. 🗄 (v4.0)
- Added custom exception module. (v4.0)
- Bug fixes and performance improvements. (v4.0)
- Minor fixes. (v4.0.1)
- Searching for a directory/instance now also shows the index. (v4.1.0)
- Specific directory/instance now can be excluded during execution. See [Running Commands](README.md#exclude-directoryinstance-from-execution) section. (v4.1.0)
- Project root is now shown beside project name. 📂 (v4.1.1)
- Added a `requirements.txt` for using without `Pipenv`. (v4.1.1)
- Added option to see application version. (v4.1.1)
- Minor fixes and code refactoring. (v4.1.1)
- Fixed color contrast for light terminal color scheme. 🌈 (v4.1.2)
- New option to run command for specific directories/instances only.🏷 See [Running Commands](README.md#run-only-for-specified-directories) section. (v4.2.0)
- Listing instances now shows indices also. (v4.2.0)
- Some code style and documentation update. (v4.2.1)
- Set a custom name for a project. See [Adding New Project](README.md#add-new-project) section. 🗃️ (v4.2.2) 
- Ability to rename a project. (v4.2.3)

#### Version 3.x

- Entirely rewritten main functionalities using [Python Fire](https://github.com/google/python-fire). 🔥
- Added feature to throttle the execution. ✈️
- Added feature to remove multiple directories at once.
- Added feature to search for a directory in the list and see total number of directories.
- Now shows number of successful and failed runs at the end. ✔️ ❌
- `list` command has been changed to `view`. Also `sort` will be used instead of `alpha`. 
- Now asks for confirmation when clearing entire list.
- Improved program architecture and code structure.
- Improved visual feedback.
- Removed credential module.
- Installs dependencies and runs with Pipenv rather than Pip.

#### Version 2.0

- Rewritten modules.
- Updated code structure.

#### Version 1.1

- Added alphabetical sorting for directory list.
- Added colored output to distinguish between errors, infos, warnings, and success messages.
- Polished and more clear output.

#### Version 1.0

- Initial release.
