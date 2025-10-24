import os
import json
import time
import matplotlib.pyplot as plt
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

def get_model_info(model_type):
    # """Get model name for display purposes"""
    if model_type == "gemini":
        return os.environ.get('MLC_GEMINI_MODEL', 'models/gemini-2.5-flash')
    elif model_type == "openai":
        return os.environ.get('MLC_OPENAI_MODEL', 'gpt-4o')
    elif model_type == "groq":
        return os.environ.get('MLC_GROQ_MODEL', 'llama-3.3-70b-versatile')
    else:
        return "unknown"


def initialize_model(model_type):
    # Initialize the appropriate model based on type
    if model_type == "gemini":
        import google.generativeai as genai

        api_key = os.environ.get('GEMINI_API_KEY')
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY not set in environment or .env file!")
        
        genai.configure(api_key=api_key)

        model_name = os.environ.get('MLC_GEMINI_MODEL', 'models/gemini-2.5-flash')

        return genai.GenerativeModel(model_name)
    
    elif model_type == "openai":
        from openai import OpenAI

        api_key = os.environ.get('OPENAI_API_KEY')
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY not set in environment or .env file!")
        
        return OpenAI(api_key=api_key)
    
    elif model_type == "groq":
        from groq import Groq

        api_key = os.environ.get('GROQ_API_KEY')
        if not api_key:
            raise RuntimeError("GROQ_API_KEY not set in environment or .env file!")
        
        return Groq(api_key=api_key)
    else:
        raise ValueError("Invalid model type. Choose from 'gemini', 'openai', or 'groq'.")
    

def ask_model(question, options_dict, model_type, model_instance, q_type):
    options_text = "\n".join([f"{k}. {v}" for k, v in options_dict.items()]) if options_dict else ""

    if q_type == "MCQ":
        prompt = f""""Assume you are an expert in Computer Science and Engineering fundamentals, especially the subjects typically covered in a Bachelor's degree in Computer Science like:
        Data Structures, Algorithms, Operating Systems, Computer Networks, Databases, Theory of Computation, Digital Logic, Computer Architecture, Compiler Design, Discrete Mathematics, Linear Algebra, Probability, and Genral Aptitude.

        Answer the following question based on your deep subject knowledge. Do not give explanation, just the final answer.
        Solve the following multiple choice question carefully.

        Question: {question}

        Options:
        {options_text}

        Choose the **one correct option** among A, B, C, or D.
        Respond with only the **option letter** (A, B, C, or D). Do **not** provide any explanation."""
    
    elif q_type == "MSQ":
        prompt = f"""Assume you are an expert in Computer Science and Engineering fundamentals, especially the subjects typically covered in a Bachelor's degree in Computer Science like:
        Data Structures, Algorithms, Operating Systems, Computer Networks, Databases, Theory of Computation, Digital Logic, Computer Architecture, Compiler Design, Discrete Mathematics, Linear Algebra, Probability and Genral Aptitude.

        Answer the following question based on your deep subject knowledge. Do not give explanation, just the final answer.
        Solve the following multiple select question carefully.

        Question: {question}

        Options:
        {options_text}

        Choose **all correct options** from A, B, C, or D. There may be more than one correct answer.

        Respond using **only the letters of correct options**, separated **strictly by semicolons (;)**, and **no spaces**.
        For example: A;C or B;C;D
        Do **not** provide any explanation."""

    elif q_type == "NAT":
        prompt = f"""Assume you are an expert in Computer Science and Engineering fundamentals, especially the subjects typically covered in a Bachelor's degree in Computer Science like:
        Data Structures, Algorithms, Operating Systems, Computer Networks, Databases, Theory of Computation, Digital Logic, Computer Architecture, Compiler Design, Discrete Mathematics, Linear Algebra, Probability and Genral Aptitude.

        Answer the following question based on your deep subject knowledge. Do not give explanation, just the final answer. If the question allows decimals, round the answer to **1 or 2 decimal places** as appropriate.
        Example: 4 or 1.8 or 23.67
        Solve the following numerical answer type (NAT) question carefully and confidentally. Do not ask for clarification or provide any explanation.

        Question: {question}

        Provide **only the final numeric answer** with **no units and no explanation**."""

    else:
        raise ValueError("Invalid question type. Choose from 'MCQ', 'MSQ', or 'NAT'.")
    

    if model_type == "gemini":
        response = model_instance.generate_content(prompt)
        answer = response.text.strip().upper()

    elif model_type == "openai":
        response = model_instance.chat.completions.create(
            model=os.environ.get('MLC_OPENAI_MODEL', 'gpt-4o'),
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=50,
            temperature=0
        )
        answer = response.choices[0].message.content.strip().upper()

    elif model_type == "groq":
        response = model_instance.chat.completions.create(
            model=os.environ.get('MLC_GROQ_MODEL', 'llama-3.3-70b-versatile'),
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=50,
            temperature=0
        )
        answer = response.choices[0].message.content.strip().upper()
    else:
        raise ValueError("Invalid model type. Choose from 'gemini', 'openai', or 'groq'.")
    

    # Normalize MSQ answers
    if q_type == "MSQ":
        answer = answer.replace(",", ";").replace(" ", "")
        if all(c in "ABCD;" for c in answer) and ";" not in answer and len(answer) > 1:
            answer = ";".join(answer)

    return answer


def get_rate_limits(model_type):
    if model_type == "gemini":
        if(os.environ.get('MLC_GEMINI_MODEL') == 'models/gemini-2.5-pro'):
            return {"batch_size":3, "batch_sleep": 60}
        else:
            return {"batch_size": 6, "batch_sleep": 30}
        
    elif model_type == "openai":
        return {"batch_size": 10, "batch_sleep": 60}
    
    else:
        return {"batch_size": 35, "batch_sleep": 60}


def modelProcess(i):
    env = i['env']
    marks = 0
    marksObtained = 0
    negativeMarks = 0
    mcqCorrect = 0
    mcqWrong = 0
    msqCorrect = 0
    msqWrong = 0
    natCorrect = 0
    natWrong = 0
    totalMarks = 0
    total_sleep_time = 0
    process_start = time.time()
    
    # Determine model type from environment variable
    model_type = env.get('MLC_MODEL_TYPE', 'gemini').lower()
    
    # Initialize the appropriate model
    model_instance = initialize_model(model_type)
    model_name = get_model_info(model_type)
    rate_limits = get_rate_limits(model_type)
    
    print("********************************************************************************************************************************")
    print(f"Model type: {model_type}")
    print(f"Model name: {model_name}")
    print(f"Question url: {env.get('MLC_GATE_QUESTION_PDF_URL', 'https://github.com/user-attachments/files/20423322/CS25set2-questionPaper.pdf')}")

    # Load questions
    questions_file = os.path.expanduser(env.get('MLC_GATE_OUTPUT_JSON_PATH', '~/MLC/repos/local/cache/gate-exam-data/output.json'))
    with open(os.path.expanduser(questions_file), 'r') as f:
       questions = json.load(f)

    results = []
    cnt = 0
    print("------------------------------------------------------------------------------------------------------------------------------------")
    
    for q in questions:
        print(f"Processing Q{q['question_number']}..")
        
        model_answer = ask_model(q["question"], q["options"], model_type, model_instance, q["type"])
        
        if isinstance(q["answer"], list):
            correct_answer = ";".join([ans.strip().upper() for ans in q["answer"]])  # Join MSQ answers with ';'
        else:
            correct_answer = q["answer"].strip().upper()  # Handle MCQ/NAT answers

        # Evaluate Model's Answer
        if q["type"] == "NAT" and isinstance(q["answer"], str) and "TO" in q["answer"].upper():
            # Handle NAT range answers like "0.5 TO 0.6"
            try:
                a, b = [float(x.strip()) for x in q["answer"].upper().split("TO")]
                try:
                    model_ans_float = float(model_answer)
                    is_correct = a <= model_ans_float <= b
                except ValueError:
                    print(f"Model answer '{model_answer}' could not be converted to float.")
                    is_correct = False
            except Exception as e:
                print(f"Error parsing NAT range: {e}")
                is_correct = False
        else:
            is_correct = model_answer == correct_answer

        # Marks calculation
        totalMarks += q.get("marks", 0)
        if is_correct:
            marks = q.get("marks", 0)
            if q["type"] == "MCQ":
                mcqCorrect += 1
            if q["type"] == "MSQ":
                msqCorrect += 1
            if q["type"] == "NAT":
                natCorrect += 1    
        else:
            if q["type"] == "MCQ":
                mcqWrong += 1
                if q.get("marks", 0) == 1:
                    marks = -0.33
                    negativeMarks += 0.33
                elif q.get("marks", 0) == 2:
                    marks = -0.67
                    negativeMarks += 0.67
            elif q["type"] == "MSQ":
                marks = 0
                msqWrong += 1
            elif q["type"] == "NAT":
                marks = 0
                natWrong += 1
                
        marksObtained += marks
        
        # Print results        
        print(f"Q{q['question_number']}: Model: {model_answer}, Correct: {correct_answer} — {'[✓]' if is_correct else '[x]'}")
        print(f"Marks for the question: {q.get('marks', 0)} (Marks received: {marks})")
        print(f"Type: {q['type']}")
        
        # Save result
        results.append({
            "question_number": q["question_number"],
            "model_answer": model_answer,
            "correct_answer": correct_answer,
            "type": q["type"],
            "is_correct": is_correct,
            "marks": marks,
        })
        
        print("------------------------------------------------------------------------------------------------------------------------------------")
        cnt += 1

        #for gemini 2.5 pro test
        # if(cnt == 49):
        #     if(model_name == 'models/gemini-2.5-pro'):
        #         print("50 questions completed on gemini 2.5 pro. exiting")
        #         break

        # Sleep for Rate limit 
        if cnt % rate_limits["batch_size"] == 0:
            print(f"Pause of {rate_limits['batch_sleep']} sec due to rate limiting")
            sleep_start = time.time()
            for remaining in range(rate_limits["batch_sleep"], 0, -1):
                print(f"\rResuming in {remaining} seconds...", end="", flush=True)
                time.sleep(1)
            sleep_end = time.time()
            total_sleep_time += (sleep_end - sleep_start)
            print("Resuming now!")
            print("********************************************************************************************************************************")

    i['state']['output'] = results
    i['state']['model_info'] = {'type': model_type, 'name': model_name}
    
    process_end = time.time()
    total_time = process_end - process_start
    effective_time = total_time - total_sleep_time
    filename = env.get('MLC_GATE_QUESTION_PDF_URL', 'https://github.com/user-attachments/files/20423322/CS25set2-questionPaper.pdf').split("/")[-1]

    # Results summary
    print(f"Result for: {model_name}")
    print(f"Question Paper Filename: {filename}")
    print("*******************************************************")
    print(f"Marks Obtained by {model_name} is {marksObtained:.2f} out of total {totalMarks} marks")
    print(f"# MCQ Correct: {mcqCorrect}, Wrong: {mcqWrong}")
    print(f"# MSQ Correct: {msqCorrect}, Wrong: {msqWrong}")
    print(f"# NAT Correct: {natCorrect}, Wrong: {natWrong}")
    print(f"Total Questions: {len(questions)}")
    print(f"Negative Marks: {negativeMarks:.2f}")
    print(f"Total Marks Obtained: {marksObtained:.2f}")
    print(f"Total Marks: {totalMarks:.2f}")
    print(f"Total Time Taken: {total_time:.2f} seconds (Effective Time: {effective_time:.2f} seconds, Sleep Time: {total_sleep_time:.2f} seconds)")
    print("*****************************************************************************************************************************************")
    return {'return': 0}


def resultProcess(i):
    state = i['state']
    results = state['output']
    model_info = state.get('model_info', {'type': 'unknown', 'name': 'unknown'})

    correct = sum(1 for r in results if r['is_correct'])
    wrong = len(results) - correct
    accuracy = 100 * correct / len(results) if results else 0

    # Save results in a JSON file
    results_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "results")
    os.makedirs(results_dir, exist_ok=True)
    filename = os.environ.get('MLC_GATE_QUESTION_PDF_URL', 'https://github.com/user-attachments/files/20423322/CS25set2-questionPaper.pdf').split("/")[-1]

    output_file = os.path.join(results_dir, f"{model_info['name']}_results.json")

    with open(output_file, "w") as f:
        json.dump({
            "model_info": model_info,
            "results": results,
            "summary": {
                "model-name": model_info['name'],
                "question-paper-filename": filename,
                "correct": correct,
                "wrong": wrong,
                "total": len(results),
                "total_marks": sum(r.get("marks", 0) for r in results),
                "accuracy": accuracy
            },
        }, f, indent=2)

    print(f"Results saved to: {output_file}")
    print("*********************************************************************************************************************************")
    print("Summary of results:")
    print("*********************************************************************************************************************************")
    print(f"Correct: {correct}, Wrong: {wrong}, Total: {len(results)}")
    print("---------------------")
    print(f"| Accuracy: {accuracy:.2f}%  |")
    print("---------------------")
    return {'return': 0}

if __name__ == "__main__":
    i = {'env': os.environ, 'state': {}}
    modelProcess(i)
    resultProcess(i)