MAXNET Public Script Server 

Welcome to the MAXNET Script Server — a chaotic-good web app where users can:
	•	Download functional, prank, and learning shell scripts 
	•	Complete interactive coding challenges with instant feedback 
	•	Trigger wild site modes like Red Alert and Midnight Mode 
	•	Talk to a custom-built AI chatbot called MAXNET  (who is totally a Gen Z baddie)

⸻

FEATURES

Script Categories
	•	Functional: Useful scripts like system crash diagnostics and file organizers.
	•	Prank: Scare your friends, go full Batman mode, or pretend to be a hacker.
	•	Learning: Interactive Bash challenges with auto-check grading and flashy pass/fail effects.

Built-in AI Chatbot
	•	Route: /chat
	•	Powered by OpenAI (GPT-3.5 Turbo)
	•	Responds with sass, Gen Z energy, and MAXNET personality
	•	Maintains convo memory by tracking history in JSON format

Modes
	•	Red Alert Mode: Flashes red, blasts sirens, pure chaos
	•	Midnight Mode: Purple lo-fi vibes with looping audio and rain animation
	•	Chaos Mode: Triggered by activating Red Alert + Midnight. All modes, all sounds, flashing lights. Escape with a big ol’ EXIT button.

Learning Scripts

Interactive coding challenges where users:
	•	Upload or edit scripts directly in-browser
	•	Get real-time validation vs answer key
	•	See big “PASS” or “FAIL” screen with sound and color
	•	Mobile-friendly editor included

⸻

Tech Stack
	•	Python (Flask)
	•	HTML + JavaScript
	•	OpenAI API (for chatbot)
	•	Render.com (hosting)

⸻

Setup Instructions

1. Clone this Repo

git clone https://github.com/max2dmax/public-script-server.git
cd public-script-server

2. Install Dependencies

Create requirements.txt:

flask
openai==0.28

Then:

pip install -r requirements.txt

3. Set Your OpenAI Key

In terminal (or add to .zshrc / .bashrc):

export OPENAI_API_KEY=sk-XXXXXXXXXXXXXXXXXXXX

On Render:
	•	Go to your service > Environment
	•	Add:
	•	Key: OPENAI_API_KEY
	•	Value: your actual API key

4. Run Locally

python app.py

Then go to http://localhost:5000

⸻

Routes
	•	/ – homepage
	•	/grab/<filename> – download scripts
	•	/chat – chatbot API POST endpoint

⸻

Folder Structure

public-script-server/
├── static/
│   ├── [script files]
│   ├── sounds/ (pass.mp3, fail.mp3, etc)
├── templates/
│   └── index.html
├── app.py
├── requirements.txt
└── README.md


⸻

Future Ideas
	•	MAXNET voice mode 
	•	New script categories (advanced, community-made)
	•	Achievements or badges for learning

⸻

🤝 Credits

Created with love, chaos, and way too much caffeine by Max.

Want to build your own? Fork it. Remix it. Just don’t blame MAXNET when you enter Chaos Mode 
