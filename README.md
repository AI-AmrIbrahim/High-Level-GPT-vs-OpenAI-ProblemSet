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
    - `Simple Average`: (Runtime Beats + Memory Beats) / 2
    - `Weighted Average`: 0.6 * Runtime Beats + 0.4 * Memory Beats (prioritizing runtime slightly more).
  
- **Math Problem Evaluation**: This will be implemented as per team discussions but may focus on qualitative metrics such as the correctness and depth of reasoning.

### 4. **Ongoing Model Comparison**
After generating solutions from the models, we will store them in our dataset, alongside their evaluation metrics, allowing us to compare performance over time. This process will evolve to include more automated evaluation steps in the future.

## How to Contribute
1. **Add New Problems**: Use the `DatasetManager` tool to easily add new math or coding problems into the dataset. Ensure that each problem is unique and formatted according to the schema.
2. **Generate Solutions**: Prompt GPT-4o or OpenAI-o1 to solve the problems in the dataset. The solutions will be saved for evaluation.
3. **Run Evaluations**: LeetCode problem evaluations involve manually submitting solutions and entering runtime/memory performance data into the system.
4. **Submit Feedback**: Open issues or pull requests to propose improvements or report issues with the dataset, code, or evaluation methods.

## Repository Structure
- `math_problems.json`: Stores graduate-level math problems and their model-generated solutions.
- `leetcode_problems.json`: Stores hard-level LeetCode problems, solutions, and associated performance metrics.
- `scripts/`: Contains Python scripts for managing the dataset, prompting models, and evaluating results.
- `scripts/requirements.txt`: Lists the Python dependencies required to run the project.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/yourrepository.git
