import openai as openai
import gradio as gr
# import time

from dotenv import dotenv_values

config = dotenv_values(".env")

openai.api_key = config["OPENAI_API_KEY"]

messages = [
    {
        "role": "system",
        "content": "You are a quiz. You only ask very difficult questions. Present the user with a difficult multiple-choice question to practice for a data science interview. The position they are interviewing for is 'Senior Data Scientist'. Ask technical questions about Statistics, Machine Learning, Regularization, Cross-Validation, Probability, Bayes Rule, A/B Testing, Gradient Boosting, Logistic Regression, Data Science Technique, Data Science Best Practices, Data Science Mistakes, etc. Assume the user is smart, highly knowledgable and has a PhD in Data Science. They have to respond by typing 'a', 'b', 'c', 'd' or 'e'. Only one question at a time. Wait until the user responds before presenting a new question or the answer to the previous question. When answering the user, tell them if they got it correct, then tell them why it is correct or incorrect, then present a new question immediately. ",
    }
]


def format_text(user_input, chatbot):
    global messages
    chatbot = chatbot + [[user_input, ""]]
    messages.append({"role": "user", "content": user_input})
    return "", chatbot


def get_response(user_input, chatbot):
    global messages
    
    # add user input to messages
    # chatbot = chatbot + [[user_input, ""]]
    new_message = {"role": "user", "content": user_input}
    messages.append(new_message)
    # for msg in messages:
    #     print(msg)
    print(chatbot)
    print('\n\n')
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages
    )
    
    # obtain response text to messages
    return_message = response.choices[0].message
    messages.append(return_message)
    
    return chatbot + [[user_input, return_message.content]]


def main():
    with gr.Blocks() as quizbot:
        gr.Markdown("# GPT-3 Data Science Quiz Grader\n<br/>")
        gr.Markdown('### Instructions:\n')
        gr.Markdown("\nHit \"start\" in the text area to start the quiz\nIf you don't get a question, just hit \<enter\> or ask the quiz for another question.\n")
        gr.Markdown("This is GPT - don't expect the question/answers to always be correct!\n<br/>")
        
        chatbot = gr.Chatbot(label="Data Science QuizBot")
        user_input = gr.Textbox(label="Enter your answer here:", value='start')

        user_input.submit(
            get_response,
            inputs=[user_input, chatbot],
            outputs=chatbot,
        )

    quizbot.launch(share=False)


if __name__ == "__main__":
    main()
