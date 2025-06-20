#!/usr/bin/env python3
#Purpose: Practice python programming and get more motivation to practice HAM questions
#
#License: GPL3
#
#The test file can be retrieved from https://ised-isde.canada.ca/site/amateur-radio-operator-certificate-services/en/downloads
#  wget https://apc-cap.ic.gc.ca/datafiles/amat_basic_quest.zip
#  unzip -x amat_basic_quest.zip

import csv
import json
import random
import argparse
import os
import sys
import requests
from datetime import datetime
from zipfile import ZipFile
from io import BytesIO

# Each record has the following data, separated by ";"

# Question ID
# English Question
# Correct English Answer
# Incorrect English Answer 1
# Incorrect English Answer 2
# Incorrect English Answer 3
# French Question
# Correct French Answer
# Incorrect French Answer 1
# Incorrect French Answer 2
# Incorrect French Answer 3

BASE_NAMES={
    1:{
        "description":"amateur basic questions until 2025-07-15",
        "base_name":"amat_basic_quest",
        "url":"https://apc-cap.ic.gc.ca/datafiles/amat_basic_quest.zip",
        "pass":100
    },
    2:{
        "description":"amateur advanced questions",
        "base_name":"amat_adv_quest",
        "url":"https://apc-cap.ic.gc.ca/datafiles/amat_adv_quest.zip",
        "pass":50
    },
    3:{
        "description":"amateur basic questions after 2025-07-15",
        "base_name":"amat_basic_quest_2025-07-15",
        #"url":"https://apc-cap.ic.gc.ca/datafiles/amat_basic_quest_2025-07-15.zip"
        "url":"https://ised-isde.canada.ca/site/amateur-radio-operator-certificate-services/sites/default/files/documents/amat_basic_quest_2025-07-15.zip",
        "pass":100,
        "quiz_name":"amat_basic_quest_delim.txt"
    }
}

VERSION=f"{sys.argv[0]} version 0.3.1"
USAGE = f"Usage: python {sys.argv[0]} [--help] | [--category ?]"
TEST=False

################
def prep_for_quiz(quizno):
    global QUIZNO,BASE_NAME,URL,INFILE,PREV_ANSWERS,QUIZ_RECORD,category,MAXQ

    QUIZNO=quizno
    BASE_NAME=BASE_NAMES[QUIZNO]['base_name']
    URL=BASE_NAMES[QUIZNO]['url']

    INFILE=BASE_NAME+"_delim.txt"
    PREV_ANSWERS=BASE_NAME+"_answers.json"
    QUIZ_RECORD=BASE_NAME+"_quiz.json"

    category={}
    MAXQ=BASE_NAMES[QUIZNO]['pass']
    if "basic" in BASE_NAME:
        #basic test
        category['B-001']={"description":"Regulations and Policies"}
        category['B-002']={"description":"Operating and Procedures"}
        category['B-003']={"description":"Station Assembly, Practice and Safety"}
        category['B-004']={"description":"Circuit Components"}
        category['B-005']={"description":"Basic Electronics and Theory"}
        category['B-006']={"description":"Feedlines and Antenna Systems"}
        category['B-007']={"description":"Radio Wave Propagation"}
        category['B-008']={"description":"Interference and Suppression"}
    elif "adv" in BASE_NAME:
        #advanced test
        category['A-001']={"description":"Advanced Theory"}
        category['A-002']={"description":"Advanced Components and Circuits"}
        category['A-003']={"description":"Measurements"}
        category['A-004']={"description":"Power Supplies"}
        category['A-005']={"description":"Transmitters, Modulation and Processing"}
        category['A-006']={"description":"Receivers"}
        category['A-007']={"description":"Feedlines - Matching and Antenna Systems"}
    else:
        print(f"ERROR: don't know if {BASE_NAME} is basic or advanced")
        exit(15)

################
def print_cat():
    ''' print the categories '''
    for cnt,cat in enumerate(category):
        print(f"{cnt+1} => {cat} - {category[cat]['description']}")

################
# def usage():
#     print("usage: practice_questions.py [-h|--help] [-V|--version] [-t|--test] [-c|--category #]")
#     print(" -t|--test  means it will not show progress or if you got it right or wrong, only how many questions you answerd. When 100 questions are done it shows the result.")
#     print(" -c|--category  focus on one category")

################
def parse_args():
    '''
    https://docs.python.org/3/library/argparse.html
    parse command line arguments with argparse (instead of getopt)
    '''
    global TEST
    catid=""

    parser = argparse.ArgumentParser(
        prog=f"{sys.argv[0]}",
        description='It will allow to practice for the canadian ham radio license test',
        epilog='73 de VA3TUE'
    )
    #parser.add_argument('-v', '--verbose',  action='store_true',help='be more versbose in outputs')  # on/off flag
    #parser.add_argument('-h','--help','-?',action='store_true',help='this help')
    parser.add_argument('-V','--version',action='version',help='show program version',version=VERSION)
    parser.add_argument('-e','--exam',help='Exam to run, "1"/"basic" for basic(default), "2"/"adv" for advanced, "3" for basic after 2025-07-15',default="1")
    parser.add_argument('-t','--test',action='store_true',help='run in test mode, that means no  righ/wrong after each question or progress is shown')
    parser.add_argument('-c','--category',help="what category of question to focus on, pass \"?\" for a list")
    args = parser.parse_args()
    if args.test:
        TEST=True
        catno=0
    # args.exam has a default of "1"
    exam=args.exam
    if args.exam=="basic":
        exam="1"
    elif args.exam=="adv" or args.exam=="advanced":
        exam="2"
    if exam.isnumeric():
        exam=int(exam)
    if exam not in BASE_NAMES:
        if exam != "?":
            print(f"unknown exam \"{exam}\", only know")
        for e in BASE_NAMES:
            print(f"   {e}:  {BASE_NAMES[e]['description']}")
        sys.exit(8)

    if args.category:
        cat=args.category
        if cat=="?":
            prep_for_quiz(exam)
            print_cat()
            exit(0)
        try:
            catno=int(cat)
        except ValueError:
            catno=0
        if catno<1 or catno>len(category.keys()):
            print(f"Unknown category: >{cat}<")
            print_cat()
            raise SystemExit(USAGE)
        else:
            catid=list(category.keys())[catno-1]

    prep_for_quiz(exam)

    return catid

################
def download_quiz():
    print(f"downloading {BASE_NAMES[QUIZNO]['url']}")
    response=requests.get(BASE_NAMES[QUIZNO]['url'])
    #print (f"received {len(response.content)} bytes")
    if response.status_code == 200:
        FILENAME=BASE_NAMES[QUIZNO]['base_name']+"_delim.txt"
        if "quiz_name" in BASE_NAMES[QUIZNO]:
            QUIZ_NAME=BASE_NAMES[QUIZNO]['quiz_name']
        else:
            QUIZ_NAME=FILENAME
        # Create a ZipFile object from the response content
        with ZipFile(BytesIO(response.content)) as zip_file:
            # Extract the quiz to current directory
            print(f"Extracting {QUIZ_NAME}")
            zip_file.extract(QUIZ_NAME)
            if QUIZ_NAME != FILENAME:
                os.rename(QUIZ_NAME,FILENAME)
        print("Files extracted successfully")
    else:
        print(f"Failed to download file: {response.status_code}")
        exit(9)

################
def get_questions(catopt):
    ''' read in all questions '''
    # Question categories:
    global category

    if not os.path.isfile(INFILE):
        download_quiz()

    all_questions={}
    with open(INFILE, mode='r') as infile:
        reader = csv.DictReader(infile,delimiter=";")
        for row in reader:
            #print(row.keys())
            # for x in row.keys():
            #     print(f"x = \"{x}\" - {row[x]}")
            question={}
            for q in row.keys():
                #print(f"q = \"{q}\" - \"{row[q]}\"")
                key=q.strip()
                question[key]=row[q]
            #print(f"\nquestion={question}")
            if not question.get('question_id'):
                print("Missing question id")
                print(row)
                exit(88)
            cat=question['question_id'][:5]
            if 'questions' not in category[cat]:
                category[cat]['questions']=[]
            if catopt and not question['question_id'].startswith(catopt):
                continue
            category[cat]['questions'].append(question['question_id'])
            all_questions[question['question_id']]=question

    print(f"total number of questions found: {len(all_questions)}")
    #print(all_questions)
    for key in category:
        if 'questions' not in category[key]:
            continue
        if len(category[key]['questions']) == 0:
               continue
        print(f"{key} - {len(category[key]['questions']):3d}; {category[key]['description']}: ")
    #exit(9)
    return (category,all_questions)
    #print(f"lenght={size(reader)}")

################
def get_prev_answers():
    ''' read all previous answers for this test '''
    ''' should be replaced with get_prev_quiz() '''
    prev_answers={}
    try:
        with open(PREV_ANSWERS, mode='r') as infile:
            prev_answers=json.load(infile)
    except FileNotFoundError:
        pass
    return prev_answers

################
def save_answers(answers):
    ''' save the answers given '''
    # "B-006-003-003": {
    #     "correct": 0,
    #     "wrong": 0,
    #     "skipped": 1
    # }
    if not answers:
        return
    with open(PREV_ANSWERS, mode='w') as outfile:
        outfile.write(json.dumps(answers))
      
################
def get_prev_quiz():
    ''' read in each run done before '''
    ''' this should be the only way needed '''
    prev_quiz={}
    try:
        with open(QUIZ_RECORD, mode='r') as infile:
            prev_quiz = json.load(infile)
    except FileNotFoundError:
        pass
    #print(f"prev quiz lenght={len(prev_quiz)}")
    return prev_quiz
    #print(f"lenght={size(reader)}")

################
def save_quiz(quiz):
    ''' Save the quiz done '''
    # "B-006-003-003": {
    #     "correct": 0,
    #     "wrong": 0,
    #     "skipped": 1
    # }

    # print ("**************** saving quiz")
    # print (f" Len quiz = {len(quiz)}")

    if not quiz:
        return

    for q in sorted(quiz.keys()):
        # print (f" Len q = {len(q)}, q = {q}")
        # print (f" Len questions = {len(quiz[q]['questions'])}, questions = {quiz[q]['questions']}")
        # print (f" quiz[q] = {quiz[q]}")
        if len(quiz[q]['questions']) <1:
            quiz.pop(q)

    with open(QUIZ_RECORD, mode='w') as outfile:
        outfile.write(json.dumps(quiz))

################
def flash_sample(all_questions,prev_answers,prev_quiz,category):
    ''' show the questions one by one and if not test mode, show right/wrong and progress after each question '''
    TOT=0
    CORRECT=0
    WRONG=0
    NOW=datetime.now().strftime("%F %T")
    global TEST

    prev_quiz[NOW]={"questions":{}}
    # 'question_id', 'question_english', 'correct_answer_english', 'incorrect_answer_1_english', 'incorrect_answer_2_english', 'incorrect_answer_3_english'
    print(f"\nShowing questions for \"{BASE_NAMES[QUIZNO]['description']}\" out of a pool of {len(all_questions)} questions. The test randomly picks {MAXQ} questions to answer")
    random.seed()
    questions=list(all_questions.keys())
    random.shuffle(questions)
    # print(f"questions type = {type(questions)}")
    # print(f"questions: {questions}")
    #while True:
    for q_id in questions:
        print()
        # print(f">>>>>>> type={type(q_id)}, {len(all_questions)}")
        # print(f">>>>>>> {q_id}")
        # print(f">>>>>>> {all_questions[q_id]['question_id']}")
        # print(json.dumps(all_questions[q_id],indent=2))
        PCT="NA"
        if TOT>0:
            if CORRECT>0:
                PCT=f"{CORRECT/TOT*100:3.2f}%"
            elif WRONG>0:
                PCT=f"{100-WRONG/TOT*100:3.2f}%"
        TOT+=1
        if TOT > MAXQ:
            TOT-=1
            break
        ans=""
        a=[]
        a.append(all_questions[q_id]['correct_answer_english'])
        a.append(all_questions[q_id]['incorrect_answer_1_english'])
        a.append(all_questions[q_id]['incorrect_answer_2_english'])
        a.append(all_questions[q_id]['incorrect_answer_3_english'])
        random.shuffle(a)
        OPTIONS=""
        for cnt,i in enumerate(a,1):
            OPTIONS+=f"{cnt}: {i}\n"

        while ans not in ('1','2','3','4','q','s','t','?'):
            if TEST:
                PROGRESS=""
            else:
                PROGRESS=f" ({CORRECT}/{WRONG} {PCT})"

            print(f"Question {TOT}{PROGRESS} - {q_id}   ({category[q_id[:5]]['description']})")
            print(f"Question : {all_questions[q_id]['question_english']}")
            print(OPTIONS)

            ans=input(f" <cr> to continue: ")
                
            if ans == "t":
                TEST=not TEST
                ans=""
            elif ans == "s":
                print("skipped")
                break
            elif ans in ('1','2','3','4','q','s'):
                break
            elif ans:
                print('press')
                print('  "q" to quit')
                print('  "s" to skip')
                print('  "t" for test mode (no info on right/wrong)')
                if ans != "?":
                    print('  "?" for help')
                ans=""

        if ans=="q":
            TOT-=1
            break

        if q_id not in prev_answers:
            prev_answers[q_id]={
                'correct':0,
                'wrong':0,
                'skipped':0
            }
        if q_id not in prev_quiz[NOW]:
            prev_quiz[NOW]["questions"].update({q_id:{
                'correct':0,
                'wrong':0,
                'skipped':0
            }})

        try:
            ans=int(ans)
        except ValueError:
            ans=0
        if ans >0 and ans <5:
            if a[int(ans)-1]==all_questions[q_id]['correct_answer_english']:
                if not TEST:
                    print("Correct")
                CORRECT+=1
                prev_answers[q_id]['correct']+=1
                prev_quiz[NOW]["questions"][q_id]["correct"]+=1
                continue
            else:
                WRONG+=1
                prev_answers[q_id]['wrong']+=1
                prev_quiz[NOW]["questions"][q_id]["wrong"]+=1
                if not TEST:
                    print("!!!!!!!!!!!!!!!! INCORRECT !!!!!!!!!!!!!!!!")
        else:
            WRONG+=1
            prev_answers[q_id]['skipped']+=1
            prev_quiz[NOW]["questions"][q_id]["skipped"]+=1

        if not TEST:
            print(f"     A: {all_questions[q_id]['correct_answer_english']}")
        #print(json.dumps(prev_answers,indent=2))
        #print(f"{json.dumps(prev_quiz,indent=2)}")

    #"q" selected or All questions done
    print()
    print(f"Done {TOT} questions")
    print(f" Got {CORRECT} right")
    print(f" Got {WRONG} wrong")
    if CORRECT > 0:
        print(f"That means you got {CORRECT/TOT*100:6.2f}% right")
    return prev_answers,prev_quiz,prev_quiz[NOW]

################
def show_pct_last(prev_quiz):
    ''' show percentage of right/wrong of the last {QCNT} quiz taken - to hint about progress '''
    TOT=0
    CORRECT=0
    WRONG=0
    QCNT=10
    category_pct={}
    for cat in category:
        category_pct[cat]={"description":category[cat]['description']}
    CNT=0
    for test_time in sorted(prev_quiz.keys(), reverse = True):
        #print(f" test_time = {test_time}")
        quiz=prev_quiz[test_time]['questions']
        #print(f"   quiz no {CNT} = {json.dumps(quiz,indent=2)}")
        for q_id in quiz:
            cat=q_id[:5]
            if "ans" not in category_pct[cat]:
                category_pct[cat].update({"ans":{"correct":0,"wrong":0,"skipped":0}})
            for ans in quiz[q_id]:
                cnt=category_pct[cat]['ans'][ans]
                category_pct[cat]['ans'].update({ans:cnt+quiz[q_id][ans]})
        CNT+=1
        if CNT==QCNT:
            break
    #print(f"****************************************************************\n{json.dumps(category_pct,indent=2)}\n****************")
    print()
    print(f"Stats from the last {CNT} times")
    show_result(category_pct)

################
def show_result(category_pct):
    ''' show all questions answered so far'''
    for cat in category_pct:
        if 'ans' not in category_pct[cat]:
            continue
        answers=category_pct[cat]['ans']
        tot=0
        for ans in answers:
            tot+=answers[ans]
        #print(f"{category_pct[cat]['description']}")
        #print(f"{category_pct[cat]}")
        #print(f"{category_pct[cat]['ans']} = tot {tot}")
        #print(f"{category_pct[cat]['description']} - {tot} of {len(category_pct[cat]['ans'])} questions answered:")
        #print(f"{category_pct[cat]['description']} - {tot} of {len(answers[ans])} questions answered:")
        line=f"{cat[4:]} - {category_pct[cat]['description']:37}  - a questions been answered {tot:3d} times; "
        tail=""
        for ans in answers:
            pct=answers[ans]/tot*100
            #print(f"  ans={ans} - pct={pct}")
            if ans=="correct":
                if pct <70:
                    tail=" <<<<<<<< !!!!!!!!!!!!!!!!"
                elif pct <80:
                    tail=" <<<<<<<<"
                elif pct <90:
                    tail=" <<"
            line+=f"{ans} : {answers[ans]:3d} - {pct:6.2f}%, "
        print(line[0:-2],tail)


################
def show_pct(prev_answers):
    ''' show pct of all questions taken'''
    #print(f"prev_answers={json.dumps(prev_answers,indent=2)}")
    #print(f"prev_quiz={prev_answers.keys()}")
    category_pct=category
    if len(prev_answers) == 0:
        return
    for q_id in prev_answers:
        cat=q_id[:5]
        if "ans" not in category_pct[cat]:
            category_pct[cat].update({"ans":{"correct":0,"wrong":0,"skipped":0}})
        for ans in prev_answers[q_id]:
            cnt=category_pct[cat]['ans'][ans]
            category_pct[cat]['ans'].update({ans:cnt+prev_answers[q_id][ans]})
        #print(f"{prev_answers[q_id]}")
    #print(f"category_pct={json.dumps(category_pct,indent=2)}")
    #print(json.dumps(category_pct[cat],indent=2)
    print("\nStats from all rounds:")
    show_result(category_pct)

################
def main():
    ''' main function '''

    print("HAM radio flash card starting")
    cat=parse_args()
    (category,questions)=get_questions(cat)
    #print(type(questions))
    #print(type(questions[0]))
    #print(json.dumps(questions,indent=2))
    #q="B-004-001-001"
    #print(type(questions[q]))
    #print(json.dumps(questions[q],indent=2))
    #exit(9)
    prev_answers=get_prev_answers()
    prev_quiz=get_prev_quiz()
    show_pct(prev_answers)
    answers,prev_quiz,quiz=flash_sample(questions,prev_answers,prev_quiz,category)
    save_answers(answers)
    #save_answers_json(answers)
    save_quiz(prev_quiz)
    #print(f"quiz={json.dumps(quiz,indent=2)}")
    #print(f"prev_quiz={json.dumps(prev_quiz,indent=2)}")
    if len(quiz['questions']) >0:
        show_pct(quiz['questions'])
    #print(f"prev_quiz={json.dumps(quiz,indent=2)}")
    show_pct_last(prev_quiz)

main()
