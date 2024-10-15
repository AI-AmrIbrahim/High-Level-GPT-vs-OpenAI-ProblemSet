import json
import os
import random
import requests

class DatasetManager:
    def __init__(self, dataset_folder='../High-Level-GPT-vs-OpenAI-ProblemSet/'):
        self.dataset_folder = dataset_folder
        self.math_dataset_path = os.path.join(self.dataset_folder, 'math_problems.json')
        self.leetcode_dataset_path = os.path.join(self.dataset_folder, 'leetcode_problems.json')
        self.titleslug_store_path = os.path.join(self.dataset_folder, 'queried_titleslugs.json')
        # Initialize datasets and titleslug store if they don't exist
        self._initialize_dataset(self.math_dataset_path)
        self._initialize_dataset(self.leetcode_dataset_path)
        self._initialize_dataset(self.titleslug_store_path)
    
    def _initialize_dataset(self, path):
        """If the dataset file does not exist, create it with an empty structure."""
        try:
            if not os.path.exists(path):
                with open(path, 'w') as f:
                    json.dump([], f, indent=4)
        except Exception as e:
            print(f"Error initializing dataset at {path}: {e}")
    
    def _is_duplicate(self, problem_str, dataset):
        """Check if the problem already exists in the dataset."""
        return any(item["problem"] == problem_str for item in dataset)
    
    def _get_next_id(self, dataset):
        """Generate the next ID based on the highest current ID."""
        if len(dataset) == 0:
            return 1
        return max(item["id"] for item in dataset) + 1

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
            new_problem = {
                "id": self._get_next_id(dataset),
                "problem": problem_str,
                "4o-solution": "",  # Empty solution to be filled later
                "o1-solution": ""  # Empty solution to be filled later
            }
            dataset.append(new_problem)
            
            # Save the updated dataset
            with open(dataset_path, 'w') as f:
                json.dump(dataset, f, indent=4)
            print(f"New problem added to {dataset_type} dataset with ID {new_problem['id']}.")
            
            # Save the titleSlug only if the problem was added
            if title_slug:
                self._save_title_slug(title_slug)
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
            selected_titleslugs = []
            i = 0
            
            # Ensure that 15 problems are successfully added, even after encountering errors
            while len(selected_titleslugs) < 15 and i < len(hard_question_titleslugs):
                slug = hard_question_titleslugs[i]
                i += 1
                
                if not self._is_duplicate_slug(slug):
                    try:
                        # Try fetching and adding the problem
                        self.get_problem_description_and_add(slug)
                        selected_titleslugs.append(slug)  # Append only after successful fetch
                    except Exception as e:
                        # Catch the error for a specific slug and print the message but continue
                        print(f"Error fetching problem for titleSlug {slug}: {e}")
                        # Do not append to selected_titleslugs on error; just move to next slug
                        continue
                
                if len(selected_titleslugs) >= 15:  # Early exit after getting 15 unique slugs
                    break

            # Check if less than 15 slugs were added due to errors
            if len(selected_titleslugs) < 15:
                print(f"Only {len(selected_titleslugs)} problems were added due to errors or limitations.")
        
        except Exception as e:
            print(f"Error querying LeetCode API: {e}")

    
    def query_multiple_tags(self, tags_limits):
        """Query LeetCode API for multiple tags with specified limits, select random titleslugs, and avoid duplicates."""
        for tag, limit_num in tags_limits.items():
            print(f"Querying LeetCode for tag: {tag} with limit: {limit_num}")
            self.query_leetcode_problems(tag, limit_num)

    
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
            
            # Find the problem by ID and remove it
            dataset = [item for item in dataset if item["id"] != problem_id]
            
            # Save the updated dataset
            with open(dataset_path, 'w') as f:
                json.dump(dataset, f, indent=4)
            print(f"Problem with ID {problem_id} removed from {dataset_type} dataset.")
        except Exception as e:
            print(f"Error removing problem from {dataset_type} dataset: {e}")
