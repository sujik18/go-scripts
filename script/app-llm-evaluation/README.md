## Demo
Test it live : https://huggingface.co/spaces/sujithh/llm-evaluation

## Installation
1. Install MLC and MLC Flow and activate the virtual environment with the following reference: https://docs.mlcommons.org/mlcflow/install/

2. Create a .env file in the same directory as the customize.py file with the following content:
    ```shell
    MLC_MODEL_TYPE='gemini' 
    (or 'openai' or 'groq' and make sure to set the corresponding API KEY)

    GEMINI_API_KEY='<your-api-key>'
    ```
    Replace `<your-api-key>` with your actual API key.

    ####  Optional Parameters and their default values
    ```shell
    OPENAI_API_KEY='<your-api-key>'
    GROQ_API_KEY='<your-api-key>'
    MLC_GEMINI_MODEL = 'models/gemini-2.5-flash' 
    MLC_GROQ_MODEL='llama-3.3-70b-versatile'
    MLC_OPENAI_MODEL='gpt-4o'

    MLC_GATE_QUESTION_PDF_URL = 'https://github.com/user-attachments/files/20423322/CS25set2-questionPaper.pdf'
    MLC_GATE_ANSWER_PDF_URL = 'https://github.com/user-attachments/files/20423320/CS25set2-answerKey.pdf'

    MLC_GATE_QUESTION_PDF_PATH = '~/MLC/repos/local/cache/gate-exam-data/paper.pdf'
    MLC_GATE_ANSWER_PDF_PATH = '~/MLC/repos/local/cache/gate-exam-data/key.pdf'
    
    MLC_GATE_OUTPUT_JSON_PATH = '~/MLC/repos/local/cache/gate-exam-data/output.json'

    ```
    NOTE: Temporary assets for GATE CS 25 can be obtained from [sujik18/go-script/release](https://github.com/sujik18/go-scripts/releases/tag/v1)

3. To run the script, use the following comm0and:
    ```shell
    mlcr llm-evaluation
    ```

This one script will automatically download the required GATE question paper and answer key, parse them, and run the specified Gemini model on the questions and answers.

## Results
1. Gemini-2.5-flash on GATE-CS 2025 Set 2 paper Test 1
    ```shell
    ------------------------------------------------------------------------------------------------------------------------------------
    Results for models/gemini-2.5-flash:
    *******************************************************
    Marks Obtained by models/gemini-2.5-flash is 78.32 out of total 100 marks
    # MCQ Correct: 30, Wrong: 6
    # MSQ Correct: 11, Wrong: 3
    # NAT Correct: 14, Wrong: 1
    Total Questions: 65
    Negative Marks: 3.6799999999999997
    Total Marks Obtained: 78.32
    Total Marks: 100
    Total Time Taken: 1631.97 seconds (Effective Time: 1271.53 seconds, Sleep Time: 360.44 seconds)
    *****************************************************************************************************************************************
    Summary of results:
    *********************************************************************************************************************************
    Correct: 55, Wrong: 10, Total: 65
    ---------------------
    | Accuracy: 84.62%  |
    ---------------------
    ```
2. Gemini-2.5-flash on GATE-CS 2025 Set 2 paper Test 2
    ```shell
    ------------------------------------------------------------------------------------------------------------------------------------
    Results for models/gemini-2.5-flash:
    Question Paper Filename:b''
    *******************************************************
    Marks Obtained by models/gemini-2.5-flash is 75.32 out of total 100 marks
    # MCQ Correct: 30, Wrong: 6
    # MSQ Correct: 10, Wrong: 4
    # NAT Correct: 13, Wrong: 2
    Total Questions: 65
    Negative Marks: 3.6799999999999997
    Total Marks Obtained: 75.32
    Total Marks: 100
    Total Time Taken: 1738.32 seconds (Effective Time: 1377.95 seconds, Sleep Time: 360.37 seconds)
    *****************************************************************************************************************************************
    Summary of results:
    *********************************************************************************************************************************
    Correct: 53, Wrong: 12, Total: 65
    ---------------------
    | Accuracy: 81.54%  |
    ---------------------
    ```
3. Gemini-2.5-flash on GATE-CS 2025 Set 1 paper
    ```shell
    ------------------------------------------------------------------------------------------------------------------------------------
    Results for models/gemini-2.5-flash:
    *******************************************************
    Marks Obtained by models/gemini-2.5-flash is 71.32 out of total 100 marks
    # MCQ Correct: 27, Wrong: 6
    # MSQ Correct: 8, Wrong: 2
    # NAT Correct: 16, Wrong: 6
    Total Questions: 65
    Negative Marks: 3.6799999999999997
    Total Marks Obtained: 71.32
    Total Marks: 100
    Total Time Taken: 1747.45 seconds (Effective Time: 1385.71 seconds, Sleep Time: 361.74 seconds)
    *****************************************************************************************************************************************
    Summary of results:
    *********************************************************************************************************************************
    Correct: 51, Wrong: 14, Total: 65
    ---------------------
    | Accuracy: 78.46%  |
    ---------------------
    ```
4. llama-3.3-70b-versatile on GATE-CS 2025 Set 2 paper (via Groq)
    ```shell
    ********************************************************************************************************************************
    Results for llama-3.3-70b-versatile:
    Question Paper Filename: b''
    *******************************************************
    Marks Obtained by llama-3.3-70b-versatile is 33.32999999999999 out of total 100 marks
    # MCQ Correct: 21, Wrong: 15
    # MSQ Correct: 6, Wrong: 8
    # NAT Correct: 2, Wrong: 13
    Total Questions: 65
    Negative Marks: 7.67
    Total Marks Obtained: 33.33
    Total Marks: 100
    Total Time Taken: 414.59 seconds (Effective Time: 24.18 seconds, Sleep Time: 390.41 seconds)
    *****************************************************************************************************************************************
    Summary of results:
    *********************************************************************************************************************************
    Correct: 29, Wrong: 36, Total: 65
    ---------------------
    | Accuracy: 44.62%  |
    ---------------------
    ```
5. gemma2-9b-it on GATE-CS 2025 Set 2 paper (via Groq)
    ```shell
    ********************************************************************************************************************************
    Results for gemma2-9b-it:
    Question Paper Filename: b''
    *******************************************************
    Marks Obtained by gemma2-9b-it is 13.67 out of total 100 marks
    # MCQ Correct: 13, Wrong: 23
    # MSQ Correct: 4, Wrong: 10
    # NAT Correct: 1, Wrong: 14
    Total Questions: 65
    Negative Marks: 11.33
    Total Marks Obtained: 13.67
    Total Marks: 100
    Total Time Taken: 134.75 seconds (Effective Time: 134.75 seconds, Sleep Time: 0.00 seconds)
    *****************************************************************************************************************************************
    Summary of results:
    *********************************************************************************************************************************
    Correct: 18, Wrong: 47, Total: 65
    ---------------------
    | Accuracy: 27.69%  |
    ---------------------
    ```
6. qwen3-32b on GATE-CS 2025 Set 2 paper (via Groq)
    ```shell
    ********************************************************************************************************************************
    Results for gemma2-9b-it:
    Question Paper Filename: b''
    *******************************************************
    Marks Obtained by gemma2-9b-it is 13.67 out of total 100 marks
    # MCQ Correct: 13, Wrong: 23
    # MSQ Correct: 4, Wrong: 10
    # NAT Correct: 1, Wrong: 14
    Total Questions: 65
    Negative Marks: 11.33
    Total Marks Obtained: 13.67
    Total Marks: 100
    Total Time Taken: 138.89 seconds (Effective Time: 138.89 seconds, Sleep Time: 0.00 seconds)
    *****************************************************************************************************************************************
    Summary of results:
    *********************************************************************************************************************************
    Correct: 18, Wrong: 47, Total: 65
    ---------------------
    | Accuracy: 27.69%  |
    ---------------------
    ```
