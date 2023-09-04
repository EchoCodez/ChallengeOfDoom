
__all__ = (
    'apimedic_txt_config',
    "disclaimer"
)

apimedic_txt_config = (
        {
            "title": "Registering for APImedic",
            "content": "Congressional Health App uses the APImedic web api to rank which conditions you will be most likely to have based on your symptoms. \
                \nAs such, we need a username and password for APImedic. Don't worry, it's free! All you need to do is follow the instructions on the next page."
        },
        {
            "title": "Registering for APImedic",
            "content": "Just go through and follow the directions to sign up on the website (click the button below).\
                \nOnce you have completed the signup, login and go to \"API KEYS\" at the top bar of the website.\
                    \nThen click the arrow next to Live Basic API Account, and copy paste your username and password onto the next page.",
            "buttons": ("Go to website", "See registering live"),
            "commands": (lambda: open_new_tab("https://apimedic.com/signup"), lambda: open_new_tab("https://www.youtube.com/"))
        }
    )

disclaimer = ". ".join([
    "\tThis app (“App”) provides only information, is not medical or treatment advice and may not be treated as such by the user",
    "As such, this App may not be relied upon for the purposes of medical diagnosis or as a recommendation for medical care or treatment",
    "The information on this App is not a substitute for professional medical advice, diagnosis or treatment",
    "All content, including text, graphics, images and information, contained on or available through this App is for general information purposes only",
    "\n\tYou are strongly encouraged to confirm any information obtained from or through this App with your physician or another professional healthcare provider and to review all information regarding any medical condition or treatment with your physician or other a professional healthcare provider",
    "By click \"I Accept\", you have acknowledged that you have read the disclaimer, you agree with the disclaimer, and you agree to be legally bound by this medical disclaimer which shall take place immediately upon clicking the button"
])
