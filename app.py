#! python3
import pandas as pd
import streamlit as st


def get_seconds(t):
    """Translates duration to seconds"""
    return int(t[: t.find(":")]) * 60 + int(t[t.find(":") + 1 :])

def get_time(s):
    h = int(s/3600)
    m = int((s%3600)/60)
    s = int((s%3600)%60)
    if s >= 3600:
        t = f'{h}:{m}:{s}'
    elif s >=60:
        t = f'{m:s}'
    else:
        t= f'{s}'


st.title("Music Report for Hindenburg")
st.markdown(
    """
**Paste your music report från Hindenburg in the field below to
get a report with the total lenght of each song used. If you chose to download it
you will get a CSV where you find the start time for each music clip in the report.**
"""
)
# Get data from clipboard
data = st.text_area(
    label="Paste your music report from Hindenburg here.",
    label_visibility="hidden",
    placeholder="Paste music report here.",
)

if data:
    rows = data.split("\n")

    # Dict to fill with info
    d = {}

    # Get data into dict
    for row in rows:
        l = row.split("\t")
        if len(l) < 3:  # Filter out empty rows
            continue
        start = str(l[0])
        title = l[2]
        duration = l[1]
        if title in d:  # If the song has been used already.
            d[title] = {
                "Starts": d[title]["Starts"] + ", " + start,
                "Duration": d[title]["Duration"] + get_seconds(duration),
                "Artist": l[3],
            }
        else:
            d[title] = {
                "Starts": start,
                "Duration": get_seconds(duration),
                "Artist": l[3],
            }

    # Put data into a dataframe.
    df = pd.DataFrame.from_dict(d, orient="index")
    df["Title"] = df.index
    df.index = [i for i in range(1, df.shape[1] + 1)]
    # CSS to inject contained in a string
    hide_table_row_index = """
                <style>
                thead tr th:first-child {display:none}
                tbody th {display:none}
                </style>
                """
    print(df)
    # Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)

    # Display as dataframe.
    st.dataframe(df[["Title", "Artist", "Duration"]])

    st.download_button(
        "Download as CSV",
        data=df[["Title", "Artist", "Duration", "Starts"]]
        .to_csv(index=False, sep=";")
        .encode("utf-8"),
        file_name="music_report.csv",
        mime="text/csv",
        key="download-csv",
    )