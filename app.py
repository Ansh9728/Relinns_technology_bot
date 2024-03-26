
import openai
import streamlit as st
import requests
from bs4 import BeautifulSoup


# Fetching The website
@st.cache_data()
def fetch_website_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        return response.status_code

# return the relevant information of website
def fetch_relevant_information(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    text_content = soup.get_text()
    return text_content

# ChatGpt to to answer our query
def get_chatGpt_response(user_input, web_scraping_data):

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a chatbot."},
                {"role": "user", "content": user_input},
                {"role": "assistant", "content": web_scraping_data},
            ],
            max_tokens=150,
            temperature=0.7
        )
        reply = response['choices'][0].message.content
        return reply
    except openai.OpenAIError as e:
        st.error("An error occurred while generating the Chatbot response.")
        st.error(f"Error details: {e}")
        return None




# GUI and main function Implimentation
def main():

    openai.api_key="API KEY"

    st.set_page_config(
        page_title="Relinns ChatBot",
        page_icon=":robot_face:"
    )

    st.header("Relinns ChatBOT :robot_face:")
    st.write("Hello User")
    user_input_url = st.text_input("Please provide a URL:")


    if st.button("Fetch Website Content"):
        website_content = fetch_website_content(user_input_url)

        if website_content:
            st.success("Data Fetched Successfully")

    user_input = st.text_area("Chatbot: How can I assist you?", value="")

    if st.button("Get Response"):
        website_content = fetch_website_content(user_input_url)
        extracted_info = fetch_relevant_information(website_content)
        web_scraping_data = " ".join(extracted_info.split())

        if web_scraping_data:
            try:
                chatbot_response = get_chatGpt_response(user_input, web_scraping_data)

                # Display the chatbot's response
                st.write("Chatbot:", chatbot_response)

            except Exception as e:
                st.error(f"Error details: {e}")  # The error is already handled in the get_chatGpt_response function
        else:
            st.error("Please fetch website content first.")

if __name__ == '__main__':
    main()

