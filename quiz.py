from random import sample, shuffle
from time import time
import requests


""" 
Full API copyrights & docs: 
https://the-trivia-api.com/docs/v2/ 

Non commercial project.
"""


class TriviaAPI:
    # Define the constructor
    def __init__(self, limit, region):
        self.limit = limit
        self.region = region
        self.url = "https://the-trivia-api.com/v2/questions"

    def get_questions(self):
        try:
            # Perform a GET request to fetch questions from the trivia API
            response = requests.get(
                url=self.url,
                params={
                    "limit": self.limit,
                    "region": self.region,
                },
            )
            # Raise an HTTPError if the request resulted in an error response
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"An error occurred while connecting to the API: {e}")
            print("Please try again later.")
            # Raise if can't connect to internet or API
        except requests.exceptions.ConnectionError as e:
            print(f"An error occurred while connecting to the API: {e}")
            print("Please try again later.")
            exit()

        # Parse the JSON response data
        data = response.json()
        return data


class Game:
    def __init__(self, questions):
        self.questions = questions
        self.counter = 1
        self.question_number = 0
        self.score = 0
        self.times = []
        self.ask_user_questions()
        self.quiz()
        self.summary()
        self.restart()

    def ask_user_questions(self):
        choice = input("Do you want to add your own questions? (Y/N) ")
        if choice.lower() == "y":
            # Create a loop to allow adding multiple questions
            while True:
                question = input("Provide the question text: ")
                correctAnswer = input("Provide the correct answer: ")
                incorrectAnswers = []
                for i in range(3):
                    incorrectAnswer = input(f"Provide the incorrect answer {i+1}: ")
                    incorrectAnswers.append(incorrectAnswer)
                question_dict = {
                    "question": {"text": question},
                    "correctAnswer": correctAnswer,
                    "incorrectAnswers": incorrectAnswers,
                }
                # validate the question and answers if they are not empty
                if not question or not correctAnswer or not incorrectAnswers:
                    print("Please provide the question and answers.")
                    continue
                # Add the dictionary to the questions list
                self.questions.append(question_dict)
                another = input("Do you want to add another question? (Y/N) ")
                if another.lower() != "y":
                    break

    def quiz(self):
        # select 10 random questions from the list of questions
        selected_questions = sample(self.questions, 10)

        # create a loop to ask the user for an answer to each question
        for question in selected_questions:
            # display the question and information
            print(f"Question number {self.question_number + 1}:")
            print(f"Category: {question['category']}")
            tags = ", ".join(question["tags"])
            print(f"Tags: {tags}")
            print(f"Difficulty: {question['difficulty']}")
            print(question["question"]["text"])

            # randomly shuffle the correct and incorrect answers
            options = question["incorrectAnswers"] + [question["correctAnswer"]]
            shuffle(options)

            # display the options to choose from
            for i in range(len(options)):
                print(f"{i+1}. {options[i]}")

            # loop until the user provides a valid answer
            valid = False
            while not valid:
                # get the answer from the user a start measuring time
                start = time()
                answer = input("Provide the answer number: ")
                end = time()
                self.times.append(end - start)
                # check if input is int and from len(options) range
                try:
                    answer = int(answer)
                    if answer in range(1, len(options) + 1):
                        valid = True
                    else:
                        print("Please provide a number from the list above.")
                except ValueError:
                    print("The answer must be a number. Please try again.")

            # check if the answer is correct
            if options[int(answer) - 1] == question["correctAnswer"]:
                print("Correct!")
                print(f"\n {len(question['question']['text']) * '-'}\n")
                self.score += 1
            else:
                print("Incorrect!")
                print(f"The correct answer is: {question['correctAnswer']}")
                print(f"\n {len(question['question']['text']) * '-'}\n")

            # increment the question number
            self.question_number += 1

    def summary(self):
        # Counting points and avg time per answer, fastest and slowest answer
        points = self.score
        percentage = points / 10 * 100
        avg_time = sum(self.times) / len(self.times)
        fastest_time = min(self.times)
        slowest_time = max(self.times)
        # Displaying summary
        print(f"Your score is: {points}/10")
        print(f"Percentage of correct answers: {percentage}%")
        print(f"Average time per answer: {avg_time:.2f} seconds")
        print(f"Fastest answer: {fastest_time:.2f} seconds")
        print(f"Slowest answer: {slowest_time:.2f} seconds")

    def restart(self):
        valid = False
        while not valid:
            choice = input("Do you want to play again? (Y/N) ")
            if choice.lower() == "y":
                print("Restarting the game...")
                if self.counter == 5:
                    self.questions = trivia.get_questions()
                    self.counter = 1
                else:
                    self.counter += 1
                self.question_number = 0
                self.score = 0
                self.times = []
                self.ask_user_questions()
                self.quiz()
                self.summary()

            elif choice.lower() == "n":
                # Exit the game
                print("Thank you for playing!")
                exit()
            else:
                print("Please provide a valid answer.")


trivia = TriviaAPI(limit=50, region="PL")
questions = trivia.get_questions()

play = Game(questions)
