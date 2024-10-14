import json
import os

class DatasetManager:
    def __init__(self, dataset_folder='../High-Level-GPT-vs-OpenAI-ProblemSet/'):
        self.dataset_folder = dataset_folder
        self.math_dataset_path = os.path.join(self.dataset_folder, 'math_problems.json')
        self.leetcode_dataset_path = os.path.join(self.dataset_folder, 'leetcode_problems.json')
        # Initialize datasets if they don't exist
        self._initialize_dataset(self.math_dataset_path)
        self._initialize_dataset(self.leetcode_dataset_path)
    
    def _initialize_dataset(self, path):
        """If the dataset file does not exist, create it with an empty structure."""
        if not os.path.exists(path):
            with open(path, 'w') as f:
                json.dump([], f, indent=4)
    
    def _is_duplicate(self, problem_str, dataset):
        """Check if the problem already exists in the dataset."""
        return any(item["problem"] == problem_str for item in dataset)
    
    def _get_next_id(self, dataset):
        """Generate the next ID based on the highest current ID."""
        if len(dataset) == 0:
            return 1
        return max(item["id"] for item in dataset) + 1
    
    def add_problem(self, problem_str, dataset_type="math"):
        """Add a new problem to the specified dataset (either 'math' or 'leetcode')."""
        if dataset_type == "math":
            dataset_path = self.math_dataset_path
        elif dataset_type == "leetcode":
            dataset_path = self.leetcode_dataset_path
        else:
            raise ValueError("Invalid dataset_type. Choose 'math' or 'leetcode'.")
        
        # Load the dataset
        with open(dataset_path, 'r') as f:
            dataset = json.load(f)
        
        # Generate the new problem with an auto-incremented ID
        new_problem = {
            "id": self._get_next_id(dataset),
            "problem": problem_str,
            "solution": ""  # Empty solution to be filled later
        }
        dataset.append(new_problem)
        
        # Save the updated dataset
        with open(dataset_path, 'w') as f:
            json.dump(dataset, f, indent=4)
        print(f"New problem added to {dataset_type} dataset with ID {new_problem['id']}.")
    
    def remove_problem(self, problem_id, dataset_type="math"):
        """Remove a problem by its ID from the specified dataset (either 'math' or 'leetcode')."""
        if dataset_type == "math":
            dataset_path = self.math_dataset_path
        elif dataset_type == "leetcode":
            dataset_path = self.leetcode_dataset_path
        else:
            raise ValueError("Invalid dataset_type. Choose 'math' or 'leetcode'.")
        
        # Load the dataset
        with open(dataset_path, 'r') as f:
            dataset = json.load(f)
        
        # Find the problem by ID and remove it
        dataset = [item for item in dataset if item["id"] != problem_id]
        
        # Save the updated dataset
        with open(dataset_path, 'w') as f:
            json.dump(dataset, f, indent=4)
        print(f"Problem with ID {problem_id} removed from {dataset_type} dataset.")