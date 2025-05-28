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
It's just a single python 3 program. Download that single file or clone the repo to get started.<br>
The test questions will be downloaded the first time the program starts.<br>
They are downloaded from <br>
https://ised-isde.canada.ca/site/amateur-radio-operator-certificate-services/en/downloads
If you want to you can manually download them first with
   ```
   wget https://apc-cap.ic.gc.ca/datafiles/amat_basic_quest.zip
   unzip -x amat_basic_quest.zip
   ```

## Usage
Just run the program with `--help` to get a list of options.
If you run it without any parameters it will just start showing questions.

## Roadmap
- Add an option to easily do a review of questions done

## License
GPL3

## Project status
Currently under development, will possible stop once I got my license.

## Quick demo
$ python3 practice_questions.py --help
HAM radio flash card starting
usage: practice_questions.py [-h] [-V] [-e EXAM] [-t] [-c CATEGORY]

It will allow to practice for the canadian ham radio license test

options:
  -h, --help            show this help message and exit
  -V, --version         show program version
  -e EXAM, --exam EXAM  Exam to run, "1"/"basic" for basic(default), "2"/"adv" for advanced, "3" for basic after 2025-07-15
  -t, --test            run in test mode, that means no righ/wrong after each question or progress is shown
  -c CATEGORY, --category CATEGORY
                        what category of question to focus on, pass "?" for a list

73 de VA3TUE
$ python3 practice_questions.py --exam ?
HAM radio flash card starting
   1:  amateur basic questions until 2025-07-15
   2:  amateur advanced questions
   3:  amateur basic questions after 2025-07-15
$ python3 practice_questions.py --exam 2
HAM radio flash card starting
downloading https://apc-cap.ic.gc.ca/datafiles/amat_adv_quest.zip
Extracting amat_adv_quest_delim.txt
Files extracted successfully
total number of questions found: 549
A-001 -  54; Advanced Theory:
A-002 - 132; Advanced Components and Circuits:
A-003 -  66; Measurements:
A-004 -  44; Power Supplies:
A-005 -  99; Transmitters, Modulation and Processing:
A-006 -  55; Receivers:
A-007 -  99; Feedlines - Matching and Antenna Systems:

Showing questions for "amateur advanced questions" out of a pool of 549 questions. The test randomly picks 50 questions to answer

Question 1 (0/0 NA) - A-007-003-006   (Feedlines - Matching and Antenna Systems)
Question : A quarter-wave stub, for use at 15 MHz, is made from a coaxial cable having a velocity factor of 0.8. Its physical length will be:
1: 12 m (39.4 ft)
2: 8 m (26.2 ft)
3: 4 m (13.1 ft)
4: 7.5 m (24.6 ft)

 <cr> to continue:
