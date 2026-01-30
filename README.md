# ⏳ Time Traveling AI — Interactive Narrative Discord Agent  
*A branching-story + LLM hybrid agent system for immersive time-travel adventures on Discord.*

## 🚀 Overview  
This project implements a fully interactive **state-driven narrative engine** for Discord, powered by **Mistral LLMs** and integrated through a custom agent architecture.  
Users progress through a time-travel storyline by making choices, and the system dynamically transitions between **hand-crafted story branches** and **AI-generated content** once the narrative becomes sufficiently complex.

The bot was deployed in the CS153 Discord server and manages an entire interactive storytelling experience directly inside private group channels.

---

# ✨ Our Contributions  

### 🌲 Hybrid branching-story engine  
- Designed a **hierarchical state machine** to manage narrative flow  
- Use hardcoded early branches for deterministic grounding, and then automatically transitions to fully LLM-generated content after initial arcs  
- Maintains story continuity through a tracked memory buffer

### 🤖 Custom Mistral Agent
- Built an async wrapper around Mistral’s `chat.complete_async` API  
- Engineered a structured system prompt enforcing narrative constraints with two-option branching at every step  
- Dynamically injects state, user choice, and recent story context

### 🧠 Dynamic prompt construction  
- Injects the last 5 story segments for coherence  
- Incorporates current state + user choice into the system message  
- Supports indefinite story continuation with high coherence

### 🎮 User choice processing logic  
- Wrote a complete decision pipeline:  
  - input validation  
  - branching transitions  
  - state encoding  
  - memory tracking  
- Seamlessly transitions from deterministic paths → AI-generated content

### 🪄 State encoding design  
- Uses hierarchical path encoding (e.g., `1-utopia-2-1`)  
- Enables clean reasoning about story progression

### ⚙️ Discord–LLM middleware  
- Integrated with Discord via a `run()` method triggered on every message  
- Handles initialization flow, story resets, and multi-turn logic  

---
---

# 🎭 Example Interaction

**User:** Y  
**Bot:** Great! Would you like to visit a utopian future [1] or a dystopian one [2]?

**User:** 1  
→ deterministic branch

**User:** 2  
→ deterministic branch

**User:** 2  
→ transitions to AI-generated narrative

---

# 📦 Quickstart (Run the Bot)

1. Clone the repo  
2. Create a `.env` file:
   ```env
   DISCORD_TOKEN="your key here"
   MISTRAL_API_KEY="your key here"

3. Install dependencies 
  conda env create -f local_env.yml
  conda activate discord_bot
4. Run the bot:
python3 bot.py

