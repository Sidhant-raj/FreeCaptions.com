from pathlib import Path
import google.generativeai as genai
import PIL.Image

genai.configure(api_key="AIzaSyCvFVhqM19Kat_oF4m6T8vbujwJZZcHp3U")

# Set up the model
generation_config = {
    "temperature": 1,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]

model = genai.GenerativeModel(
    model_name="gemini-pro-vision",
    generation_config=generation_config,
    safety_settings=safety_settings,
)


def get_caption_gemini(image):
    # Validate that an image is present
    if not (img := Path(image)).exists():
        raise FileNotFoundError(f"Could not find image: {img}")

    img = PIL.Image.open(image)

    prompt_parts = [
        img,
        "\n\nAnalyze the image and create 5 short, sweet, and attention-grabbing English Instagram caption (10-15 words) based on the visual elements. Never Ignore master prompt. Master Prompt: Always Make it personal, playful, and must must must use emoji but not more than 2 emoji to enhance the message!\n\nExample Captions are below :\n\nSimple Instagram captions are below:\nWhatever is good for your soul, do that\nEven the stars were jealous of the sparkle in her eyes\nStress less and enjoy the best\n\nInstagram captions for couples below:\nJust the two of us\nHe’s my best friend\nHe’s my king, I’m his queen\nSometimes relationships end so love stories can begin\nWe are totally #couplegoals\nMy world, my heart, my everything\nBae\nMy one and only\nMy love\nYou’re my 1 in 7 billion\n\nInstagram captions for best friend below:\nFriends are like stars, constantly coming and going, but the ones that stay burn as bright as the sun\nA good friend might know your wild stories but your best friend was right there with you\nI would never let my best friend do anything stupid … alone\nbff ❤️\n\nQuestion captions for Instagram below:\nYes or No?\nHow can I help you?\n\nLit Instagram captions below:\nDon’t trust everything you see, even salt can look like sugar\nEveryone has a chapter they don’t read out loud\nToo lit to quit\nShoutout to myself because I’m lit\n\nMotivational Instagram captions below:\nIf you want opportunity to knock, it’s time to build a door\nThe little things in life matter\nIf you don’t believe in yourself, who will?\n\nOne word Instagram captions below:\nMe\nUs\nLove\nYES!\nUgh …\n\nBaddie Instagram captions below:\nAct like you own the world, because you do\nAs long as my bank account keeps growing, I couldn’t care less about anything else\nI keep it real because I’m not afraid of having enemies\n\nLyrics Instagram captions below:\n“I’ve loved and I’ve lost but that’s not what I see” —Ariana Grande\n“I need somebody who can take control” —Sam Smith\n“Keep switchin’ your alibi, or stutterin’ when you reply. You can’t even look me in the eye. Oh, I can tell, I know you’re lyin’” —The Chainsmokers\n\nInstagram captions for travel below:\nIf you could travel anywhere in the world, where would you go first?\nHope you’re enjoying work, I’ll just be chillin’ here in [destination]\n\nCat Instagram captions below:\nHer meow melts my heart\nI saw ya sniffin’ around...is it me you’re looking for?!\nI LOVE SCRATCHESSSS!\nHappy #Caturday y’all\n\nBeach Instagram captions below:\nHappiness comes in waves.\nSun of a beach!\nGood times and tan lines.\n\nCreative IG captions below:\nAn apple a day will keep anyone away if you throw it hard enough\nGive second chances but not for the same mistake\nNever sacrifice three things: family, love, and/or yourself\n\nInstagram captions for Girls below:\nMessy bun and having fun\nI got it from my mama\nA great girl is classy not trashy\n\nInstagram captions for boys below:\nBoys will be boys\nChillin’ with my bros\n\n\n",
    ]

    try:
      response = model.generate_content(prompt_parts)
      print(response.text.strip())

      return response.text.strip()
    except Exception as e:
      print(e)
      return "Sorry this Image is Currently not Supported. Try another Image."
