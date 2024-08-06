# AnthologyGPT
LLMs are great at making up stuff - this is the best way to use it


# what am i making?

this is a cli application that use calls to some LLM that talks to itself over and over to build a giant block of text for your literary needs:

- scripture
- history
- legends
- fables
- dynasties
- plots

# what's the input?

- Anthology Type
- Factions (fantasy races, clans, gangs, whatever)
- Themes
- Characters
- Conflicts
- More

# What's the output?

- a directory of conversations
- a directory of actual historical events
- a directory of "remembered" historical events
- a summary of the current state of history

# What's the catch?

the more thought you put into the first (and subsequent) generations, the less generic the final output.


# The Flow:

## Phase One: Anthology Generation

This is where you set up the whole thing. Current implementation is guided generation, shortlist feature is a config file that can both be created and read by the app

- An Anthology has five initial components:
    1. Name - An identifier to distinguish this from other anthologies you generate
    2. Setting - A rough list of adjectives to help set the tone for the anthology
    3. Anthology Type - The physical characteristics of the space your characters inhabit
    4. Factions - The arbitrary distinguishing factors between different groups within your anthology.
    5. Characters - The avatars that actually inhabit your anthology and represent the changes that occur within the progression of time.

After your anthology has been created, you enter into the main loop of AnthologyGPT:

## Phase Two: Passage of Time

In this stage, you determine how much time passes between the current year of the Anthology and the end of the Era your characters inhabit, and what the theme for this Era will be.
The theme can be specific, like "The death of Character X", "The Cataclysm", or "War between Faction A and Faction B", but can also be more broad, like "Love" or "Sunlight"
Time passes in whole-year increments, with longer passages of time resulting in fewer, but more significant events added to your Anthology.

The passage of time is comprised of three parts:
1. Historical events, whether large or small, that affect the space and/or the characters.
2. Conversations between your characters (or monologues from a character).
3. The loss of existing history.

## Phase Three: End of an Era


Once the Era has completed, all the events that have occured are collected and transformed into "Remembered History".
Memory is a fuzzy thing - summaries gloss over information that might have been relevant; events can be misremembered; only one side of a story can be heard.
Even lost memories can live on in "remembered" forms, evolving into stories that persist throughout your Anthology.
If you dislike what you got, you can describe what you want done differently and either rewrite the history to match or re-run the entire Era (with or without your suggestions).

Once you have settled on the history for your Era, a new generation of factions and characters are generated as suggestions for the next Era. 
You can choose to keep what you started with, replace them all with these new suggestions, add all new factions and/or characters yourself, or any combination of these!
From there, your options are:
- Continue the current Era. Experience the same passage of time, but expand upon the events that have occured.
- Extend the current Era. Progress through a new length of time, but continuing with the same theme.
- Enter a new Era. Progress through a new length of time, with a new theme.
- End your Anthology. Create a summary of your Remembered History, and stop the Passage of Time


