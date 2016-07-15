# Cardinal

Cardinal is software for collecting data about users' file management behavior through their voluntary, remote, and anonymous participation. A GUI, built in Qt5, guides users through participation, presents them with a summary of their results, and returns the anonymized data to the researchers. Data are collected only about those files and folders that users specify, and specified locations can be ignored as well. No identifying data are collected, file and folder names are not stored, and file contents are not accessed.

For the purposes of the first study using Cardinal (read about it here: http://dinneen.research.mcgill.ca), this version collects additional data via text fields and questionnaires, namely: (anonymous) demographic features, technological properties like the OS, installed FM software (using semi-reliable detection), hard drive capacity and use, and the psychological measures of personality style and spatial cognition using the Ten Item Personality Index and Santa Barbara Sense of Direction Scale.

The GUI uses Qt5 and therefore the PyQt5 bindings, and the pycrypto and dropbox API packages are used to encrypt the compressed results files and send them to a specified Dropbox folder. From there, they will need to be retrieved and unencrypted, and any measurements then made.

### Requirements
* Python 3.x
* Qt5
* PyQt5
* pypiwin32 (Win only)
* pycrypto
* dropbox
* scandir (optional but recommended for Python < 3.5)

### Usage
#### Linux

#### OSX (10.8 - 10.11)

#### Windows (XP, 7, 8, and 10 -- may work on others)

### Sample of raw data
The following describes one folder (containing two sub-folders) and one file it contains.
```json
    "1": {
                "c_time": "2015-06-30 18:58:18",
                "children": [
                    "2",
                    "1431",
                ],
                "default": false,
                "depth": 2,
                "file_list": [
                     {
                        "a_time": "2015-07-23 12:27:27",
                        "c_time": "2015-07-23 12:27:26",
                        "extension": "png",
                        "file_id": 915,
                        "file_size": 3213,
                        "full_name_length": 12,
                        "hard_link_duplicate": false,
                        "letters": 4,
                        "m_time": "2015-07-23 12:27:27",
                        "name_duplicate": true,
                        "numbers": 3,
                        "special_chars": 1,
                        "white_spaces": 0
                    }
                ],
                "hard_link_duplicate": false,
                "hidden_children": 0,
                "hidden_files": 6,
                "ignored_children": 0,
                "inaccessible_children": 0,
                "letters": 5,
                "m_time": "2015-06-30 19:01:01",
                "name_duplicate": false,
                "name_length": 10,
                "node_id": "1",
                "numbers": 1,
                "special_chars": 2,
                "symlinks": 0,
                "white_spaces": 2
    }
```
