# Graduate Level Stats & Hard Level LeetCode GPT-4o VS OpenAI-o1 Problem-Solving Evaluation

## Project Overview
This project aims to create a dataset and evaluate the performance of two advanced large language models: **GPT-4o** and **OpenAI-o1**. The evaluation will focus on two types of problems:
1. **Graduate-level Statistics and PhD Qualification Problems**
2. **Hard-level LeetCode Coding Problems**

The dataset will be used to test and compare which LLM is better suited for high-level problem-solving in these areas.

## Project Goals
### 1. **Creating the Dataset**
We are building two distinct datasets:
- **Math Problems**: Problems sourced from graduate-level statistics or PhD qualification exams, with an empty solution field to be filled by LLMs.
- **LeetCode Problems**: Hard-level LeetCode problems that also have an empty solution field to be completed by LLMs.

### 2. **Model Evaluation**
Once the dataset is complete, we will evaluate the problem-solving ability of:
- **GPT-4o**
- **OpenAI-o1**

The evaluation will test both correctness and model reasoning capabilities when solving complex problems.

### 3. **Evaluation Process**
- **Manual Evaluation**: Initially, the solutions provided by the LLMs will be manually checked for correctness and reasoning quality.
- **Future Updates**: Automated evaluation for efficiency (runtime, memory usage) will be implemented at a later stage.

## How to Contribute
1. **Add New Problems**: Use our dataset manager tool to easily add new math or coding problems to the dataset.
2. **Run Evaluations**: After generating solutions with the models, the evaluations can be done manually using the problem's ground truth solutions.
3. **Submit Feedback**: Open issues or pull requests to improve the dataset or evaluation process.

## Repository Structure
- `math_problems.json`: JSON file for the graduate-level math problems.
- `leetcode_problems.json`: JSON file for LeetCode problems.
- `scripts/`: Contains the code for managing the dataset and running evaluations.

---

### Contact
For questions or contributions, feel free to open an issue or submit a pull request.
