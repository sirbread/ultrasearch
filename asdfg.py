import streamlit as st
import asyncio
import random
import base64
from libgen_api_modern import LibgenSearch
import pandas as pd

from tools.image_downloader import async_download_image
import tools.hide_st as hide_st

st.set_page_config(
    layout="centered", page_title="UltraSearch", page_icon="🔎",
    initial_sidebar_state="collapsed")



@st.cache_data(ttl=60)
def rnd_image_load():
    image_filenames = ["images/books-ultra.webp",
                    "images/left-search-ultra.webp",
                    "images/right-search-ultra.webp",
                    ]
    random_image_filename = random.choice(image_filenames)
    with open(random_image_filename, "rb") as file_:
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
    return data_url

colA, colB, colC = st.columns([0.2, 0.6, 0.2])

data_url = rnd_image_load()
colB.markdown(
    f'''
    <img src="data:image/gif;base64,{data_url}" alt="UltraSearch Logo" style="width: 100%; height: auto; margin-top: calc(15%); margin-bottom: 10%;">
    ''',
    unsafe_allow_html=True)
colB.write()

s = LibgenSearch()

async def search_books(search_type: str, query: str, file_type: str, english_only: bool) -> list[dict]:
    filters = {}
    if search_type in ["Author", "Title"] and filters:
        results = await s.search_filtered(query, filters, search_type=search_type.lower(), exact_match=False)
    elif search_type in ["Author", "Title"] and not filters:
        results = await s.search(query, search_type=search_type.lower())

    filtered_results = []
    for book in results:
        if (file_type == 'Any' or (file_type == 'EPUBs only' and book['Extension'] == 'epub') or (file_type == 'PDFs only' and book['Extension'] == 'pdf')) and (not english_only or book['Language'] == 'English'):
            filtered_results.append(book)
    return filtered_results

async def download_image(url: str):
    return await async_download_image(url)

async def display_results(results):
    for i, book in enumerate(results, start=1):
        with st.spinner(f'Gathering knowledge... &emsp; {i}/{len(results)}'):
            image_path = await download_image(book['Cover'])
            # Columns for response
            left, mid, right = st.columns([0.8, 3, 1], gap="small")
            left.image(image_path)

            mid.caption(f"**Year:** {book['Year']}&emsp;**Pages:** {book['Pages']}&emsp;**Size:** {book['Size']}&emsp;**Extension**: {book['Extension']}")
            mid.write(f"[**{book['Title']}**]({book['Direct Download Link 1']})")
            mid.write(f"*{book['Author(s)']}*")

            # Display the download links as "Link 1", "Link 2", "Link 3"
            for i in range(1, 4):  # Loop through 1, 2, 3
                key = f"Direct Download Link {i}"  # Construct the key dynamically
                if key in book:  # Check if the key exists in the book dictionary
                    right.markdown(f"[Download Link {i}]({book[key]})")
            st.divider()

async def main():
    filters = {}
    col1, col2, col3 = st.columns([0.32, 0.52, 0.18], gap="small")

    search_type = col1.radio("Search by:", ["Title", "Author"], index=0, horizontal=True, label_visibility="collapsed")
    file_type = col2.radio('File Extension:', ['Any', 'EPUBs only', 'PDFs only'], index=0, horizontal=True, label_visibility="collapsed")
    english_only = col3.checkbox('English Only', value=True)

    colX, colY = st.columns([0.999, 0.001], gap="small")

    query = colX.text_input(label=f"Search {search_type}:",
                            placeholder=f"Search {search_type}",
                            help="Search is case and symbol sensitive.",
                            label_visibility="collapsed")

    if file_type == 'EPUBs only':
        filters['Extension'] = 'epub'
    elif file_type == 'PDFs only':
        filters['Extension'] = 'pdf'
    if english_only:
        filters['Language'] = 'English'

    if colY.button("🔎"):
        with st.spinner('Searching...'):
            results = await search_books(search_type, query, file_type, english_only)
        if results:
            #st.write(results)
            #st.dataframe(results, use_container_width=True) ## df of the results

            new_results = pd.DataFrame(results)
            new_results.fillna({'Year':'NA'}, inplace=True)

            st.info(f"Showing results for {len(results)} items")
            st.divider()
            await display_results(results)
        else:
            st.info("None found. Search another?")


    hide_st.header()
    hide_st.footer()

if __name__ == "__main__":
    asyncio.run(main())
#