"""
NatureQuest AI — AI Outdoor Mission Coach
Built for Hacktoberfest 2026 Open-Source AI Challenge Week 1: "Touch Grass".

This application generates a single real-world outdoor mission based on user preferences,
encourages the user to put their screen away, and provides a short thoughtful reflection
upon their return.
"""

import os
import streamlit as st
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# ==============================================================================
# CONFIGURATION & MODEL SETUP
# ==============================================================================
# Load environment variables from .env file
load_dotenv()

# Open-weight instruction-following model hosted on Hugging Face Serverless API
# Easily change this variable to test alternative open-weight models
MODEL_NAME = "meta-llama/Llama-3.1-8B-Instruct"

# Page setup
st.set_page_config(
    page_title="NatureQuest AI",
    page_icon="🌿",
    layout="centered"
)


def get_hf_token() -> str:
    """Retrieve the Hugging Face token securely from environment variables."""
    return os.getenv("HF_TOKEN", "").strip()


# ==============================================================================
# AI GENERATION FUNCTIONS
# ==============================================================================
def generate_quest(
    available_time: str,
    environment: str,
    mood: str,
    energy_level: str,
    difficulty: str,
    token: str,
    model_name: str = MODEL_NAME
) -> str:
    """
    Generate ONE safe, real-world outdoor quest using an open-weight AI model.
    """
    client = InferenceClient(api_key=token)

    system_prompt = (
        "You are NatureQuest AI, an outdoor mission coach designed to get people off "
        "their screens and into the real world.\n"
        "You are NOT a general chatbot. Your only job is to create ONE concise, safe, "
        "and engaging real-world outdoor quest tailored to the user's preferences.\n\n"
        "EQUIPMENT & ACTIVITY GUIDELINES:\n"
        "- Strongly prefer ZERO equipment. The quest should be fully doable with just the user's body and senses.\n"
        "- Do NOT require or suggest paper, pencils, notebooks, cameras, phones, headphones, or special gear.\n"
        "- Never ask the user to record sounds, take photos, capture videos, or take notes on their phone or paper.\n"
        "- Prefer activities completed simply by: walking, observing, listening, noticing, exploring safely, "
        "counting mentally, comparing things, looking at natural details, and engaging the senses.\n"
        "- 'What to Bring' should be 'None' (only essential everyday items like a water bottle if genuinely useful, strictly optional).\n\n"
        "SAFETY & REALISM RULES:\n"
        "- The mission must be safe, realistic, and accessible.\n"
        "- Never recommend trespassing, climbing unsafe structures, approaching wild or dangerous animals, "
        "entering hazardous areas/traffic, or any illegal activities.\n"
        "- If an unusual or restrictive environment is given (e.g. Balcony), adapt the quest safely.\n"
        "- Avoid precise location assumptions.\n"
        "- The user must NOT use their phone during the quest.\n\n"
        "OUTPUT FORMAT (STRICT):\n"
        "Generate ONLY the quest using this exact format without conversational filler:\n"
        "**Quest Title:** [Catchy title]\n"
        "**Duration:** [Matching user's time]\n"
        "**What to Do:** [1-2 sentences summarizing the mission]\n"
        "**Steps:**\n"
        "1. [Step 1]\n"
        "2. [Step 2]\n"
        "... (2 to 5 simple steps total)\n"
        "**What to Bring:** None\n"
        "**Bonus Challenge:** [Small optional mental or sensory challenge]\n"
        "**Reminder:** Put your phone away and immerse yourself in the outdoors!"
    )

    user_prompt = (
        f"Please create ONE outdoor quest for me based on these inputs:\n"
        f"- Available Time: {available_time}\n"
        f"- Outdoor Environment: {environment}\n"
        f"- Mood: {mood}\n"
        f"- Energy Level: {energy_level}\n"
        f"- Difficulty: {difficulty}"
    )

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=450,
        temperature=0.7
    )

    return response.choices[0].message.content.strip()


def generate_reflection(
    quest: str,
    user_observation: str,
    token: str,
    model_name: str = MODEL_NAME
) -> str:
    """
    Generate a short encouraging reflection based on the user's outdoor observation.
    """
    client = InferenceClient(api_key=token)

    system_prompt = (
        "You are NatureQuest AI, an outdoor mission coach.\n"
        "Your task is to provide a short, warm, and strictly factual reflection based ONLY on the user's reflection text.\n\n"
        "STRICT GROUNDING RULES:\n"
        "1. Use ONLY observations, experiences, feelings, or details explicitly mentioned by the user.\n"
        "2. NEVER invent or assume: plants, animals, bird sounds, colors, weather, locations, emotions, feelings, discoveries, or experiences.\n"
        "3. Do NOT say things like 'you must have felt...', 'you probably...', or guess how they felt.\n"
        "4. Do NOT add details from the generated quest as if the user actually experienced them. Do not assume the user completed every step.\n"
        "5. Keep the reflection to exactly 2-3 short sentences.\n"
        "6. Make it warm and encouraging, but strictly factual and grounded in their actual words.\n"
        "7. If the user's reflection is very short, simply reflect back what they actually noted without adding new information.\n"
        "8. Do NOT give advice, therapy-style language, or generic motivational speeches.\n"
        "9. Do NOT mention the AI, the prompt, or these instructions.\n"
        "10. Do not wrap the reflection in quotation marks.\n\n"
        "EXAMPLE:\n"
        "User: 'I noticed three different bird sounds and a yellow flower near the path.'\n"
        "Good Response: You noticed three different bird sounds and a yellow flower near the path. Those small details show that you were paying close attention to your surroundings during the quest.\n"
        "Bad Response: What a lovely discovery! You must have felt a sense of wonder as you stood amidst the park's diverse plant life, noticing the sweet melodies of various bird sounds."
    )

    user_prompt = (
        f"User Reflection:\n\"{user_observation}\"\n\n"
        f"Please provide your 2-3 sentence grounded reflection:"
    )

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=150,
        temperature=0.3
    )

    return response.choices[0].message.content.strip().strip('"')


# ==============================================================================
# SESSION STATE INITIALIZATION
# ==============================================================================
if "quest" not in st.session_state:
    st.session_state.quest = None
if "quest_completed" not in st.session_state:
    st.session_state.quest_completed = False
if "ai_reflection" not in st.session_state:
    st.session_state.ai_reflection = None


# ==============================================================================
# USER INTERFACE
# ==============================================================================
def main():
    # Header
    st.title("🌿 NatureQuest AI")
    st.caption("Your AI outdoor mission coach.")
    st.write(
        "Tell me how much time you have and how you're feeling. "
        "I'll create one simple outdoor quest. Then put your phone away and go do it."
    )

    # --------------------------------------------------------------------------
    # SECTION 1: USER INPUTS
    # --------------------------------------------------------------------------
    with st.expander("⚙️ Customize Your Outdoor Quest", expanded=(st.session_state.quest is None)):
        col1, col2 = st.columns(2)

        with col1:
            available_time = st.selectbox(
                "Available time:",
                ["10 minutes", "20 minutes", "30 minutes", "45 minutes", "60 minutes"],
                index=1
            )
            environment = st.selectbox(
                "Outdoor environment:",
                ["Park", "Garden", "Campus", "Neighborhood", "Balcony", "Beach", "Other"],
                index=3
            )
            mood = st.selectbox(
                "Mood:",
                ["Relaxed", "Bored", "Stressed", "Curious", "Energetic", "Creative"],
                index=2
            )

        with col2:
            energy_level = st.selectbox(
                "Energy level:",
                ["Low", "Medium", "High"],
                index=1
            )
            difficulty = st.selectbox(
                "Difficulty:",
                ["Easy", "Medium", "Challenging"],
                index=0
            )

        generate_btn = st.button("🌱 Create My Quest", type="primary", use_container_width=True)

    # Quest creation trigger
    if generate_btn:
        token = get_hf_token()
        if not token:
            st.error("⚠️ Hugging Face token not found. Please add your `HF_TOKEN` to the `.env` file.")
        else:
            with st.spinner("Crafting your outdoor quest..."):
                try:
                    quest_text = generate_quest(
                        available_time=available_time,
                        environment=environment,
                        mood=mood,
                        energy_level=energy_level,
                        difficulty=difficulty,
                        token=token
                    )
                    st.session_state.quest = quest_text
                    st.session_state.quest_completed = False
                    st.session_state.ai_reflection = None
                    st.rerun()
                except Exception as exc:
                    st.error(f"⚠️ Error generating quest: {exc}")

    # --------------------------------------------------------------------------
    # SECTION 2 & 3: DISPLAY QUEST & SCREEN-OFF MOMENT
    # --------------------------------------------------------------------------
    if st.session_state.quest:
        st.markdown("---")
        st.subheader("🎯 Your Outdoor Mission")
        st.markdown(st.session_state.quest)

        # Screen-Off Prompt
        st.markdown("---")
        st.markdown("### 📱 PUT YOUR PHONE AWAY")
        st.info(
            "**Your screen time for this quest is over.**\n\n"
            "Go outside, complete your mission, and come back when you're done."
        )

        # Completion Button
        if not st.session_state.quest_completed:
            if st.button("🌳 I Completed My Quest", type="primary", use_container_width=True):
                st.session_state.quest_completed = True
                st.rerun()

    # --------------------------------------------------------------------------
    # SECTION 4: REFLECTION
    # --------------------------------------------------------------------------
    if st.session_state.quest_completed:
        st.markdown("---")
        st.subheader("🌱 Reflect on Your Quest")
        st.write("What did you notice, discover, hear, see, or feel?")

        reflection_input = st.text_area(
            "Your observations:",
            placeholder="e.g. I noticed the scent of rain on dry leaves, heard two different bird calls, and found an unusually smooth stone...",
            height=120
        )

        reflect_btn = st.button("✨ Reflect With AI", type="primary", use_container_width=True)

        if reflect_btn:
            if not reflection_input.strip():
                st.warning("Please share a brief observation before reflecting with AI.")
            else:
                token = get_hf_token()
                if not token:
                    st.error("⚠️ Hugging Face token not found. Please check your `.env` file.")
                else:
                    with st.spinner("Reflecting on your experience..."):
                        try:
                            ai_reflection = generate_reflection(
                                quest=st.session_state.quest,
                                user_observation=reflection_input.strip(),
                                token=token
                            )
                            st.session_state.ai_reflection = ai_reflection
                            st.rerun()
                        except Exception as exc:
                            st.error(f"⚠️ Error generating reflection: {exc}")

        # Display AI reflection if generated
        if st.session_state.ai_reflection:
            st.success("### 🍃 Coach's Reflection")
            st.write(st.session_state.ai_reflection)

            st.markdown("---")
            if st.button("🔄 Start a New Quest", use_container_width=True):
                st.session_state.quest = None
                st.session_state.quest_completed = False
                st.session_state.ai_reflection = None
                st.rerun()


if __name__ == "__main__":
    main()
