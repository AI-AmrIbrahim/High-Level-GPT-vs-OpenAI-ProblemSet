# Graduate-Level Statistics, PhD Quals, & Hard LeetCode Problem-Solving: GPT-4o vs OpenAI-o1 Evaluation

## Project Overview
This project aims to **evaluate the problem-solving performance** of two large language models: **GPT-4o** and **OpenAI-o1**. The evaluation focuses on two challenging domains:
1. **Graduate-level Statistics and PhD Qualification Problems**
2. **Hard-level LeetCode Coding Problems**

We aim to measure the effectiveness, efficiency, and overall quality of solutions provided by these models.

## Project Goals
### 1. **Dataset Creation**
We are constructing two datasets:
- **Math Dataset**: Contains problems from graduate-level statistics courses or PhD qualification exams, with empty solution fields that will be populated by the models.
- **LeetCode Dataset**: Focuses on hard-level coding problems sourced from LeetCode. These problems also have empty solution fields.

### 2. **Model Performance Evaluation**
Once the datasets are finalized, both **GPT-4o** and **OpenAI-o1** will be evaluated on their ability to solve these problems. The key evaluation metrics are:
- **Correctness**: Whether the models’ solutions are accurate.
- **Efficiency**: Evaluation of runtime and memory usage for coding problems.
- **Reasoning**: The models' ability to generate high-quality, logical solutions for complex math and coding problems.

### 3. **Evaluation Process**
- **LeetCode Problem Evaluation**: After generating solutions for coding problems, we will manually submit them to LeetCode, extracting key performance metrics:
  - **Runtime Beats**: Percentage of submissions the solution is faster than.
  - **Memory Beats**: Percentage of submissions that use more memory.
  - **Evaluation Metrics**: 
    - `Simple Average: (Runtime Beats + Memory Beats) / 2`
    - `Weighted Average: 0.6 * Runtime Beats + 0.4 * Memory Beats (prioritizing runtime slightly more).`
  
- **Math Problem Evaluation**: The performance of GPT-4o and OpenAI-o1-preview was evaluated using a custom math rubric, as our problem involved advanced mathematical concepts, and linguistic analysis alone was insufficient. We opted for a more sophisticated human evaluation approach.

`Math Score = 0.25 * correctness_final +  0.30 * correctness_steps +  0.20 * clarity_explanation +  0.15 * completeness +  0.10 * appropriate_methods`


![image](https://github.com/user-attachments/assets/40ecd0fc-f11b-4a00-b78c-86160aebc02a)

### 4. **Ongoing Model Comparison**
After generating solutions from the models, we will store them in our dataset, alongside their evaluation metrics, allowing us to compare performance over time. This process will evolve to include more automated evaluation steps in the future.

## Full Report 
For a detailed explanation of the methodology, results, and analysis, view the [Final Report](https://github.com/AI-AmrIbrahim/High-Level-GPT-vs-OpenAI-ProblemSet/blob/main/Final%20Report.pdf).

## How to Use
### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/AI-AmrIbrahim/High-Level-GPT-vs-OpenAI-ProblemSet.git
   ```
2. Navigate to the project directory:
   ```bash
   cd High-Level-GPT-vs-OpenAI-ProblemSet
   ```
3. Install the required dependencies:
   ```bash
   pip install -r scripts/requirements.txt
   ```
### Using `DatasetManager` in Python
Currently only Python interaction is supported and CLI scripts are not available.
#### Initiating Dataset Manager
```python
from scripts.data_manager import DatasetManager
manager = DatasetManager()
```
#### Adding New Problems to a Dataset
```python
manager.add_problem("Find the determinant of this matrix...", dataset_type="math")
```
#### Generating Solution
Currently, only OpenAI models are supported. For o1-preview, users need to provide an OpenRouter API key.

**Ensure that you have access to the appropriate API keys.** For GPT-4o, use an OpenAI API key, while for o1-preview, use an OpenRouter API key.
```python
manager.prompt_llm(openai_key=API_KEY, problem_id=1, model_name="gpt-4o", dataset_type="leetcode")
```
#### Evaluating Solutions
User can either pass supported evaluation metrics through arguments or through input evaluations.
```python
# Example for math dataset. Metrics in the range 1 to 5
manager.eval(problem_id=1, model="gpt-4o", dataset_type="math",
             correctness_final=5, correctness_steps=4, 
             clarity_explanation=5, completeness=5, appropriate_methods=4)

# Example for leetcode dataset. Metrics in the range 0 to 100
manager.eval(problem_id=1, model="gpt-4o", dataset_type="leetcode",
             runtime_beats=80.5, memory_beats=75.3)
```

## Repository Structure
- `math_problems.json`: Stores graduate-level math problems and their model-generated solutions.
- `leetcode_problems.json`: Stores hard-level LeetCode problems, solutions, and associated performance metrics.
- `scripts/`: Contains Python scripts for managing the dataset, prompting models, and evaluating results.
- `scripts/requirements.txt`: Lists the Python dependencies required to run the project.

## Future Work
- **Automating Evaluation**: We aim to automate the evaluation of coding problems by integrating a custom scoring system that analyzes runtime and memory performance.
- **Math Problem Evaluation**: Define and implement metrics to evaluate reasoning and correctness in math problems.
- **OpenAI-o1 Updates**: Transition from the `o1-preview` model to the fully released OpenAI-o1 model as soon as it becomes available.

## Acknowledgments
- Groupmates:
    - Solha Park (Stony Brook University Data Science PhD Candidate)
    - David Zhao (Stony Brook University Data Science PhD Candidate)
- Tools:
    - [Alfa LeetCode API](https://github.com/alfaarghya/alfa-leetcode-api)
