import random
from urllib.request import urlopen
import spacy
from collections import Counter
import tracery
from tracery.modifiers import base_english

citiesURL = "https://gist.githubusercontent.com/norcal82/4accc0d968444859b408/raw/d295d94608be043a4774087d6cb19caf3a1f27a2/city_names.txt"
occupationsURL = "https://gist.githubusercontent.com/wsc/1083459/raw/d8d0aa8737a36912e6c119a172c8367276b76260/gistfile1.txt"
companiesURL = "https://raw.githubusercontent.com/abilitize/Helpful-Lists/master/Fortune%20500.txt"
myLifeAndWorkURL = "http://www.gutenberg.org/cache/epub/7213/pg7213.txt"

citiesList = urlopen(citiesURL).read().decode("utf-8").split("\n")[2:]
occupationsList = urlopen(occupationsURL).read().decode("utf-8").split("\n")
companiesList = urlopen(companiesURL).read().decode("utf-8").split("\n")
myLifeAndWorkText = urlopen(myLifeAndWorkURL).read().decode("utf-8").replace("\n", " ")

# create a new spaCy object with English model
nlp = spacy.load('en_core_web_md')

# parse the text
doc = nlp(myLifeAndWorkText)

# extract text units
sentences = list(doc.sents)
words = [w for w in list(doc) if w.is_alpha]
nounChunks = list(doc.noun_chunks)
entities = list(doc.ents)

# used for finding the most common words
wordCount = Counter([w.text for w in words])


def getWordsByPos(pos):
    return [w for w in words if w.pos_ == pos]


nouns = getWordsByPos("NOUN")  # robot
properNouns = getWordsByPos("PROPN")  # Mt. Everest
verbs = getWordsByPos("VERB")  # eat
adjectives = getWordsByPos("ADJ")  # big
adverbs = getWordsByPos("ADV")  # slowly
pronouns = getWordsByPos("PRON")  # I, me, my, mine, there, who
determiners = getWordsByPos("DET")  # my, all
conjunctions = getWordsByPos("CCONJ")  # and, but, or, so
symbols = getWordsByPos("SYM")  # currency, $
punctuations = getWordsByPos("PUNCT")  # ,.:()
numbers = getWordsByPos("NUM")  # number
xs = getWordsByPos("X")  # email, foreign word, unknown


# nouns
def getNounsByTag(tag):
    return [n.text for n in nouns if n.tag_ == tag]


nounsSingular = getNounsByTag("NN")  # robot
nounsPlural = getNounsByTag("NNS")  # robots


# proper nouns
def getProperNounsByTag(tag):
    return [p.text for p in properNouns if p.tag_ == tag]


properNounsSingular = getProperNounsByTag("NNP")  # Korean
properNounsPlural = getProperNounsByTag("NNPS")  # Koreans


# verbs
def getVerbsByTag(tag):
    return [v.text for v in verbs if v.tag_ == tag]


verbsBase = getVerbsByTag("VB")  # eat
verbsPast = getVerbsByTag("VBD")  # ate
verbsPresentParticiple = getVerbsByTag("VBG")  # eating
verbsPastParticiple = getVerbsByTag("VBN")  # eaten
verbsPresentNon3rd = getVerbsByTag("VBP")  # eat
verbsPresent3rd = getVerbsByTag("VBZ")  # eats
verbsModal = getVerbsByTag("MD")  # can, could, should, might


# adjectives
def getAdjectivesByTag(tag):
    return [a.text for a in adjectives if a.tag_ == tag]


adjectivesAffix = getAdjectivesByTag("AFX")  # unhappy, useless
adjectivesAdjective = getAdjectivesByTag("JJ")  # long
adjectivesComparative = getAdjectivesByTag("JJR")  # longer
adjectivesSuperlative = getAdjectivesByTag("JJS")  # the longest


# adverbs
def getAdVerbsByTag(tag):
    return [a.text for a in adverbs if a.tag_ == tag]


adverbsAdverb = getAdVerbsByTag("RB")  # slowly
adverbsComparative = getAdVerbsByTag("RBR")  # more slowly
adverbsSuperlative = getAdVerbsByTag("RBS")  # most slowly
adverbsWh = getAdVerbsByTag("WRB")  # when, where, why, how


# pronouns
def getPronounsByTag(tag):
    return [p.text for p in pronouns if p.tag_ == tag]


pronounsThere = getPronounsByTag("EX")  # there
pronounsPersonal = getPronounsByTag("PRP")  # I, me, my
pronounsWh = getPronounsByTag("WP")  # who, who, whose


# entities
def getEntitiesByLabel(label):
    return [e.text for e in entities if e.label_ == label]


people = getEntitiesByLabel("PERSON")
locations = getEntitiesByLabel("LOC")
times = getEntitiesByLabel("TIME")
companies = getEntitiesByLabel("ORG")
countries = getEntitiesByLabel("GPE")
product = getEntitiesByLabel("PRODUCT")
language = getEntitiesByLabel("LANGUAGE")
date = getEntitiesByLabel("DATE")
time = getEntitiesByLabel("TIME")
percent = getEntitiesByLabel("PERCENT")  # 100%
money = getEntitiesByLabel("MONEY")  # dollars
quantity = getEntitiesByLabel("QUANTITY")  # miles, pounds
ordinal = getEntitiesByLabel("ORDINAL")  # first, second
cardinal = getEntitiesByLabel("CARDINAL")  # one, two

name = random.choice(people)
pronoun = random.choice(["he", "she"])

rules = {
    "origin1":
        [
            "#name.capitalize# is #city.capitalize.a#-based #profession# who works with #company.capitalize# to help #customer# #verbPresent# their #nounObject#."
        ],
    "origin2":
        [
            "#pronoun.capitalize# has #verbsPastParticiple# one of the #adjectivesSuperlative# #nounsPlural# in #location# and #achievement#",
            "#pronoun.capitalize# has #verbsPastParticiple# the #ordinal# #adjectivesSuperlative# #nounsSingular# in #location# and #achievement#"
        ],
    "origin3":
        [
            "Also, #pronoun.capitalize# can speak #cardinal# languages including #language#."
        ],
    "origin4":
        [
            "#name.capitalize# continues to #verbPresent# #adjectivesAdjective# #nounsPlural#."
        ],
    "achievement": "has #verbsPastParticiple# the #nounsSingular# by #percent# for #nounChunk#.",
    "name": name,
    "pronoun": pronoun,
    "city": citiesList,
    "location": locations,
    "profession": occupationsList,
    "company": companiesList,
    "customer": people,
    "verbPresent": [i.lower() for i in verbsBase],
    "nounObject": [i.lower() for i in product],
    "verbsPresentParticiple": [i.lower() for i in verbsPresentParticiple],
    "verbsPastParticiple": [i.lower() for i in verbsPastParticiple],
    "adjectivesSuperlative": [i.lower() for i in adjectivesSuperlative],
    "nounsSingular": [i.lower() for i in nounsSingular],
    "nounsPlural": [i.lower() for i in nounsPlural],
    "nounChunk": [i.text.lower() for i in nounChunks],
    "ordinal": [i for i in ordinal if not " " in i],
    "cardinal": [i for i in cardinal if i.lower() != "one" and not " " in i],
    "language": language,
    "percent": [i for i in percent if not " " in i],
    "adverbsAdverb": adverbsAdverb,
    "adjectivesAdjective": adjectivesAdjective,
}

grammar = tracery.Grammar(rules)
grammar.add_modifiers(base_english)

numBiographies = 1  # for testing
numOrigins = 4
for i in range(numBiographies):
    print("\n")
    for j in range(numOrigins):
        print(grammar.flatten(f"#origin{j + 1}#"))
