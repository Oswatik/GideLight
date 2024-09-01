import streamlit as st
import sqlite3
from streamlit_option_menu import option_menu
from templates import home_page
from shortlist_resumes import score_resumes
from candidate_help import chatbot_response 
from admin_help import assisting_chatbot

# Function to store the uploaded resume in the database
def store_resume_in_db(filename, content, name, email, phone_no):
    conn = sqlite3.connect('resumes.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO resumes (filename, content, name, email, phone_no)
        VALUES (?, ?, ?, ?, ?)
    ''', (filename, content, name, email, phone_no))

    conn.commit()
    conn.close()
    st.success("Resume uploaded and stored successfully!")

# Candidate page: Upload resume and Chatbot
def candidate_page():

    st.header("Candidate Portal")

    # Tabs for resume upload and chatbot
    selected_tab = st.selectbox("Select an option:", ["Upload Resume", "Help"])

    if selected_tab == "Upload Resume":
        st.subheader("Upload Resume")
        name = st.text_input("Enter your name")
        email = st.text_input("Enter your email")
        phone_no = st.text_input("Enter your phone number")
        uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])

        if st.button("Submit"):
            if uploaded_file is not None:
                content = uploaded_file.read()
                filename = uploaded_file.name
                store_resume_in_db(filename, content, name, email, phone_no)
            else:
                st.error("Please upload a PDF file.")
    
    elif selected_tab == "Help":
        st.subheader("Chill Guy")
        st.write("Ask any questions you have regarding the job application process to Chill Guy, he is cool enough to help-")
        
        # Input for user's question
        user_query = st.text_input("Enter your query here:")
        
        # When the user submits a query
        if user_query:
            with st.spinner("He is thinking..."):
                response = chatbot_response(user_query)
            st.write(f"**Chill Guy:** {response}")

# Admin page: View database
# Admin page: View database or shortlist candidates
def admin_page():
    st.header("Admin Page")

    # Create a selectbox with options
    admin_choice = st.selectbox("Select an option", ["View database", "Shortlist candidates", "Manage database", "Assist"])

    if admin_choice == "View database":
        conn = sqlite3.connect('resumes.db')
        cursor = conn.cursor()

        cursor.execute('SELECT id, filename, name, email, phone_no FROM resumes')
        rows = cursor.fetchall()

        if rows:
            for row in rows:
                st.write(f"ID: {row[0]}, Filename: {row[1]}")
                st.write(f"Name: {row[2]}, Email: {row[3]}, Phone No.: {row[4]}")
                st.write("---")
        else:
            st.write("No resumes found in the database.")

        conn.close()

    elif admin_choice == "Shortlist candidates":
        st.subheader("Shortlist Candidates")

        # Input for job description
        job_description = st.text_area("Enter job description", height=150)

        if st.button("Shortlist Candidates"):
            if job_description:
              st.write("Shortlisting candidates...")
              shortlisted_candidates = score_resumes(job_description)

        # Display shortlisted candidates
              st.write("Top resumes:")
              for candidate in shortlisted_candidates:
                  st.write(f"ID: {candidate[0]}, Filename: {candidate[1]}, Name: {candidate[2]}, Email: {candidate[3]}, Phone No.: {candidate[4]}, Score: {candidate[5]}")
                  st.write("---")

        # Message candidates
              st.write("Messages sent to all shortlisted candidates.")
            else:
               st.error("Please enter a job description.")

    elif admin_choice == "Manage database":
        manage_database()

    elif admin_choice == "Assist":
        st.subheader("Reliable Guy")
        st.write("Welcome HR! Reliable guy will assist or help you with anything-")
        
        # Input for user's question
        user_query = st.text_input("Enter your question:")
        
        # When the user submits a query
        if user_query:
            with st.spinner("He is thinking..."):
                response = chatbot_response(user_query)
            st.write(f"**Reliable Guy:** {response}")


def manage_database():
    st.subheader("Manage Database")

    conn = sqlite3.connect('resumes.db')
    cursor = conn.cursor()

    action = st.radio("Select Action", ("Edit", "Delete"))

    if action == "Edit":
        resume_id = st.number_input("Enter Resume ID to Edit", min_value=1)
        if st.button("Load Record"):
            cursor.execute('SELECT filename, name, email, phone_no FROM resumes WHERE id = ?', (resume_id,))
            record = cursor.fetchone()

            if record:
                filename, name, email, phone_no = record
                new_name = st.text_input("Name", value=name)
                new_email = st.text_input("Email", value=email)
                new_phone_no = st.text_input("Phone No.", value=phone_no)

                if st.button("Update Record"):
                    cursor.execute('''
                        UPDATE resumes
                        SET name = ?, email = ?, phone_no = ?
                        WHERE id = ?
                    ''', (new_name, new_email, new_phone_no, resume_id))
                    conn.commit()  # Ensure changes are committed
                    st.success(f"Resume ID {resume_id} updated successfully!")
                else:
                    st.warning("Make sure to click the 'Update Record' button after editing the fields.")
            else:
                st.error("Record not found.")

    elif action == "Delete":
        resume_id = st.number_input("Enter Resume ID to Delete", min_value=1)
        if st.button("Delete Record"):
            cursor.execute('DELETE FROM resumes WHERE id = ?', (resume_id,))
            conn.commit()  # Ensure changes are committed
            st.success(f"Resume ID {resume_id} deleted successfully!")

    conn.close()


# Main function to control the app
def main():
    st.set_page_config(layout="wide")
    
    # Create a horizontal navigation bar
    selected = option_menu(
        menu_title=None,
        options=["Home", "Candidate", "Admin"],
        icons=["house", "person", "lock"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal"
    )

    if selected == "Home":
        home_page()
    elif selected == "Candidate":
        candidate_page()
    elif selected == "Admin":
        admin_page()

if __name__ == "__main__":
    main()










## AUthentication test code

# import streamlit as st
# import streamlit_authenticator as stauth

# credentials = {
#     'usernames': {
#         'oswat': {
#             "name": 'Swatik',
#             "password": '123456', 
#         }
#     }
# }

# names = ['John Smith','Rebecca Briggs']
# usernames = ['jsmith','rbriggs']
# passwords = ['123','456']

# # hashed_passwords = stauth.hasher(passwords).generate()

# authenticator = stauth.Authenticate(
#     credentials, 
#     "Swatik", 
#     "Swatik", 
#     cookie_expiry_days=30
# )

# name, authentication_status, usernames = authenticator.login('main', key='Login')

# if authentication_status == True:
#     st.write('Welcome!')
#     st.title('Some content')
# elif authentication_status == False:
#     st.error('Username/password is incorrect')
# elif authentication_status == None:
#     st.warning('Please enter your username and password')

# if st.session_state['authentication_status'] == True:
#     st.write('Welcome *%s*' % (st.session_state['name']))
#     st.title('Some content')
# elif st.session_state['authentication_status'] == False:
#     st.error('Username/password is incorrect')
# elif st.session_state['authentication_status'] == None:
#     st.warning('Please enter your username and password')

# import streamlit as st
# import streamlit_authenticator as stauth

# # Correct credentials format
# credentials = {
#     "usernames": {
#         "admin": {   # <-- This is the username
#             "name": "Admin",
#             "password": "123456",  # <-- This is the password
#         }
#     }
# }

# # Create an authenticator object
# authenticator = stauth.Authenticate(
#     credentials, 
#     "cookie_name", 
#     "signature_key", 
#     cookie_expiry_days=30
# )

# # Authentication process
# username, authentication_status, password = authenticator.login("main", "Login")

# if authentication_status:
#     authenticator.logout("Logout", "sidebar")
    
#     if username == "admin":
#         # Admin Page
#         st.title("Admin Dashboard")
#         st.subheader("Welcome!")
#         st.write("This is the admin page, accessible only to authenticated users.")
# else:
#     # User Page
#     st.title("Candidate Page")
#     st.subheader("Welcome to the Candidate Portal")
#     st.write("This is the user page, accessible to all visitors.")

# if authentication_status is False:
#     st.error("Username/password is incorrect")

# elif authentication_status is None:
#     st.warning("Please enter your username and password")