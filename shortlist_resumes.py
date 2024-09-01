import sqlite3
from pathlib import Path
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
import pywhatkit as kit
import time

def score_resumes(job_description):
    conn = sqlite3.connect('resumes.db')
    cursor = conn.cursor()

    # Fetch all resumes with additional candidate details
    cursor.execute('SELECT id, filename, content, name, email, phone_no FROM resumes')
    resumes = cursor.fetchall()

    # Initialize Ollama embeddings (using Llama3)
    embeddings = OllamaEmbeddings(model="llama3")

    # Create a FAISS index for the job description
    job_desc_index = FAISS.from_texts([job_description], embeddings)

    # Process each resume
    results = []
    for resume_id, filename, content, name, email, phone_no in resumes:
        # Save PDF content to a temporary file
        temp_pdf = Path('temp.pdf')
        temp_pdf.write_bytes(content)
        
        # Load and process the PDF
        loader = PyPDFLoader(str(temp_pdf))
        pages = loader.load_and_split()
        
        # Combine all pages into a single text
        resume_text = ' '.join([page.page_content for page in pages])
        
        # Split the text into chunks
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        chunks = text_splitter.split_text(resume_text)
        
        # Create a FAISS index for the resume
        resume_index = FAISS.from_texts(chunks, embeddings)
        
        # Calculate similarity score
        similarity = resume_index.similarity_search_with_score(job_description, k=1)[0][1]
        
        # Append results with candidate details
        results.append((resume_id, filename, name, email, phone_no, similarity))

        # Remove the temporary file
        temp_pdf.unlink()

    # Sort results by similarity score (higher score is better)
    results.sort(key=lambda x: x[5], reverse=True)

    # Select top resumes (e.g., top 4)
    top_resumes = results[:4]

    # Send messages to shortlisted candidates using pywhatkit
    for candidate in top_resumes:
        name = candidate[2]
        phone_no = candidate[4]
        if phone_no:  # Ensure phone number is provided
            try:
                kit.sendwhatmsg_instantly(
                    phone_no=f"+91{phone_no}",  # Add country code if needed
                    message=f"""
                    Congratulations {name}!, you have been shortlisted for the next round!\n
                    You will be again contacted soon by us for further process.\n
                    Stay tuned!
                    """,
                    wait_time=30,  # Time delay to open WhatsApp Web
                    tab_close=True,  # Close the tab after sending the message
                )
                print(f"Message sent to {name} on {phone_no}.")
            except Exception as e:
                print(f"Failed to send message to {name}: {e}")

            time.sleep(5)  # Adding a delay between sending messages

    return top_resumes

if __name__ == "__main__":
    job_description = """
    We are looking for a skilled Python developer with experience in web development,
    data analysis, and machine learning. The ideal candidate should have strong 
    problem-solving skills and be familiar with popular Python frameworks and libraries.
    """
    top_resumes = score_resumes(job_description)
    for resume in top_resumes:
        print(resume)
