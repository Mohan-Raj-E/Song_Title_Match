import base64

import streamlit as st
import pandas as pd

global filename
def main():
    st.title("Song Title Match")
    st.write("Upload two Excel files and process them for Song Title Match.")

    # File Upload
    uploaded_file1 = st.file_uploader("Upload Title file", type=["xlsx"])
    st.write("Upload a file containing 'Titles'. The file must be in Excel format (XLSX) with a 'Title' column.")

    uploaded_file2 = st.file_uploader("Upload Movie List file (SONG and MOVIE Column must be in the file)",
                                      type=["xlsx"])
    st.write(
        "Upload a file containing movie data. The file must be in Excel format (XLSX) with 'SONG' and 'MOVIE' columns.")
    # Add some spacing for better readability
    st.write("")  # Empty line for spacing

    if uploaded_file1 is not None and uploaded_file2 is not None:
        # Read uploaded files
        try:
            df_Title = pd.read_excel(uploaded_file1)
            df_song = pd.read_excel(uploaded_file2)
        except Exception as e:
            st.error(f"Error occurred while reading the files: {e}")
            return

        filename = st.text_input("Enter the Output filename:") + ".xlsx"

        # Process the data
        if st.button("Match Title"):
            df_song['SONG_Splitted'] = df_song['SONG'].apply(
                lambda x: ' '.join(str(x).split()[:2]) if isinstance(x, str) and len(x.split()) > 2 else x)
            df_Title['SONG'] = ''
            df_Title['MOVIE'] = ''

            for _, row in df_song.iterrows():
                song = str(row['SONG_Splitted']).lower() + ' '
                movie = str(row['MOVIE']).lower() + ' '

                for index, title in df_Title['Title'].items():
                    title_lower = str(title.lower()).replace(":", " ")

                    if song in title_lower:
                        df_Title.at[index, 'SONG'] = row['SONG']
                    if movie in title_lower:
                        df_Title.at[index, 'MOVIE'] = row['MOVIE']

            # Save the processed data
            try:
                df_Title.to_excel(filename, index=False)

                st.success(f"Processing completed and file saved")

                # Download button
                download_button = create_download_button(filename)
                st.markdown(download_button, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Error occurred while saving the file: {e}")


def create_download_button(filename):
    with open(filename, "rb") as file:
        file_content = file.read()
    base64_encoded_file = base64.b64encode(file_content).decode('utf-8')
    download_button = f'<a href="data:application/octet-stream;base64,{base64_encoded_file}" download= {filename}>Download Excel File</a>'
    return download_button


if __name__ == "__main__":
    main()
