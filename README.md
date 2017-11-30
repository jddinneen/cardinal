# Cardinal

Cardinal is software for researchers to use to collect data about study participants' file management through their voluntary, remote, and anonymous participation. The motivations and technical details of the development of Cardinal can be read in detail in Dinneen et al, (2016) Cardinal: Novel software for studying file management behavior. *ASIS&T 2016: Proceedings of the 79th Annual Meeting of the Association for Information Science & Technology, 53*. It was created by Dr. Jesse Dinneen (Victoria University of Wellington) with the assistance of Fabian Odoni (HTW Chur).

## Usage

1. The researcher downloads the source code, modifies it to suit their study, compiles on whichever platforms they want it to run in, and distributes binaries to participants. 

2. The program's GUI, built in Qt5, guides participants through the process, presents them with a summary of their results, and returns the anonymized data to the researchers. Data are collected only about those files and folders that users specify, and specified locations can be ignored as well. No identifying data are collected, file and folder names are not stored, and file contents are not accessed. By default, Cardinal collects additional anonymous data via text fields and questionnaires, namely: (anonymous) demographic features, technological attributes like the OS, hard drive capacity and use, and the psychological measures of personality style and spatial cognition using the Ten Item Personality Index and Santa Barbara Sense of Direction Scale.

3. The default behaviour is to forward the data (upon participant request) via the Dropboc API to the researcher's specified Dropbox folder. Data are encrypted and compressed before being sent. Once received, they will need to be retrieved and decrypted before analyses can be made (e.g., by deserialising the JSON data and iterating over it to make measurements). A sample of raw data is below.

### Requirements
* Windows (XP or newer), Mac OS X, or Linux
* Python 3.x
* Qt5.x
* PyQt5
* python packages: scandir, dropbox, pycrypto, pypiwin32 (Windows only) 

### Sample of collected data
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
