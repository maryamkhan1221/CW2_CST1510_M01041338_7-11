import streamlit as st
import pandas as pd
from openai import OpenAI

# Display an error message showing which file loaded the assistant
st.error(f"ASSISTANT BOT LOADED FROM: {__file__}")

# Create and return an OpenAI client using the API key from Streamlit secrets
def _client():
    return OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Generate a short text summary of the dataframe
def _df_summary(df: pd.DataFrame) -> str:
    cols = list(df.columns)
    lines = [f"Rows: {len(df)}", f"Columns: {', '.join(cols)}"]

    # For object/string columns, find the most common value
    for c in cols:
        if df[c].dtype == "object" and len(df) > 0:
            try:
                lines.append(f"Top {c}: {df[c].value_counts().idxmax()}")
            except Exception:
                pass

    return "\n".join(lines)

# Render the AI assistant UI for a specific page and dataframe
def render_assistant(df: pd.DataFrame, page_name: str):
    st.markdown("---")
    st.subheader(f"🤖 OpenAI Assistant — {page_name}")

    # Unique key for storing chat history per page
    hist_key = f"chat_msgs_{page_name}"

    # Initialize chat history if it does not exist
    if hist_key not in st.session_state:
        st.session_state[hist_key] = []

    # System prompt that defines assistant behavior and dataset context
    system_prompt = (
        "You are an AI assistant inside a Streamlit dashboard.\n"
        f"Context: {page_name}\n\n"
        "Dataset summary:\n"
        f"{_df_summary(df)}\n\n"
        "Rules:\n"
        "- Be clear and concise.\n"
        "- Do not invent columns.\n"
    )

    # Display previous chat messages
    for m in st.session_state[hist_key]:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    # Button to clear the chat history
    if st.button("Clear Chat", use_container_width=True, key=f"clear_{page_name}"):
        st.session_state[hist_key] = []
        st.rerun()

    # Input box for user messages
    user_msg = st.chat_input("Ask the AI (e.g. 'summarize', 'risks', 'priorities')")

    if user_msg:
        # Store and display user message
        st.session_state[hist_key].append({"role": "user", "content": user_msg})
        with st.chat_message("user"):
            st.markdown(user_msg)

        # Combine system prompt with conversation history
        messages = [{"role": "system", "content": system_prompt}] + st.session_state[hist_key]

        try:
            # Send the conversation to OpenAI
            resp = _client().chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.3,
            )
            reply = resp.choices[0].message.content
        except Exception as e:
            reply = f"OpenAI error: {e}"

        # Store and display assistant response
        st.session_state[hist_key].append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply)
