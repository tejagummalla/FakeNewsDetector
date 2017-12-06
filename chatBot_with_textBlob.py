#Implementing a chat bot with the help of the text blob library
# followed the World Writable chat-bot tutorial

from textblob import TextBlob
import random


def find_pronoun(text):
    pronoun = None
    for word, part_of_speech in text.pos_tags :
        if part_of_speech == "PRP":
            if word == "I" :
                pronoun = "I"

            elif word.lower() == "you" :
                pronoun = "you"

    return pronoun


def find_verb(text):

    for word, pos in text.pos_tags:
        if pos.startswith('VB'):
            return word, pos

    return None, None


def find_adjective(text):
    for word, pos in text.pos_tags:
        if pos == "JJ" :
            return word

    return None



def find_noun(text):

    for word, part_of_speech in text.pos_tags:
        if part_of_speech == "NN":
            return word

    return None


def pre_process_text(text) :
    words = TextBlob(text)
    print words.tags

def find_parts_of_speech(text):
    pronoun = None
    noun = None
    adjective = None
    verb = None

    for sent in text.sentences :
        pronoun = find_pronoun(sent)
        noun = find_noun(sent)
        adjective = find_adjective(sent)
        verb = find_verb(sent)

    return pronoun, noun, adjective, verb



def starts_with_vowel(word):
    return True if word[0] in 'aeiou' else False




def check_for_greetings(text):
    for word in text.words:
        if word.lower() in GREETING_KEYWORDS:
            return random.choice(GREETING_RESPONSES)
    return None



def construct_response(pronoun, noun, verb):
    resp = []

    if pronoun:
        if pronoun.lower() == 'you':
            resp.append('I')
        elif pronoun == "I":
            resp.append('you')

        else:
            resp.append(pronoun)

    if verb:
        verb_word = verb[0]
        if verb_word in ('be', 'am', 'is', "'m"):
            if pronoun == 'I':

                resp.append("aren't really")
            else:
                resp.append(verb_word)
    if noun:
        pronoun = "an" if starts_with_vowel(noun) else "a"
        resp.append(pronoun + " " + noun)

    resp.append(random.choice(("tho", "bro", "lol", "bruh", "smh", "human")))

    return " ".join(resp)



def check_for_compliment_about_bot(text, pronoun) :
    if pronoun == 'you' :
        for word in text.words:
            if word in COMPLIMENT_WORDS:
                resp = random.choice(COMPLIMENT_RESPONSE)
                return resp

    return None

def check_for_comments_about_the_bot(pronoun, noun, adjective) :
    resp = None
    if pronoun == 'you' and (noun or adjective) :
        if noun:
            if random.choice((True,False)):
                resp = random.choice(SELF_VERBS_WITH_NOUN_CAPS_PLURAL).format(**{'noun': noun.pluralize().capitalize()})
            else :
                resp = random.choice(SELF_VERBS_WITH_NOUN_LOWER).format(**{'noun': noun})
        else :
            resp = random.choice(SELF_VERBS_WITH_ADJECTIVE).format(**{'adjective' : adjective})

    return resp



def respond(sentence) :
    parsed = TextBlob(sentence)

    #extracting the features of the text
    pronoun, noun, adjective, verb = find_parts_of_speech(parsed)


    #checking for anything that has been said about the bot
    resp = check_for_comments_about_the_bot(pronoun, noun, adjective)

    resp = check_for_compliment_about_bot(parsed, pronoun)

    if not resp:
        resp = check_for_greetings(parsed)

    if not resp:
        if not pronoun :
            resp = random.choice(NONE_RESPONSE)
        elif pronoun == 'I' and not verb :
            resp = random.choice(COMMENTS_ABOUT_SELF)
        else :
            resp = construct_response(pronoun, noun, verb)

    if not resp:
        resp = random.choice(NONE_RESPONSE)


    return resp





SELF_VERBS_WITH_NOUN_CAPS_PLURAL = [
    "My last startup totally crushed the {noun} vertical",
    "Were you aware I was a serial entrepreneur in the {noun} sector?",
    "My startup is Uber for {noun}",
    "I really consider myself an expert on {noun}",
]

SELF_VERBS_WITH_NOUN_LOWER = [
    "Yeah but I know a lot about {noun}",
    "My bros always ask me about {noun}",
]

SELF_VERBS_WITH_ADJECTIVE = [
    "I'm personally building the {adjective} Economy",
    "I consider myself to be a {adjective}preneur",
]

NONE_RESPONSE = ['MEH','WHATEVER!','REALLY', 'WHAT SHOULD I EAT FOR LUNCH?', 'YOU LOOK GOOD!']

COMMENTS_ABOUT_SELF = [
    "You're one jealous person",
    "I kinda worked very hard for that",
    "You were of no help"
    "My Klout score is {}".format(random.randint(100, 500)),
]

GREETING_KEYWORDS = ("hello", "hi", "greetings", "sup", "what's up","waddup","hola")
GREETING_RESPONSES = ["'sup bro", "hey", "*nods*", "hey you get my snap?","hohoho","how is it going?"]

COMPLIMENT_WORDS = ["good", "amazing", "beautiful", "rock", "brilliant"]

COMPLIMENT_RESPONSE = ["You are not bad yourself.", "I was born this way.", "Are you trying to flirt with me?",
                       "Hmmmmmmmmm"]

print respond("You look good")