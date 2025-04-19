#!/usr/bin/env python3
#Purpose: Practice python programming and get more motivation to practice HAM questions
#
#The test file can be retrieved from https://ised-isde.canada.ca/site/amateur-radio-operator-certificate-services/en/downloads
#  wget https://apc-cap.ic.gc.ca/datafiles/amat_basic_quest.zip
#  unzip -x amat_basic_quest.zip

import csv
import json
import random
import getopt
import sys
from datetime import datetime

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

INFILE="amat_adv_quest_delim.csv"
PREV_ANSWERS="amat_adv_quest_answers.csv"

INFILE="amat_basic_quest_delim.txt"
PREV_ANSWERS="amat_basic_quest_answers.csv"
PREV_ANSWERS_JSON="amat_basic_quest_answers.json"
QUIZ_RECORD="amat_basic_quest_quiz.json"

VERSION=f"{sys.argv[0]} version 0.1.0"
USAGE = f"Usage: python {sys.argv[0]} [--help] | [--category ?]"

TEST=False

category={}
category['B-001']={"description":"Regulations and Policies"}
category['B-002']={"description":"Operating and Procedures"}
category['B-003']={"description":"Station Assembly, Practice and Safety"}
category['B-004']={"description":"Circuit Components"}
category['B-005']={"description":"Basic Electronics and Theory"}
category['B-006']={"description":"Feedlines and Antenna Systems"}
category['B-007']={"description":"Radio Wave Propagation"}
category['B-008']={"description":"Interference and Suppression"}

def print_cat():
    for cnt,cat in enumerate(category):
        print(f"{cnt+1} => {cat} - {category[cat]['description']}")
    
def get_opt():
    global TEST
    opts, args = getopt.getopt(sys.argv[1:], 'hqVtc:', ['help','question','version','test','category='])
    #print(f"opts={opts},   args={args}")
    catid=""
    for o,a in opts:
        if o in ('-c','--category'):
            if a=="?":
                print_cat()
                exit(0)
            try:
                catno=int(a)
            except ValueError:
                catno=0
            if catno<1 or catno>8:
                print(f"Unknown category: {a}")
                print_cat()
                raise SystemExit(USAGE)
            else:
                catid=list(category.keys())[catno-1]
        elif o in ("-t","--test"):
            TEST=True
            catno=0
        elif o in ("-v","--version"):
                print(VERSION)
        #print(f"o={o},  a={a}")
    return catid

def get_questions(catopt):
    # Question categories:
    global category

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
        if len(category[key]['questions']) == 0:
               continue
        print(f"{key} - {len(category[key]['questions']):3d}; {category[key]['description']}: ")
    #exit(9)
    return (category,all_questions)
    #print(f"lenght={size(reader)}")

def get_prev_answers():
    prev_answers={}
    try:
        with open(PREV_ANSWERS, mode='r') as infile:
            reader = csv.DictReader(infile,delimiter=",")
            for row in reader:
                prev_answers[row['q_id']]={
                    "correct":int(row["correct"]),
                    "wrong":int(row["wrong"]),
                    "skipped":int(row["skipped"])
                    }
                #for x in row.keys():
                #    print(f"x = \"{x}\" - {row[x]}")
                # question={}
                # for q in row.keys():
                #     #print(f"q = \"{q}\" - \"{row[q]}\", q_id=\"{q_id}\"")
                #     question[q]=row[q]
                # all_questions.append(question)
    except FileNotFoundError:
        pass
    #print(f"lenght={len(prev_answers)}")
    #print(all_questions)
    #print(json.dumps(prev_answers,indent=2))
    return prev_answers
    #print(f"lenght={size(reader)}")

def save_answers(answers):
    # "B-006-003-003": {
    #     "correct": 0,
    #     "wrong": 0,
    #     "skipped": 1
    # }
    if not answers:
        return
    with open(PREV_ANSWERS, mode='w') as outfile:
        outfile.write("q_id,correct,wrong,skipped\n")
        for q_id,q_cnt in sorted(answers.items()):
            # print(f"type = {type(q_id)}")
            # print(f"value = {q_id}")
            # print(f"type = {type(q_cnt)}")
            # print(f"value = {q_cnt}")
            # print(q_cnt.keys())
            answer=q_id
            for x in ("correct","wrong","skipped"):
                answer+=","+str(q_cnt[x])
                #print(f"x = \"{x}\" - {q_cnt[x]}")
            outfile.write(answer+"\n")

def save_answers_json(answers):
    if not answers:
        return
    with open(PREV_ANSWERS_JSON, mode='w') as outfile:
        outfile.write(json.dumps(answers))
      
def get_prev_quiz():
    prev_quiz={}
    try:
        with open(QUIZ_RECORD, mode='r') as infile:
            prev_quiz = json.load(infile)
    except FileNotFoundError:
        pass
    print(f"prev quiz lenght={len(prev_quiz)}")
    return prev_quiz
    #print(f"lenght={size(reader)}")

def save_quiz(quiz):
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

def flash_sample(all_questions,prev_answers,prev_quiz,category):
    TOT=0
    CORRECT=0
    WRONG=0
    NOW=datetime.now().strftime("%F %T")
    global TEST

    prev_quiz[NOW]={"questions":{}}
    # 'question_id', 'question_english', 'correct_answer_english', 'incorrect_answer_1_english', 'incorrect_answer_2_english', 'incorrect_answer_3_english'
    print(f"show some questions out of a pool of {len(all_questions)} questions")
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
        if TOT > 100:
            ans="q"
        else:
            ans=""
        # print(f"A1: {all_questions[q_id]['incorrect_answer_1_english']}")
        # print(f"A2: {all_questions[q_id]['incorrect_answer_2_english']}")
        # print(f"A3: {all_questions[q_id]['incorrect_answer_3_english']}")
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
            elif ans == "s":
                print("skipped")
                break

        if ans=="q":
            TOT-=1
            print()
            print(f"Done {TOT} questions")
            print(f" Got {CORRECT} right")
            print(f" Got {WRONG} wrong")
            if CORRECT > 0:
                print(f"That means you got {CORRECT/TOT*100}% right")
            return prev_answers,prev_quiz,prev_quiz[NOW]

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

def show_pct_last(prev_quiz):
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
        #print(f"   quiz no {QCNT} = {quiz}")
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

    # print(f"****************************************************************\n{json.dumps(category_pct,indent=2)}\n****************")
    print()
    print(f"stats from the last {CNT} times")
    for cat in category_pct:
        answers=category_pct[cat]['ans']
        tot=0
        for ans in answers:
            tot+=answers[ans]
        #print(f"{category_pct[cat]['description']}")
        #print(f"{category_pct[cat]['description']} - {tot} of {len(category_pct[cat]['questions'])} questions answered:")
        line=f"{cat[4:]} - {category_pct[cat]['description']:40}  - a questions been answered {tot:3d} times; "
        tail=""
        for ans in answers:
            pct=answers[ans]/tot*100
            if ans=="correct":
                if pct <70:
                    tail=" <<<<<<<<<<<<<<<<"
                elif pct <80:
                    tail=" <<<<"
                elif pct <90:
                    tail=" <<"
            line+=f"{ans} : {answers[ans]:3d} - {pct:3.2f}%, "
        print(line[0:-2],tail)


def show_pct(prev_answers):
    #print(f"prev_answers={json.dumps(prev_answers,indent=2)}")
    #print(f"prev_quiz={prev_answers.keys()}")
    category_pct=category
    for q_id in prev_answers:
        cat=q_id[:5]
        if "ans" not in category_pct[cat]:
            category_pct[cat].update({"ans":{"correct":0,"wrong":0,"skipped":0}})
        for ans in prev_answers[q_id]:
            cnt=category_pct[cat]['ans'][ans]
            category_pct[cat]['ans'].update({ans:cnt+prev_answers[q_id][ans]})
        #print(f"{prev_answers[q_id]}")
    #print(f"prev_answers={json.dumps(category_pct,indent=2)}")
    for cat in category_pct:
        answers=category_pct[cat]['ans']
        tot=0
        for ans in answers:
            tot+=answers[ans]

        #print(f"{category_pct[cat]['description']}")
        #print(f"{category_pct[cat]['description']} - {tot} of {len(category_pct[cat]['questions'])} questions answered:")
        print(f"{category_pct[cat]['description']} - a questions answered {tot} times")
        for ans in answers:
            print(f"    {ans:8}: {answers[ans]:3d} - {answers[ans]/tot*100:3.2f}%")

        # totq=len(category_pct[cat]['questions'])
        # if tot != totq:
        #     print(f"   >>>> cat {cat}, tot={tot}, totq={totq}")
        #     #print(f"\n{json.dumps(category_pct[cat]['questions'],indent=2)}")
        #     #print(f"\n{category_pct[cat]['questions']['B-001-025-004']}")
        #     #print(f"\n{json.dumps(category_pct[cat]['questions']['B-001-025-004'],indent=2)}")
        #     print(f"\n{json.dumps(category_pct[cat],indent=2)}")
        #     exit(8)

def main():
    print("test_sampler starting")
    cat=get_opt()
    (category,questions)=get_questions(cat)
    #print(type(questions))
    #print(type(questions[0]))
    #print(json.dumps(questions[3],indent=2))
    #q="B-004-001-001"
    #print(type(questions[q]))
    #print(json.dumps(questions[q],indent=2))
    #exit(9)
    prev_answers=get_prev_answers()
    prev_quiz=get_prev_quiz()
    show_pct(prev_answers)
    answers,prev_quiz,quiz=flash_sample(questions,prev_answers,prev_quiz,category)
    save_answers(answers)
    save_answers_json(answers)
    save_quiz(prev_quiz)
    #print(f"quiz={json.dumps(quiz,indent=2)}")
    #print(f"prev_quiz={json.dumps(prev_quiz,indent=2)}")
    if len(quiz['questions']) >0:
        show_pct(quiz['questions'])
    #print(f"prev_quiz={json.dumps(quiz,indent=2)}")
    show_pct_last(prev_quiz)

main()
