# AdEva3CombAsst
A chatbot plugin for running Adeptus Evangelion v3 combat. 

By default, you can just run it from a terminal, but the intention is to plug it into a chatbot that provides
  (1) Chat messages that are treated as commands. The "help" function assumes the chatbot will feed it any line that starts with a '?'.
  (2) The author of the chat message. Ideally a name to be human-readable, but can be an ID or anything else that can be personally identifiable. This is for light authentication: so that only the owners of a thing can tell it what to do.
  (3) The origin of the chat message (like an IRC channel name). The main parser will return a message and where it thinks the response should go. This allows you to PM the bot your actions and for everyone to be able to see the result. 
  
It should be possible to plug this into any kind of interface (GUI, web, whatever) if the interface provides the required three pieces of information. You’re probably better off integrating that natively, though.

I'm not going to be doing versioning or anything of that sort, nor will I be frequently using GitHub since this is mostly a personal project.

Known issues:
  (1) Error handling, especially for the parser. Workaround is to either not mess up your words or put the entire combat loop statement into a try/except so it doesn’t reset your combat if you mistype. I have this handled on the chatbot’s end for me so /shrug.
  (2) It doesn’t actually do much and many things, including Hit Effects and Weapons are incomplete. Workaround is to wait for me to finish this or finish it yourself. Probably let me know if you’re going to do that so we can pool our efforts.
  (3) Typos. No workaround, a lot of the text will end up changing anyway.
Planned features, kind of in order:
  (1)	Prompt framework that allows guided creation of arbitrary actors and weapons.
  (2)	GMs having permissions to modify all actors in any way.
  (3)	Manual mode that prompts you for dice results instead of rolling dice for you.
  (4)	Condition framework.
  (5)	Action framework.
  (6)	Trigger framework.
  (7)	Initiative framework.
  (8) Combat map/engagement framework.
  (9) Save/load functions that offload everything to file(s).
  (10) Character creation function that creates a loadable character.
