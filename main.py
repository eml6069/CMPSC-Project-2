import os
from quiz import generate_questions, save_questions_to_file, quiz_user_from_json

# Ensure the dataset path is correct
dataset_path = os.path.join(os.getcwd(), 'datasets', 'storms.csv')

# Print the current working directory
print(f"Current working directory: {os.getcwd()}")

# Check if the dataset file exists
if os.path.exists(dataset_path):
    print("The dataset file was found!")
else:
    print("The dataset file was NOT found!")
    exit(1)  # Exit the program if the file is not found

# Function to ask if the user wants to restart or exit
def ask_to_restart_or_exit():
    while True:
        choice = input("\nWould you like to restart the quiz? (y/n): ").strip().lower()
        if choice == 'y':
            main()  # Restart the quiz by calling main()
        elif choice == 'n':
            print("Exiting the quiz. Goodbye!")
            break
        else:
            print("Invalid input. Please enter 'y' to restart or 'n' to exit.")

# Main function to generate questions and start the quiz directly
def main():
    try:
        questions = generate_questions(dataset_path)
    except Exception as e:
        print(f"Error generating questions: {e}")
        return

    # If questions were generated, save them to questions.json
    if questions:
        save_questions_to_file(questions)
        print("Questions saved to questions.json!")
    else:
        print("No questions generated.")
        return

    # Run the quiz in the console after generating the questions
    quiz_user_from_json('questions.json')  # Make sure to pass the correct file path here

    # After clearing the questions, ask if the user wants to restart or exit
    ask_to_restart_or_exit()

if __name__ == "__main__":
    main()
