import json
import os
import random
import requests
import openai
from openai import OpenAI

class DatasetManager:
    def __init__(self, dataset_folder='../High-Level-GPT-vs-OpenAI-ProblemSet/'):
        self.dataset_folder = dataset_folder
        self.math_dataset_path = os.path.join(self.dataset_folder, 'math_problems.json')
        self.leetcode_dataset_path = os.path.join(self.dataset_folder, 'leetcode_problems.json')
        self.titleslug_store_path = os.path.join(self.dataset_folder, 'queried_titleslugs.json')
        # Initialize datasets and titleslug store if they don't exist
        self._initialize_dataset(self.math_dataset_path)
        self._initialize_dataset(self.leetcode_dataset_path)
        # self._initialize_dataset(self.titleslug_store_path)
    
    def _initialize_dataset(self, path):
        """If the dataset file does not exist, create it with an empty structure."""
        try:
            if not os.path.exists(path):
                with open(path, 'w') as f:
                    json.dump({}, f, indent=4)
        except Exception as e:
            print(f"Error initializing dataset at {path}: {e}")
    
    def _is_duplicate(self, problem_str, dataset):
        """Check if the problem already exists in the dataset."""
        return any(problem_data["problem"] == problem_str for problem_data in dataset.values())

    
    def _get_next_id(self, dataset):
        """Generate the next ID based on the highest current ID."""
        if len(dataset) == 0:
            return 1
        return max(map(int, dataset.keys())) + 1


    def _is_duplicate_slug(self, title_slug):
        """Check if the title slug already exists in the titleslug store."""
        try:
            with open(self.titleslug_store_path, 'r') as f:
                title_slugs = json.load(f)
            return title_slug in title_slugs
        except Exception as e:
            print(f"Error checking duplicate slug: {e}")
            return False

    def _save_title_slug(self, title_slug):
        """Save the new title slug to the titleslug store."""
        try:
            with open(self.titleslug_store_path, 'r') as f:
                title_slugs = json.load(f)
            title_slugs.append(title_slug)
            with open(self.titleslug_store_path, 'w') as f:
                json.dump(title_slugs, f, indent=4)
        except Exception as e:
            print(f"Error saving title slug: {e}")
    
    def add_problem(self, problem_str, dataset_type="math", title_slug=None):
        """Add a new problem to the specified dataset (either 'math' or 'leetcode').
        If title_slug is provided, save it only if the problem is added successfully.
        """
        if not problem_str.strip():
            print("Problem string is empty. Cannot add an empty problem.")
            return
        
        if dataset_type == "math":
            dataset_path = self.math_dataset_path
        elif dataset_type == "leetcode":
            dataset_path = self.leetcode_dataset_path
        else:
            raise ValueError("Invalid dataset_type. Choose 'math' or 'leetcode'.")
        
        try:
            # Load the dataset
            with open(dataset_path, 'r') as f:
                dataset = json.load(f)

            # Check for duplicate problems
            if self._is_duplicate(problem_str, dataset):
                print(f"Problem already exists in {dataset_type} dataset.")
                return
            
            # Generate the new problem with an auto-incremented ID
            new_problem_id = str(self._get_next_id(dataset))
            if title_slug:
                new_problem_data = {
                    "title_slug": title_slug,
                    "problem": problem_str
                }
            else:
                new_problem_data = {"problem": problem_str}
            # Add the new problem to the dataset using the new ID as the key
            dataset[new_problem_id] = new_problem_data
            
            # Save the updated dataset
            with open(dataset_path, 'w') as f:
                json.dump(dataset, f, indent=4)
            print(f"New problem added to {dataset_type} dataset with ID {new_problem_id}.")
            
            # Save the titleSlug only if the problem was added
            # if title_slug:
            #     self._save_title_slug(title_slug)
        
        except Exception as e:
            print(f"Error adding problem to {dataset_type} dataset: {e}")

    def query_leetcode_problems(self, tag, limit_num=100):
        """Query LeetCode API to get a list of Hard questions for a given tag, select random titleslugs, and avoid duplicates."""
        URL_prob_list = f"https://alfa-leetcode-api.onrender.com/problems?tags={tag}&limit={limit_num}"
        
        try:
            r = requests.get(URL_prob_list)
            data = r.json()
            hard_questions = [q for q in data['problemsetQuestionList'] if q['difficulty'] == 'Hard']
            hard_question_titleslugs = [q['titleSlug'] for q in hard_questions]
            
            # Randomly select titleslugs and avoid duplicates
            random.shuffle(hard_question_titleslugs)
            
            # Get the initial count of problems in the dataset
            with open(self.leetcode_dataset_path, 'r') as f:
                initial_problem_count = len(json.load(f))
            print(f"Initial number of problems in dataset: {initial_problem_count}")
            
            problems_added = 0
            attempts = 0
            
            while problems_added < 15 and attempts < len(hard_question_titleslugs):
                slug = hard_question_titleslugs[attempts]
                attempts += 1

                # Check if the title_slug is already present in the dataset
                with open(self.leetcode_dataset_path, 'r') as f:
                    dataset = json.load(f)
                if slug in [entry["title_slug"] for entry in dataset.values()]:
                    continue  # Skip if duplicate title_slug found
                
                # if not self._is_duplicate_slug(slug):
                try:
                    # Try fetching and adding the problem
                    self.get_problem_description_and_add(slug)
                    
                    # Check if the problem was actually added
                    with open(self.leetcode_dataset_path, 'r') as f:
                        current_problem_count = len(json.load(f))
                    
                    if current_problem_count > initial_problem_count + problems_added:
                        problems_added += 1
                        print(f"Added problem {problems_added}/15")
                    else:
                        # print(f"Problem for {slug} was not added (likely duplicate content)")
                        pass
                except Exception as e:
                    # print(f"Error fetching problem for titleSlug {slug}: {e}")
                    pass
                
                if problems_added >= 15:
                    break
            
            # Get the final count of problems in the dataset
            # with open(self.leetcode_dataset_path, 'r') as f:
            #     final_problem_count = len(json.load(f))
            
            # print(f"Final number of problems in dataset: {final_problem_count}")
            # print(f"Total problems added in this run: {final_problem_count - initial_problem_count}")
            
            if problems_added < 15:
                print(f"Warning: Only able to add {problems_added} problems. Consider increasing the limit_num or adding more tags.")
        
        except Exception as e:
            print(f"Error querying LeetCode API: {e}")

    def get_problem_description_and_add(self, title_slug):
        """Fetch the problem description using the titleSlug and add it to the dataset."""
        URL_single = f"https://alfa-leetcode-api.onrender.com/select?titleSlug={title_slug}"
        
        try:
            r = requests.get(URL_single)
            problem_data = r.json()
            problem_description = problem_data["question"] + problem_data['exampleTestcases']
            
            if problem_description:
                self.add_problem(problem_description, dataset_type="leetcode", title_slug=title_slug)
            else:
                print(f"No description found for titleSlug {title_slug}.")
        
        except Exception as e:
            print(f"Error fetching problem for titleSlug {title_slug}: {e}")
    
    def remove_problem(self, problem_id, dataset_type="math"):
        """Remove a problem by its ID from the specified dataset (either 'math' or 'leetcode')."""
        if dataset_type == "math":
            dataset_path = self.math_dataset_path
        elif dataset_type == "leetcode":
            dataset_path = self.leetcode_dataset_path
        else:
            raise ValueError("Invalid dataset_type. Choose 'math' or 'leetcode'.")
        
        try:
            # Load the dataset
            with open(dataset_path, 'r') as f:
                dataset = json.load(f)
            
            del dataset[str(problem_id)]
            
            # Save the updated dataset
            with open(dataset_path, 'w') as f:
                json.dump(dataset, f, indent=4)
            print(f"Problem with ID {problem_id} removed from {dataset_type} dataset.")
        except Exception as e:
            print(f"Error removing problem from {dataset_type} dataset: {e}")
    
    def prompt_llm(self, openai_key, problem_id, model_name = "gpt-4o", dataset_type = "math"):
        if dataset_type == "math":
            dataset_path = self.math_dataset_path
            context = """You are an expert statistician and mathematician with extensive knowledge in advanced statistical methods, probability theory, and mathematical proofs. Your task is to solve PhD Qualifier and Graduate Level Statistics problems, providing a comprehensive, step-by-step solution. Focus on the following aspects:

1. Detailed Steps: Show all work, including intermediate calculations, algebraic manipulations, and reasoning behind each step.
2. Correctness: Ensure that your final answer and all intermediate steps are mathematically correct.
3. Logical Flow: Present your solution in a clear, logical sequence that a fellow graduate student or professor can follow.


Please adhere to these guidelines:

- Explain the reasoning behind key steps, especially for non-trivial operations or conceptual leaps.
- Begin with a brief outline or approach to the problem.
- Clearly state and explain any assumptions or theorems you're using.
- Use LaTeX-style formatting for mathematical expressions (e.g., $\frac{d}{dx}$ for fractions, \sum for summations).
- If the problem involves proofs, ensure each step logically follows from the previous one.
- Conclude with a clear, boxed final answer if applicable.

Your solution should be comprehensive enough for a professor to award full marks in a PhD qualifier or graduate-level exam setting."""
        elif dataset_type == "leetcode":
            dataset_path = self.leetcode_dataset_path
            context = """You are an expert algorithm designer and Python programmer. Your task is to solve a LeetCode hard problem, optimizing for the following criteria in order of importance:

1. Correctness: The solution must be correct and pass all test cases.
2. Time Complexity: Optimize the algorithm for the best possible time complexity.
3. Space Complexity: Minimize the space usage while maintaining the best time complexity.

Please follow these guidelines:
- Start your solution with the following structure:

  class Solution:
      def FunctionName(self, ... ) -> ... :
          # Your code here

- Replace 'FunctionName' with the appropriate function name for the problem.
- Fill in the parameters and return type as required by the problem.
- Provide only the Python code for the solution.
- Do not include any explanations, comments, or docstrings in your code.
- Use meaningful variable names to enhance code readability.
- If multiple solutions exist, provide the one with the best balance of time and space complexity.
- Ensure your code follows Python best practices and PEP 8 style guidelines.
- Your solution must be contained entirely within the class and function structure provided.

Your code will be directly submitted to the LeetCode judge, so it must be complete and runnable without any modifications."""
        else:
            raise ValueError("Invalid dataset_type. Choose 'math' or 'leetcode'.")
        
        # Load the problem description from the dataset
        with open(dataset_path, 'r') as f:
            dataset = json.load(f)

        # Check if the problem ID exists
        if str(problem_id) not in dataset:
            print(f"Problem with ID {problem_id} not found in the {dataset_type} dataset.")
            return
        
        # Find the problem by ID
        problem = dataset[str(problem_id)]
        if not problem:
            print(f"Problem with ID {problem_id} not found.")
            return
        
        problem_str = dataset[str(problem_id)]["problem"]
        
        if model_name == "o1-preview":
            client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=openai_key)
        else:
            client = OpenAI(api_key=openai_key)
        # openai.api_key = openai_key



        # Select the appropriate model based on the input
        # if model == "GPT-4o":
            # response = openai.ChatCompletion.create(
        selected_model = f"openai/{model_name}" if model_name == "o1-preview" else model_name
        
        response = client.chat.completions.create(
            model= selected_model,
            messages=[
                {
                "role": "system",
                "content": context
                },
                {
                "role": "user",
                "content": problem_str
                }
            ],
            max_tokens=16000,  # Adjust as needed to ensure enough space for longer solutions
            temperature=0  # Ensures deterministic output
        )
            # Store the solution in the GPT-4o slot
        solution = response.choices[0].message.content.replace('```python\n', '').replace('\n```', '')
        dataset[str(problem_id)][model_name] = {"solution": solution}
        # dataset[str(problem_id)][model_name]["solution"] = solution
        
        # elif model == "OpenAI-o1":
        #     # response = openai.ChatCompletion.create(
        #     response = client.chat.completions.create(
        #         model="o1-preview",
        #         messages=[
        #             {
        #             "role": "system",
        #             "content": context
        #             },
        #             {
        #             "role": "user",
        #             "content": problem_str
        #             }
        #         ],
        #         max_tokens=5000,
        #         temperature=0  # Ensures deterministic output
        #     )
        #     # Extract the generated code and store in the problem entry
        #     solution = response.choices[0].message.content.replace('```python\n', '').replace('\n```', '')
        #     dataset[str(problem_id)]["OpenAI-o1"]["solution"] = solution
        
        # else:
        #     raise ValueError("Invalid model name. Choose either 'GPT-4o' or 'OpenAI-o1'.")
        
        # Save the updated dataset with the new solution
        with open(dataset_path, 'w') as f:
            json.dump(dataset, f, indent=4)
        
        if dataset_type == "leetcode":
            print(f'Problem title: {dataset[str(problem_id)]["title_slug"]}')
        print(f"\nSolution added to {model_name} for problem ID {problem_id} to {dataset_type} dataset.")
        print(f"\n{model_name} solution for problem ID {problem_id}:")
        print("-" * 50)
        print(solution)
        print("-" * 50)

    def eval(self, problem_id, model_name="gpt-4o", dataset_type="math", runtime_beats=None, memory_beats=None, 
            correctness_final=None, correctness_steps=None, clarity_explanation=None, completeness=None, appropriate_methods=None):
        """
        Evaluate a model's solution for a problem in either the math or leetcode dataset.
        """
        # Set dataset path based on dataset_type
        if dataset_type == "math":
            dataset_path = self.math_dataset_path
        elif dataset_type == "leetcode":
            dataset_path = self.leetcode_dataset_path
        else:
            raise ValueError("Invalid dataset_type. Choose 'math' or 'leetcode'.")

        # Load the dataset
        with open(dataset_path, 'r') as f:
            dataset = json.load(f)

        # Check if the problem ID exists in the dataset
        if str(problem_id) not in dataset:
            print(f"Problem with ID {problem_id} not found in the {dataset_type} dataset. Please check the problem ID.")
            return

        # Check if the model_name exists and has a solution for the problem
        if model_name not in dataset[str(problem_id)] or not dataset[str(problem_id)][model_name].get("solution"):
            print(f"No solution found for model '{model_name}' in problem ID {problem_id}. Possible issues:")
            print("- The model name or problem ID might be incorrect.")
            print("- The solution may not have been generated yet.")
            return

        # For LeetCode dataset, prompt for runtime and memory if not provided
        if dataset_type == "leetcode":
            try:
                if runtime_beats is None:
                    runtime_beats = float(input("Enter the LeetCode Solution Runtime Beats: "))
                if memory_beats is None:
                    memory_beats = float(input("Enter the LeetCode Solution Memory Beats: "))
                feedback = input("Enter feedback: ")
            except ValueError:
                print("Invalid input. Please enter numeric values for runtime and memory beats.")
                return

            # Calculate average scores
            simple_average = (runtime_beats + memory_beats) / 2
            weighted_average = 0.6 * runtime_beats + 0.4 * memory_beats

            # Update model's evaluation in the dataset
            dataset[str(problem_id)].setdefault(model_name, {})["runtime_beats"] = runtime_beats
            dataset[str(problem_id)][model_name]["memory_beats"] = memory_beats
            dataset[str(problem_id)][model_name]["simple_average"] = simple_average
            dataset[str(problem_id)][model_name]["weighted_average"] = weighted_average
            dataset[str(problem_id)][model_name]["feedback"] = feedback

        elif dataset_type == "math":
            try:
                if correctness_final is None:
                    correctness_final = int(input("Rate the correctness of final answer on a scale of 1 (Poor) to 5 (Excellent): "))
                if correctness_steps is None:
                    correctness_steps = int(input("Rate the correctness of intermediate steps on a scale of 1 (Poor) to 5 (Excellent): "))
                if clarity_explanation is None:
                    clarity_explanation = int(input("Rate the clarity and depth of exmplanation on a scale of 1 (Poor) to 5 (Excellent): "))
                if completeness is None:
                    completeness = int(input("Rate the completness on a scale of 1 (Poor) to 5 (Excellent): "))
                if appropriate_methods is None:
                    appropriate_methods = int(input("Rate the use of appropriate methods and terminology on a scale of 1 (Poor) to 5 (Excellent): "))

                # Check for valid inputs
                if not all(1 <= score <= 5 for score in [correctness_final, correctness_steps, clarity_explanation, completeness, appropriate_methods]):
                    print("Invalid scores entered. All scores must be between 1 and 5.")
                    return
                    
            except ValueError:
                print("Invalid input. Please enter integer values between 1 and 5.")
                return

            # Calculate weighted score for math
            weighted_score = (
                0.25 * correctness_final +
                0.30 * correctness_steps +
                0.20 * clarity_explanation +
                0.15 * completeness +
                0.10 * appropriate_methods
            )
    
            # Save evaluations for Math
            model_data = dataset[str(problem_id)].setdefault(model_name, {})
            model_data["correctness_final"] = correctness_final
            model_data["correctness_steps"] = correctness_steps
            model_data["clarity_explanation"] = clarity_explanation
            model_data["completeness"] = completeness
            model_data["appropriate_methods"] = appropriate_methods
            model_data["weighted_score"] = weighted_score

        # Save the updated dataset
        with open(dataset_path, 'w') as f:
            json.dump(dataset, f, indent=4)

        print(f"Evaluation metrics added to {model_name} for problem ID {problem_id}.")
