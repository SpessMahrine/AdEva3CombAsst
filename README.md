# AdEva3CombAsst
A chatbot plugin for running Adeptus Evangelion v3.05 combat via CLI that supports multiple users.

By default, you can just run it from a terminal for testing, but the intention is to plug it into a chatbot that provides the following:

  (1) Chat messages that are treated as commands. The "help" function assumes the chatbot will feed it any line that starts with a '?'. You can do whatever you want, but then change the help function.

  (2) The author of the chat message ('user'). Ideally a name to be human-readable since it is read back a few times, but can be an ID or anything else that can be personally identifiable. This is for light authentication: so that only the owners of a thing can tell it what to do. If your chat client allows multiple users to share the same name, then probably use some other kind of identifier that allows authentication or don't play with jerks.

  (3) The origin of the chat message ('channel name'). The main parser will return an array consisting of a message and where it thinks the response should go. You can, of course, ignore this when you go to print the message out, but this allows you to PM the bot your actions and for everyone to be able to see the result. Listen everywhere, speak in one place.

It should be possible to plug this into any kind of interface (GUI, web, whatever) if the interface provides the required three pieces of information. You’re on your own for that and for displaying the output coherently. 

Known issues:

  (1) Error handling. The basic terminal prompt is wrapped in a try/except statement so that data persists despite typos, but the handling is bad and there are other unhandled errors elsewhere.
  
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
  
  (11) Some sort of GUI option, which will likely be a fork of this project into a standalone application in case you want to play with people IRL instead of online.
