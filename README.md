# Canadian Ham License Questions flashcard


## Name
Canadian ham radio certification test generator.

## Description
Yes, it's a lot of them out there already but I wanted to practice my programming skill and since I need to test my program I end up practicing the questions also.

Highlights of this version:
- It show progress as you answer questions, both raw correct/wrong as well as percent passed.
- You can run it in "test" mode in which case it only count up the questions done and ends when you done 100 (or hit "q")
- It does show progress based on the last then sessions you done. Progress as to how good you doing in each section.
- You can concentrate on doing just one section

## Installation
It's just a single python 3 program. Download that single file or clone the repo to get started. You also need the test questions.<br>
The test file can be retrieved from <br>
https://ised-isde.canada.ca/site/amateur-radio-operator-certificate-services/en/downloads
   ```
   wget https://apc-cap.ic.gc.ca/datafiles/amat_basic_quest.zip
   unzip -x amat_basic_quest.zip
   ```

## Usage
Just run the program with `--help` to get a list of options.
If you run it without any parameters it will just start showing questions.

## Roadmap
- Download of questions need to be be part of the program by passing "--download" to it.
- Add an option to easily switch between basic and advanced questions

## License
GPL3

## Project status
Currently under development, will possible stop once I got my license.
