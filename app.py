# Save this as app.py
import streamlit as st
from sias_core import sias_pipeline # Importing the brain I built earlier

# Setting up the website's title and look
st.set_page_config(page_title="SIAS Testing Simulator", page_icon="🛡️")
st.title(" SIAS V2.0 Threat Simulator")
st.write("Paste a text message below to simulate how the SIAS engine processes threats.")

# Creating the text box for the user to type in
user_message = st.text_area("Incoming SMS Message:", placeholder="Type or paste text here...")

# Creating the "Scan" button
if st.button("Analyze Threat"):
    if user_message:
        with st.spinner("Analyzing heuristics, neural vibe, and URLs..."):
            # Here I send the text to our pipeline
            result = sias_pipeline(user_message)
            
            # Displaying the results visually
            st.subheader(f"Verdict: {result['classification']}")
            st.write(f"**Action Taken:** {result['action']}")
            
            # Breaking down the math for the testers
            st.markdown("### Under the Hood (Risk Breakdown)")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Heuristic Risk", result['heuristic_risk'])
            col2.metric("Neural Risk", result['neural_risk'])
            col3.metric("URL Sandbox", result['url_risk'])
            col4.metric("FINAL SCORE", f"{result['final_score']} / 10")
    else:
        st.warning("Please enter a message to scan.")