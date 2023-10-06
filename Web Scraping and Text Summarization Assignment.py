#!/usr/bin/env python
# coding: utf-8

# # Importing all the Required Libraries

# In[2]:


get_ipython().system('pip install requests')
get_ipython().system('pip install beautifulsoup4')
get_ipython().system('pip install bert-extractive-summarizer')


# # Web Scraping, Text Summarization and Saving the Summarized Wikipedia Page in HTML Format

# In[3]:


import requests
from bs4 import BeautifulSoup
from summarizer import Summarizer

def extract_text_from_element(element):
    # Extract and return text from an HTML element, stripping any HTML tags
    if element:
        return element.get_text(separator=' ', strip=True)
    return ""

def remove_brackets_at_end(text):
    # Remove "[" character at the end of the text
    if text.endswith(" ["):
        return text[:-2]  # Remove the last two characters
    return text

def scrape_and_summarize_wikipedia(url):
    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the main content by searching for common content-containing elements
    content_elements = soup.find_all(['p', 'ul', 'ol', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

    # Initialize a dictionary to store section titles and their summaries
    summary_dict = {}

    # Variables to keep track of the current section title and content
    current_section_title = None
    current_section_content = []

    # Initialize the BERT summarizer
    summarizer = Summarizer()

    for element in content_elements:
        if element.name.startswith('h'):
            # Found a new section heading
            if current_section_title:
                # If there was a previous section, store its content
                section_text = ' '.join(current_section_content)
                if section_text.strip():
                    # Summarize the section text with longer summaries (8 sentences)
                    section_summary = summarizer(section_text, num_sentences=8)
                    if section_summary:
                        # Remove "[" character only if it's at the end
                        section_summary = remove_brackets_at_end(section_summary)
                        summary_dict[current_section_title] = section_summary

            # Start a new section with the current heading
            current_section_title = element.text.strip()
            current_section_content = []
        else:
            # Append the content to the current section
            content_text = extract_text_from_element(element)
            current_section_content.append(content_text)

    # Save the last section
    if current_section_title:
        # If there was a previous section, store its content
        section_text = ' '.join(current_section_content)
        if section_text.strip():
            # Summarize the section text with longer summaries (8 sentences)
            section_summary = summarizer(section_text, num_sentences=8)
            if section_summary:
                # Remove "[" character only if it's at the end
                section_summary = remove_brackets_at_end(section_summary)
                summary_dict[current_section_title] = section_summary

    return summary_dict

def save_summaries_to_html(summaries, filename):
    with open(filename, "w", encoding="utf-8") as file:
        file.write("<html>\n<head>\n<title>Wikipedia Summaries</title>\n</head>\n<body>\n")
        for section_title, section_summary in summaries.items():
            file.write(f"<h2>{section_title}</h2>\n")
            file.write(f"<p>{section_summary}</p>\n")
        file.write("</body>\n</html>\n")

def main():
    # Define the Wikipedia URL to scrape
    url = "https://en.wikipedia.org/wiki/Alexander_the_Great"

    # Scrape and summarize the Wikipedia page with longer summaries
    result = scrape_and_summarize_wikipedia(url)

    # Save the summaries to an HTML file
    save_summaries_to_html(result, "wikipedia_summaries.html")

    print("Summaries saved to wikipedia_summaries.html")

if __name__ == "__main__":
    main()


# # Saving the same Summarized Output page as Text File

# In[4]:


import requests
from bs4 import BeautifulSoup
from summarizer import Summarizer

def extract_text_from_element(element):
    # Extract and return text from an HTML element, stripping any HTML tags
    if element:
        return element.get_text(separator=' ', strip=True)
    return ""

def remove_brackets_at_end(text):
    # Remove "[" character at the end of the text
    if text.endswith(" ["):
        return text[:-2]  # Remove the last two characters
    return text

def scrape_and_summarize_wikipedia(url):
    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the main content by searching for common content-containing elements
    content_elements = soup.find_all(['p', 'ul', 'ol', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

    # Initialize a dictionary to store section titles and their summaries
    summary_dict = {}

    # Variables to keep track of the current section title and content
    current_section_title = None
    current_section_content = []

    # Initialize the BERT summarizer
    summarizer = Summarizer()

    for element in content_elements:
        if element.name.startswith('h'):
            # Found a new section heading
            if current_section_title:
                # If there was a previous section, store its content
                section_text = ' '.join(current_section_content)
                if section_text.strip():
                    # Summarize the section text with longer summaries (8 sentences)
                    section_summary = summarizer(section_text, num_sentences=8)
                    if section_summary:
                        # Remove "[" character only if it's at the end
                        section_summary = remove_brackets_at_end(section_summary)
                        summary_dict[current_section_title] = section_summary

            # Start a new section with the current heading
            current_section_title = element.text.strip()
            current_section_content = []
        else:
            # Append the content to the current section
            content_text = extract_text_from_element(element)
            current_section_content.append(content_text)

    # Save the last section
    if current_section_title:
        # If there was a previous section, store its content
        section_text = ' '.join(current_section_content)
        if section_text.strip():
            # Summarize the section text with longer summaries (8 sentences)
            section_summary = summarizer(section_text, num_sentences=8)
            if section_summary:
                # Remove "[" character only if it's at the end
                section_summary = remove_brackets_at_end(section_summary)
                summary_dict[current_section_title] = section_summary

    return summary_dict

def save_summaries_to_html(summaries, filename):
    with open(filename, "w", encoding="utf-8") as file:
        file.write("<html>\n<head>\n<title>Wikipedia Summaries</title>\n</head>\n<body>\n")
        for section_title, section_summary in summaries.items():
            file.write(f"<h2>{section_title}</h2>\n")
            file.write(f"<p>{section_summary}</p>\n")
        file.write("</body>\n</html>\n")
def save_summaries_to_text(summaries, filename):
    with open(filename, "w", encoding="utf-8") as file:
        for section_title, section_summary in summaries.items():
            file.write(f"{section_title}\n")
            file.write(f"{section_summary}\n\n")

def main():
    # Define the Wikipedia URL to scrape
    url = "https://en.wikipedia.org/wiki/Alexander_the_Great"

    # Scrape and summarize the Wikipedia page with longer summaries
    result = scrape_and_summarize_wikipedia(url)

    # Save the summaries to a text file
    save_summaries_to_text(result, "wikipedia_summaries.txt")

    print("Summaries saved to wikipedia_summaries.txt")

if __name__ == "__main__":
    main()


# In[ ]:




