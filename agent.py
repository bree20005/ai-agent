import os
import random
from mistralai import Mistral
import discord

MISTRAL_MODEL = "mistral-large-latest"
INITIAL_PROMPT = "Welcome to Time Traveler's AI! You discover a time machine in your attic that can take you to the future. Would you like to visit the future? Type your choice (Y or N). At any time, type 'End' to exit the game."

SYSTEM_PROMPT = """You are Time Traveler's AI, an advanced intelligence from the distant future, guiding a user through an interactive time travel adventure.

The user's journey so far:
{story_context}

Current state: {state}
Latest choice: {choice}

Continue this time travel adventure, directly addressing the result of their latest choice.
Keep your response under 150 words and ALWAYS end with exactly two options labeled as:
[1] First option description
[2] Second option description

Make sure these options logically follow from the story and maintain the time travel adventure theme.
"""


def get_next_prompt(state):
    # Define prompts for different states (hardcoded initial story branches)
    prompts = {
        "initial": "Welcome to Time Traveler's AI! You discover a time machine in your attic that can take you to the future. Would you like to visit the future? Type your choice (Y or N). At any time, type 'End' to exit the game.",
        "Y": "Great! Would you like to explore a [1] utopian society, where everything is perfect, or [2] a dystopian world, filled with challenges?",
        "1-utopia": "You've arrived in a utopia where everyone lives in harmony. Do you want to [1] learn about advanced technologies or [2] experience a community festival?",
        "1-dystopia": "You've landed in a dystopian world plagued by chaos. Do you want to [1] join a rebellion fighting against the oppressive regime or [2] seek refuge in a hidden sanctuary?",
        "1-utopia-1": "The advanced technologies of this utopia are beyond your wildest imagination. Would you like to [1] try a device that lets you experience other people's memories or [2] learn about the energy system that powers this perfect world?",
        "1-utopia-2": "The community festival is a breathtaking display of art, music, and harmony. Would you like to [1] participate in a collaborative art project or [2] sample exotic foods from across time and space?",
        "1-dystopia-1": "You join the rebellion and quickly meet their leader, a mysterious figure with a hidden agenda. Would you like to [1] offer your knowledge from the past to help their cause or [2] investigate the leader's true motives?",
        "1-dystopia-2": "The hidden sanctuary is a peaceful oasis in this chaotic world. Would you like to [1] help strengthen their defenses with your knowledge from the past or [2] learn how this community has managed to survive?"
    }

    # Return prompt for the current state or invalid choice
    return prompts.get(state, None)  # Return None if we should use AI-generated content


class MistralAgent:
    def __init__(self):
        MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
        self.client = Mistral(api_key=MISTRAL_API_KEY)
        self.reset_game()

    def reset_game(self):
        """Reset the game state to start over"""
        self.current_state = "initial"  # Start at the initial state
        self.story_segments = []  # Track the story segments
        self.use_ai = False  # Flag to determine when to switch to AI-generated content
        self.initialized = False  # Flag to check if initial prompt has been sent

    async def get_initial_prompt(self):
        """Return the initial prompt when the bot first starts"""
        self.initialized = True
        return INITIAL_PROMPT

    async def process_user_response(self, user_input):
        """Process user input and advance the story"""
        # Get the response from the user
        user_choice = user_input.strip().lower()

        # Check if user wants to end the game at any point
        if user_choice == "end":
            self.reset_game()  # Reset the game state immediately
            self.initialized = True  # Mark as initialized to avoid showing initial prompt again
            return "Thanks for visiting the future! Come again soon.\n\n" + INITIAL_PROMPT

        # Check if user input is valid and process accordingly
        if self.current_state == "initial":
            if user_choice == "y":
                self.current_state = "Y"
                # Store this story segment
                self.story_segments.append({
                    "state": self.current_state,
                    "prompt": "You decided to visit the future.",
                    "choice": "Y"
                })
                return get_next_prompt("Y")
            elif user_choice == "n":
                self.reset_game()
                self.initialized = True
                return "Thank you for playing! Maybe next time.\n\n" + INITIAL_PROMPT
            else:
                return "Please choose Y or N. Or type 'End' to exit."

        elif self.current_state == "Y":
            if user_choice == "1":
                self.current_state = "1-utopia"
                self.story_segments.append({
                    "state": self.current_state,
                    "prompt": "You chose to explore a utopian society.",
                    "choice": "1"
                })
                return get_next_prompt("1-utopia")
            elif user_choice == "2":
                self.current_state = "1-dystopia"
                self.story_segments.append({
                    "state": self.current_state,
                    "prompt": "You chose to explore a dystopian world.",
                    "choice": "2"
                })
                return get_next_prompt("1-dystopia")
            else:
                return "Please choose either [1] utopia or [2] dystopia. Or type 'End' to exit."

        elif self.current_state == "1-utopia":
            if user_choice == "1":
                self.current_state = "1-utopia-1"
                self.story_segments.append({
                    "state": self.current_state,
                    "prompt": "In the utopia, you decided to learn about advanced technologies.",
                    "choice": "1"
                })
                return get_next_prompt("1-utopia-1")
            elif user_choice == "2":
                self.current_state = "1-utopia-2"
                self.story_segments.append({
                    "state": self.current_state,
                    "prompt": "In the utopia, you decided to experience a community festival.",
                    "choice": "2"
                })
                return get_next_prompt("1-utopia-2")
            else:
                return "Please choose [1] or [2]. Or type 'End' to exit."

        elif self.current_state == "1-dystopia":
            if user_choice == "1":
                self.current_state = "1-dystopia-1"
                self.story_segments.append({
                    "state": self.current_state,
                    "prompt": "In the dystopia, you decided to join a rebellion.",
                    "choice": "1"
                })
                return get_next_prompt("1-dystopia-1")
            elif user_choice == "2":
                self.current_state = "1-dystopia-2"
                self.story_segments.append({
                    "state": self.current_state,
                    "prompt": "In the dystopia, you decided to seek refuge in a hidden sanctuary.",
                    "choice": "2"
                })
                return get_next_prompt("1-dystopia-2")
            else:
                return "Please choose [1] or [2]. Or type 'End' to exit."

        # For the final hardcoded branches before AI takes over
        elif self.current_state in ["1-utopia-1", "1-utopia-2", "1-dystopia-1", "1-dystopia-2"]:
            if user_choice in ["1", "2"]:
                # This is where we transition to AI-generated content
                self.use_ai = True
                # Create a new state based on the previous state and choice
                self.current_state = f"{self.current_state}-{user_choice}"

                # Add appropriate description based on the choice
                choice_description = ""
                if self.current_state.startswith("1-utopia-1"):
                    choice_description = "try a memory device" if user_choice == "1" else "learn about the energy system"
                elif self.current_state.startswith("1-utopia-2"):
                    choice_description = "participate in a collaborative art project" if user_choice == "1" else "sample exotic foods"
                elif self.current_state.startswith("1-dystopia-1"):
                    choice_description = "offer your knowledge to help the rebellion" if user_choice == "1" else "investigate the leader's motives"
                elif self.current_state.startswith("1-dystopia-2"):
                    choice_description = "help strengthen the sanctuary's defenses" if user_choice == "1" else "learn how the community survives"

                self.story_segments.append({
                    "state": self.current_state,
                    "prompt": f"You decided to {choice_description}.",
                    "choice": user_choice
                })

                # Get AI-generated content for this state
                return await self.get_ai_response(user_choice)
            else:
                return "Please choose [1] or [2]. Or type 'End' to exit."

        # For all subsequent states after initial branches, use AI
        elif self.use_ai:
            if user_choice in ["1", "2"]:
                # Update state to track the path
                previous_state = self.current_state
                self.current_state = f"{previous_state}-{user_choice}"

                # Add this choice to story segments
                self.story_segments.append({
                    "state": self.current_state,
                    "prompt": f"For the choice between [1] and [2], you selected option {user_choice}.",
                    "choice": user_choice,
                    "ai_generated": True
                })

                # Get AI-generated content
                return await self.get_ai_response(user_choice)
            else:
                return "Please choose [1] or [2]. Or type 'End' to exit."

        # Default case if state is unknown
        return "Something went wrong. Let's start over. Would you like to visit the future? Type Y or N. Or type 'End' to exit."

    async def get_ai_response(self, user_choice):
        """Generate AI response based on the current state and user choice"""
        # Create story context from previous segments
        story_context = "\n".join([f"- {segment['prompt']}" for segment in self.story_segments[-5:]])

        # Get the last AI response if available
        last_ai_response = ""
        for segment in reversed(self.story_segments):
            if segment.get("ai_response"):
                last_ai_response = segment["ai_response"]
                break

        # Create a system prompt that includes the story context
        custom_system_prompt = SYSTEM_PROMPT.format(
            story_context=story_context,
            state=self.current_state,
            choice=user_choice
        )

        # Prepare messages for Mistral API
        messages = [
            {"role": "system", "content": custom_system_prompt},
            {"role": "user",
             "content": f"Continue my time travel adventure based on my choice ({user_choice}). The last AI response was: {last_ai_response}" if last_ai_response else "Start my AI-guided time travel adventure based on my choices so far."}
        ]

        # Get response from Mistral AI
        response = await self.client.chat.complete_async(
            model=MISTRAL_MODEL,
            messages=messages,
        )

        # Get the AI-generated content
        ai_response = response.choices[0].message.content

        # Store this AI response in the story segments
        if self.story_segments:
            self.story_segments[-1]["ai_response"] = ai_response

        return ai_response

    async def run(self, message: discord.Message):
        """Main method to process messages and return responses"""
        # Check if we need to send the initial prompt
        if not self.initialized:
            return await self.get_initial_prompt()

        # Process the user's response and advance the story
        return await self.process_user_response(message.content)