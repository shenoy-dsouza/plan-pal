import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
)

import streamlit as st
from app.planner.plan_generator import TravelPlanner  # adjust this import

st.set_page_config(page_title="PlanPal - AI Travel Planner", layout="centered")

st.title("🌍 PlanPal")
st.markdown(
    "<h5 style='margin-top:-15px; color: gray;'>Where Planning Meets Adventure</h5>",
    unsafe_allow_html=True,
)

with st.form("trip_form"):
    destination = st.text_input("Destination", placeholder="e.g., Goa")
    budget = st.number_input("Total Budget (INR)", min_value=1000, step=500)
    days = st.number_input("Number of Days", min_value=1, step=1)
    style = st.selectbox(
        "Travel Style",
        ["general", "luxury", "backpacking", "chill", "adventure", "family"],
    )

    submitted = st.form_submit_button("Plan My Trip")

if submitted:
    if not destination or not budget or not days:
        st.warning("Please fill all fields.")
    else:
        with st.spinner("Planning your trip... ✈️"):
            try:
                planner = TravelPlanner()
                result = planner.plan_trip(
                    destination, int(budget), int(days), style.lower()
                )
                if isinstance(result, dict):
                    if result.get("status") == "error":
                        st.error(
                            f"Error: {result.get('message', 'Unknown error')}"
                        )
                        st.info(
                            f"Solution: {result.get('solution', 'Please try again')}"
                        )
                    else:
                        # Display the complete plan
                        st.subheader("✨ Your Personalized Travel Plan")

                        # Display sections if available
                        sections = result.get("sections", {})
                        if sections:
                            st.markdown(
                                sections.get("planner", ""),
                                unsafe_allow_html=True,
                            )
                            with st.expander("Detailed Itinerary"):
                                st.markdown(
                                    sections.get("itinerary", ""),
                                    unsafe_allow_html=True,
                                )
                            with st.expander("Budget Breakdown"):
                                st.markdown(
                                    sections.get("budget", ""),
                                    unsafe_allow_html=True,
                                )
                            with st.expander("Recommendations"):
                                st.markdown(
                                    sections.get("recommendations", ""),
                                    unsafe_allow_html=True,
                                )
                            with st.expander("Travel Tips"):
                                st.markdown(
                                    sections.get("tips", ""),
                                    unsafe_allow_html=True,
                                )
                else:
                    st.markdown(str(result), unsafe_allow_html=True)

            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")
                st.info(
                    "Please try again with different parameters or contact support."
                )
