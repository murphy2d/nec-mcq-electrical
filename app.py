import os
import json
import streamlit as st

st.set_page_config(page_title="NEC Electrical Engineering Prep", page_icon="⚡", layout="wide")

# NEC Syllabus Mapping
SYLLABUS = {
    "1. Fundamental of Electrical Engineering": {
        "1.1 Basic circuit concept": "sub_1.1.json",
        "1.2 Network theorems": "sub_1.2.json",
        "1.3 Alternating current fundamentals": "sub_1.3.json",
        "1.4 Electric circuit responses": "sub_1.4.json",
        "1.5 AC series and parallel circuits": "sub_1.5.json",
        "1.6 Three phase systems": "sub_1.6.json",
    },
    "2. Electrical Machines": {
        "2.1 Magnetic circuits": "sub_2.1.json",
        "2.2 Transformers": "sub_2.2.json",
        "2.3 DC machines": "sub_2.3.json",
        "2.4 Synchronous machines": "sub_2.4.json",
        "2.5 Three phase induction motors": "sub_2.5.json",
        "2.6 Single phase induction motor": "sub_2.6.json",
    },
    "3. Power Plants Engineering": {
        "3.1 Hydroelectric power plants": "sub_3.1.json",
        "3.2 Diesel electric power plants": "sub_3.2.json",
        "3.3 Non-conventional power generation": "sub_3.3.json",
        "3.4 Energy storages": "sub_3.4.json",
        "3.5 Excitation systems": "sub_3.5.json",
        "3.6 Starting of generators": "sub_3.6.json",
    },
    "4. Electrical Measurements and Instrumentations": {
        "4.1 Measurement and error": "sub_4.1.json",
        "4.2 Measuring instruments": "sub_4.2.json",
        "4.3 Transducers and sensors": "sub_4.3.json",
        "4.4 Analog to digital and digital to analog converters": "sub_4.4.json",
        "4.5 Digital instrumentation": "sub_4.5.json",
        "4.6 Instrument transformers": "sub_4.6.json",
    },
    "5. Power Electronics and Control": {
        "5.1 Control system fundamentals": "sub_5.1.json",
        "5.2 Time domain analysis": "sub_5.2.json",
        "5.3 Frequency domain analysis": "sub_5.3.json",
        "5.4 Power semiconductor switches": "sub_5.4.json",
        "5.5 Power converters": "sub_5.5.json",
        "5.6 Applications of power electronics": "sub_5.6.json",
    },
    "6. Power System Protection": {
        "6.1 Fuses, isolators and reactors": "sub_6.1.json",
        "6.2 Circuit breakers": "sub_6.2.json",
        "6.3 Protective relays": "sub_6.3.json",
        "6.4 Lightning protection": "sub_6.4.json",
        "6.5 Earthing": "sub_6.5.json",
        "6.6 Substations": "sub_6.6.json",
    },
    "7. Transmission and Distribution Lines": {
        "7.1 Transmission lines": "sub_7.1.json",
        "7.2 Transmission lines circuit selection": "sub_7.2.json",
        "7.3 Mechanical design of overhead line": "sub_7.3.json",
        "7.4 Electrical loads": "sub_7.4.json",
        "7.5 Distribution systems": "sub_7.5.json",
        "7.6 Voltage regulation and power factor correction": "sub_7.6.json",
    },
    "8. Utilization of Electrical Energy": {
        "8.1 Illumination": "sub_8.1.json",
        "8.2 Electrical design and estimation": "sub_8.2.json",
        "8.3 Tariff schemes": "sub_8.3.json",
        "8.4 Electric drives and motor selection": "sub_8.4.json",
        "8.5 Electric heating": "sub_8.5.json",
        "8.6 Electric traction": "sub_8.6.json",
    },
    "9. Power System Analysis": {
        "9.1 Transmission line parameters": "sub_9.1.json",
        "9.2 Performance of transmission line": "sub_9.2.json",
        "9.3 Fault calculations": "sub_9.3.json",
        "9.4 Load flow": "sub_9.4.json",
        "9.5 Stability analysis": "sub_9.5.json",
        "9.6 Voltage control and VAR compensation": "sub_9.6.json",
    },
    "10. Project Planning, Design and Implementation": {
        "10.1 Engineering drawings and its concepts": "sub_10.1.json",
        "10.2 Engineering Economics": "sub_10.2.json",
        "10.3 Project planning and scheduling": "sub_10.3.json",
        "10.4 Project management": "sub_10.4.json",
        "10.5 Engineering professional practice": "sub_10.5.json",
        "10.6 Engineering Regulatory Body": "sub_10.6.json",
    }
}

# --- State Management ---
if "submitted_answers" not in st.session_state:
    st.session_state.submitted_answers = {}  # {q_id: (user_choice, is_correct)}
if "submitted_batches" not in st.session_state:
    st.session_state.submitted_batches = set() # Track submitted batch indices
if "current_batch" not in st.session_state:
    st.session_state.current_batch = 0

# --- App Layout ---
st.title("⚡ NEC Electrical Engineering Practice Portal")

# Sidebar Navigation
st.sidebar.header("Navigation")
selected_chapter = st.sidebar.selectbox("Select Chapter", list(SYLLABUS.keys()))
subchapters = SYLLABUS[selected_chapter]
selected_subchapter = st.sidebar.radio("Select Sub-chapter", list(subchapters.keys()))

# Reset batch context when switching subchapters
if "active_subchapter" not in st.session_state or st.session_state.active_subchapter != selected_subchapter:
    st.session_state.active_subchapter = selected_subchapter
    st.session_state.current_batch = 0

# Determine Target File Path
chap_num = selected_chapter.split('.')[0]
json_filename = subchapters[selected_subchapter]
file_path = os.path.join("data", f"chapter_{chap_num}", json_filename)

st.header(f"{selected_subchapter}")

if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        all_questions = data.get("questions", [])

    total_q = len(all_questions)

    if total_q > 0:
        # Batch Settings
        batch_size = st.sidebar.select_slider("Questions per batch:", options=[5, 10, 15, 20], value=10)
        num_batches = (total_q + batch_size - 1) // batch_size
        
        # Batch Selector Dropdown
        batch_options = [f"Batch {i+1} (Q{i*batch_size + 1} - Q{min((i+1)*batch_size, total_q)})" for i in range(num_batches)]
        selected_batch_idx = st.selectbox("Select Question Batch:", range(num_batches), format_func=lambda x: batch_options[x], index=st.session_state.current_batch)
        st.session_state.current_batch = selected_batch_idx

        # Extract Batch Questions
        start_idx = selected_batch_idx * batch_size
        end_idx = min(start_idx + batch_size, total_q)
        current_questions = all_questions[start_idx:end_idx]

        # Overall Subchapter Score Header
        answered_count = len(st.session_state.submitted_answers)
        correct_count = sum(1 for v in st.session_state.submitted_answers.values() if v[1])
        
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("Total Subchapter Questions", total_q)
        col_m2.metric("Questions Attempted", f"{answered_count}/{total_q}")
        col_m3.metric("Overall Score", f"{correct_count}/{answered_count}" if answered_count > 0 else "0/0", 
                      delta=f"{(correct_count/answered_count)*100:.1f}%" if answered_count > 0 else "0%")

        st.divider()

        # Check batch submission status
        batch_key = f"{selected_subchapter}_batch_{selected_batch_idx}"
        is_batch_submitted = batch_key in st.session_state.submitted_batches

        # Questions Display
        temp_user_choices = {}
        for q in current_questions:
            q_id = q["id"]
            st.markdown(f"#### Question {q_id}: {q['question']}")

            already_answered = q_id in st.session_state.submitted_answers
            saved_choice, is_correct = st.session_state.submitted_answers.get(q_id, (None, False))

            default_idx = None
            if saved_choice:
                for idx, opt in enumerate(q["options"]):
                    if opt.startswith(saved_choice):
                        default_idx = idx
                        break

            # Radio Input
            user_choice = st.radio(
                "Options:",
                q["options"],
                index=default_idx,
                key=f"radio_{q_id}",
                disabled=is_batch_submitted
            )
            
            if user_choice:
                temp_user_choices[q_id] = user_choice[0]

            # Feedback Display (Show results if batch is submitted)
            if is_batch_submitted and already_answered:
                if is_correct:
                    st.success(f"✅ **Correct!** (Answer: {q['answer']})")
                else:
                    st.error(f"❌ **Incorrect.** Your answer: {saved_choice} | Correct answer: **{q['answer']}**")
                
                # Collapsed explanation by default
                with st.expander("💡 View Explanation & Calculation", expanded=False):
                    st.write(q["explanation"])

            st.divider()

        # Batch Controls (Bottom)
        col_sub, col_retry = st.columns([2, 2])
        with col_sub:
            if not is_batch_submitted:
                if st.button("Check Batch Answers", type="primary", use_container_width=True):
                    if len(temp_user_choices) < len(current_questions):
                        st.warning("Please answer all questions in this batch before submitting!")
                    else:
                        for q in current_questions:
                            q_id = q["id"]
                            u_choice = temp_user_choices[q_id]
                            correct_choice = q["answer"]
                            st.session_state.submitted_answers[q_id] = (u_choice, u_choice == correct_choice)
                        st.session_state.submitted_batches.add(batch_key)
                        st.rerun()
            else:
                if st.button("Retry This Batch", use_container_width=True):
                    for q in current_questions:
                        q_id = q["id"]
                        if q_id in st.session_state.submitted_answers:
                            del st.session_state.submitted_answers[q_id]
                    st.session_state.submitted_batches.remove(batch_key)
                    st.rerun()

        # Navigation Controls
        nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])
        with nav_col1:
            if selected_batch_idx > 0:
                if st.button("⬅️ Previous Batch"):
                    st.session_state.current_batch -= 1
                    st.rerun()
        with nav_col3:
            if selected_batch_idx < num_batches - 1:
                if st.button("Next Batch ➡️"):
                    st.session_state.current_batch += 1
                    st.rerun()

    else:
        st.warning("No questions found in this dataset.")
else:
    st.info("📌 Content for this subchapter is not uploaded yet. Use `generate_json.py` to add it.")