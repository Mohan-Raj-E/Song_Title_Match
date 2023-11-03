import base64

import streamlit as st
import pandas as pd

def main():
    st.title("Song Title Match")
    st.write("Upload two Excel files and process them for Song Title Match.")

    # File Upload
    uploaded_file1 = st.file_uploader("Upload Title file", type=["xlsx"])
    uploaded_file2 = st.file_uploader("Upload Movie List file", type=["xlsx"])

    if uploaded_file1 is not None and uploaded_file2 is not None:
        # Read uploaded files
        try:
            df_Title = pd.read_excel(uploaded_file1)
            df_song = pd.read_excel(uploaded_file2)
        except Exception as e:
            st.error(f"Error occurred while reading the files: {e}")
            return

        # Process the data
        if st.button("Match Title"):
            #df_song['SONG_Splitted'] = df_song['SONG'].apply(lambda x: ' '.join(x.split()[:2]) if len(x.split()) > 2 else x)
            df_song['SONG_Splitted'] = df_song['SONG'].apply(lambda x: ' '.join(str(x).split()[:2]) if isinstance(x, str) and len(x.split()) > 2 else x)
            df_Title['SONG'] = ''
            df_Title['MOVIE'] = ''

            for _, row in df_song.iterrows():
                # song = row['SONG_Splitted'].lower() + ' '
                # movie = row['MOVIE'].lower() + ' '
                song = str(row['SONG_Splitted']).lower() + ' '
                movie = str(row['MOVIE']).lower() + ' '

                for index, title in df_Title['Title'].items():
                    title_lower = title.lower().replace(":", " ")

                    if song in title_lower:
                        df_Title.at[index, 'SONG'] = row['SONG']
                    if movie in title_lower:
                        df_Title.at[index, 'MOVIE'] = row['MOVIE']

            # Save the processed data
            try:
                filename = str(df_song['LANGUAGE'].mode().iloc[0])  # Get the mode and convert it to a string
                df_Title.to_excel(filename + ".xlsx", index=False)
                
                st.success(f"Processing completed and file saved as {filename}.xlsx")

                # Download button
                download_button = create_download_button(filename + ".xlsx")
                st.markdown(download_button, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error occurred while saving the file: {e}")


def create_download_button(file_path):
    with open(file_path, "rb") as file:
        file_content = file.read()
    base64_encoded_file = base64.b64encode(file_content).decode('utf-8')
    download_button = f'<a href="data:application/octet-stream;base64,{base64_encoded_file}" download="Bengali_Songs.xlsx">Download Excel File</a>'
    return download_button


if __name__ == "__main__":
    main()
