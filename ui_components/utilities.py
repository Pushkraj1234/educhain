import json
import streamlit as st


def render_chapter(chapter_id, json_path):
    # Load the JSON data
    with open(json_path, 'r') as f:
        data = json.load(f)

    # Traverse each chapter in the data
    for chapter in data['chapters']:
        # Check if the chapter's id is the id that we're looking for
        if chapter['chapterId'] == chapter_id:
            # Display the chapter title
            st.title(chapter['chapterTitle'])

            # Display each section of the chapter
            for section in chapter['sections']:
                st.header(section['sectionTitle'])
                if 'content' in section:
                    st.markdown(section['content'])
                if 'code' in section:
                    st.code(section['code'])

                # Display each subsection of the chapter
                if 'subsections' in section:
                    for subsection in section['subsections']:
                        st.subheader(subsection['subsectionTitle'])
                        if 'content' in subsection:
                            st.markdown('*' + subsection[
                                'content'] + '*')  # Wrapping the content inside asterisks will italicize the text in markdown
                        if 'image' in subsection:
                            st.image(subsection['image'])
                        if 'code' in subsection:
                            st.code(subsection['code'])