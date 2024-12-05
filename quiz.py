import json
import random
import pandas as pd

# Function to generate quiz questions from the dataset
def generate_questions(dataset_path):
    # Load the dataset into a DataFrame
    try:
        df = pd.read_csv(dataset_path)
        print(f"Loaded dataset with {len(df)} records.")
    except FileNotFoundError:
        print(f"Dataset file {dataset_path} not found!")
        return []
    except pd.errors.EmptyDataError:
        print(f"Dataset file {dataset_path} is empty!")
        return []
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return []

    # Print the column names to debug the issue
    columns = df.columns.tolist()
    print(f"Available columns: {columns}")

    questions = []
    question_id = 1  # Start question ID from 1

    # Ensure that we always generate questions for year, category, wind, and the name of the storm
    for i in range(5):  # Limit to exactly 5 questions
        # Sample a random row from the DataFrame until we get a valid row for each category
        valid_row = False
        while not valid_row:
            row = df.sample(1).iloc[0]  # Randomly select one row
            # Check if all required columns are present and have valid (non-NaN) values
            if pd.notna(row.get('year')) and pd.notna(row.get('category')) and pd.notna(row.get('wind')):
                valid_row = True  # If all required columns are valid, stop resampling

        # Extract required information from the row
        storm_name = row['name']
        year = row['year']
        category = row['category']
        wind = row['wind']

        # Generate question for 'year'
        choices = [str(year), str(year - 1), str(year + 1), str(year - 2)]
        random.shuffle(choices)

        question = {
            "id": question_id,
            "question": f"Which year did the hurricane {storm_name} occur?",
            "choices": choices,
            "answer": str(year)
        }
        questions.append(question)
        question_id += 1

        # Generate question for 'category'
        choices = ['Category 1', 'Category 2', 'Category 3', 'Category 4', 'Category 5']
        random.shuffle(choices)

        question = {
            "id": question_id,
            "question": f"What was the category of the hurricane {storm_name}?",
            "choices": choices,
            "answer": f"Category {category}"
        }
        questions.append(question)
        question_id += 1

        # Generate question for 'wind'
        choices = [str(wind), str(wind + 10), str(wind - 10), str(wind + 20)]
        random.shuffle(choices)

        question = {
            "id": question_id,
            "question": f"What was the maximum wind speed of hurricane {storm_name} (in mph)?",
            "choices": choices,
            "answer": str(wind)
        }
        questions.append(question)
        question_id += 1

        # Stop after 5 questions
        if len(questions) >= 5:
            break

    return questions

# Function to save the generated questions to a JSON file
def save_questions_to_file(questions, filename='questions.json'):
    try:
        with open(filename, 'w') as file:
            json.dump(questions, file, indent=4)
        print(f"Questions saved to {filename}.")
    except Exception as e:
        print(f"Error saving questions to file: {e}")


# Function to load questions from the JSON file and quiz the user in the console
def quiz_user_from_json(questions_file_path):
    try:
        with open(questions_file_path, 'r') as file:
            questions = json.load(file)
    except FileNotFoundError:
        print("Questions file not found!")
        return
    except json.JSONDecodeError:
        print("Error reading questions from the file.")
        return

    if not questions:
        print("No questions found!")
        return

    correct_answers = 0

    # Ask only the first 5 questions
    for i, question in enumerate(questions[:5]):  # Ensure only 5 questions are asked
        print(f"Question {i + 1}: {question['question']}")
        print("Choices:")
        for idx, choice in enumerate(question['choices'], 1):
            print(f"{idx}. {choice}")

        # Get user's answer
        user_answer = input("Your answer (1-4): ")

        # Check if the answer is correct
        try:
            user_answer = int(user_answer)
            if 1 <= user_answer <= 4 and question['choices'][user_answer - 1] == question['answer']:
                correct_answers += 1
                print("Correct!\n")
            else:
                print(f"Wrong! The correct answer was: {question['answer']}\n")
        except ValueError:
            print("Invalid input! Please enter a number between 1 and 4.")
        except IndexError:
            print("Invalid choice! Please enter a number between 1 and 4.")

    # Print results
    print(f"\nQuiz Complete! You got {correct_answers} out of 5 correct.")

    # Clear the questions file after the quiz is complete
    """""
    with open(questions_file_path, 'w') as file:
        json.dump([], file)  # Empty the file
    print(f"{questions_file_path} has been cleared.")
    """""
