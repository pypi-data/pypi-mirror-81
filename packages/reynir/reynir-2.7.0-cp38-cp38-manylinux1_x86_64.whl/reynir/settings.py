"""
    Greynir: Natural language processing for Icelandic

    Settings module

    Copyright (C) 2020 Miðeind ehf.

    This software is licensed under the MIT License:

        Permission is hereby granted, free of charge, to any person
        obtaining a copy of this software and associated documentation
        files (the "Software"), to deal in the Software without restriction,
        including without limitation the rights to use, copy, modify, merge,
        publish, distribute, sublicense, and/or sell copies of the Software,
        and to permit persons to whom the Software is furnished to do so,
        subject to the following conditions:

        The above copyright notice and this permission notice shall be
        included in all copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
        EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
        MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
        IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
        CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
        TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
        SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

    This module reads and interprets the GreynirPackage.conf
    configuration file. The file can include other files using the $include
    directive, making it easier to arrange configuration sections into logical
    and manageable pieces.

    Sections are identified like so: [ section_name ]

    Comments start with # signs.

    Sections are interpreted by section handlers.

"""

from typing import cast, Iterable, Optional, Union, Dict, Tuple, Set, List

import os
import codecs
import locale
import threading

from contextlib import contextmanager, closing
from collections import defaultdict
from threading import Lock
from pkg_resources import resource_stream


# The sorting locale used by default in the changedlocale function
_DEFAULT_SORT_LOCALE = ("IS_is", "UTF-8")

# A set of all valid verb argument cases
_ALL_CASES = frozenset(("nf", "þf", "þgf", "ef"))
_ALL_GENDERS = frozenset(("kk", "kvk", "hk"))
_ALL_NUMBERS = frozenset(("et", "ft"))
_SUBCLAUSES = frozenset(("nh", "mnh", "falls"))
_REFLPRN = {"sig": "sig_hk_et_þf", "sér": "sig_hk_et_þgf", "sín": "sig_hk_et_ef"}
_REFLPRN_SET = frozenset(_REFLPRN.keys())

# Type of meaning tuples for static phrases
# stofn, utg, ordfl, fl, ordmynd, beyging
MeaningTuple = Tuple[str, int, str, str, str, str]
# ordfl, fl, beyging
StaticPhraseTuple = Tuple[str, str, str]
# Type for preference specifications
PreferenceTuple = Tuple[List[str], List[str], int]
# Type of set of zero-verb arguments
VerbZeroArgSet = Set[str]
# Type of dict of verbs with arguments (1 or 2),
# where each entry is a list of argument lists
VerbWithArgDict = Dict[str, List[List[str]]]
VerbWithArgErrorDict = Dict[str, Dict[str, str]]


@contextmanager
def changedlocale(new_locale=None):
    """ Change locale for collation temporarily within a context (with-statement) """
    # The newone locale parameter should be a tuple: ('is_IS', 'UTF-8')
    old_locale = locale.getlocale(locale.LC_COLLATE)
    try:
        locale.setlocale(locale.LC_COLLATE, new_locale or _DEFAULT_SORT_LOCALE)
        yield locale.strxfrm  # Function to transform string for sorting
    finally:
        locale.setlocale(locale.LC_COLLATE, old_locale)


def sort_strings(strings, loc=None):
    """ Sort a list of strings using the specified locale's collation order """
    # Change locale temporarily for the sort
    with changedlocale(loc) as strxfrm:
        return sorted(strings, key=strxfrm)


class ConfigError(Exception):

    """ Exception class for configuration errors """

    def __init__(self, s):
        super().__init__(s)
        self.fname = None
        self.line = 0

    def set_pos(self, fname, line):
        """ Set file name and line information, if not already set """
        if not self.fname:
            self.fname = fname
            self.line = line

    def __str__(self):
        """ Return a string representation of this exception """
        s = Exception.__str__(self)
        if not self.fname:
            return s
        return "File {0}, line {1}: {2}".format(self.fname, self.line, s)


class LineReader:

    """ Read lines from a text file, recognizing $include directives """

    def __init__(self, fname, outer_fname=None, outer_line=0):
        self._fname = fname
        self._line = 0
        self._inner_rdr = None
        self._outer_fname = outer_fname
        self._outer_line = outer_line

    def fname(self):
        """ The name of the file being read """
        return self._fname if self._inner_rdr is None else self._inner_rdr.fname()

    def line(self):
        """ The number of the current line within the file """
        return self._line if self._inner_rdr is None else self._inner_rdr.line()

    def lines(self):
        """ Generator yielding lines from a text file """
        self._line = 0
        try:
            if __package__:
                stream = resource_stream(__name__, self._fname)
            else:
                stream = open(self._fname, "rb")
            with stream as inp:
                # Read config file line-by-line from the package resources
                for b in inp:
                    # We get byte strings; convert from utf-8 to strings
                    s = b.decode("utf-8")
                    self._line += 1
                    # Check for include directive: $include filename.txt
                    if s.startswith("$") and s.lower().startswith("$include "):
                        iname = s.split(maxsplit=1)[1].strip()
                        # Do some path magic to allow the included path
                        # to be relative to the current file path, or a
                        # fresh (absolute) path by itself
                        head, _ = os.path.split(self._fname)
                        iname = os.path.join(head, iname)
                        rdr = self._inner_rdr = LineReader(
                            iname, self._fname, self._line
                        )
                        for incl_s in rdr.lines():
                            yield incl_s
                        self._inner_rdr = None
                    else:
                        yield s
        except (IOError, OSError):
            if self._outer_fname:
                # This is an include file within an outer config file
                c = ConfigError(
                    "Error while opening or reading include file '{0}'".format(
                        self._fname
                    )
                )
                c.set_pos(self._outer_fname, self._outer_line)
            else:
                # This is an outermost config file
                c = ConfigError(
                    "Error while opening or reading config file '{0}'".format(
                        self._fname
                    )
                )
            raise c


class VerbObjects:

    """ Wrapper around dictionary of verbs and their objects,
        initialized from the config file """

    # Dictionary of verbs by object (argument) number, 0, 1 or 2
    # Verbs can control zero, one or two arguments (noun phrases),
    # where each argument must have a particular case
    VERBS = [set(), defaultdict(list), defaultdict(list)]  # type: List[Union[VerbZeroArgSet, VerbWithArgDict]]
    # Dictionary of verb forms with associated scores
    # The key is the normal form of the verb + the associated cases,
    # separated by underscores, e.g. "vera_þgf_ef"
    SCORES = dict()  # type: Dict[str, int]
    # Dictionary of verbs where, for each verb + argument cases, we store a set of
    # preposition_case keys, i.e. "frá_þgf"
    PREPOSITIONS = defaultdict(set)  # type: Dict[str, Set[str]]

    # dict { verb + argument cases : verb particle}
    VERB_PARTICLES = defaultdict(set)  # type: Dict[str, Set[str]]

    VERBS_ERRORS = [set(), defaultdict(dict), defaultdict(dict)]  # type: List[Union[VerbZeroArgSet, VerbWithArgErrorDict]]
    VERB_PARTICLES_ERRORS = defaultdict(dict)  # type: Dict[str, Dict[str, str]]
    PREPOSITIONS_ERRORS = defaultdict(dict)  # type: Dict[str, Dict[str, str]]
    WRONG_VERBS = dict()  # type: Dict[str, str]

    @staticmethod
    def check_args(args: List[str]) -> None:
        for kind in args:
            if kind not in _ALL_CASES | _SUBCLAUSES | _REFLPRN_SET:
                spl = kind.split("_")
                # Allow the last variant to be _gr, if the
                # next-to-last one is a case
                if spl and spl[-1] == "gr":
                    spl = spl[:-1]
                if not spl or spl[-1] not in _ALL_CASES:
                    raise ConfigError(
                        "Invalid verb argument: '{0}'".format(kind)
                    )

    @staticmethod
    def add(
        verb: str,
        args: List[str],
        prepositions: List[Tuple[str, str]],
        particle: Optional[str],
        score: int,
    ) -> None:
        """ Add a verb and its objects (arguments). Called from the config file handler. """
        la = len(args)
        if la > 2:
            raise ConfigError("A verb can have 0-2 arguments; {0} given".format(la))
        if la:
            VerbObjects.check_args(args)
            # Append a possible argument list
            vargs = cast(VerbWithArgDict, VerbObjects.VERBS[la])
            arglists = vargs[verb]
            if args not in arglists:
                # Avoid adding the same argument list twice
                arglists.append(args)
        else:
            # Note that the verb can be argument-free
            argset = cast(VerbZeroArgSet, VerbObjects.VERBS[0])
            argset.add(verb)
        # Store the score, if nonzero
        verb_with_cases = "_".join([verb] + args)
        if score != 0:
            VerbObjects.SCORES[verb_with_cases] = score
        # prepositions is a list of tuples: (preposition, case/kind), e.g. ("í", "þgf") or ("í", "falls")
        d = VerbObjects.PREPOSITIONS[verb_with_cases]
        for p, kind in prepositions:
            # Add a "bare" preposition, such as "í"
            d.add(p)
            # Add a full form with case or argument kind, such as "í_þgf", or "í_nh"
            d.add(p + "_" + kind)
        if particle:
            VerbObjects.VERB_PARTICLES[verb_with_cases].add(particle)

    @staticmethod
    def add_error(
        verb: str,
        args: List[str],
        prepositions: List[Tuple[str, str]],
        particle: Optional[str],
        corr: str,
    ) -> None:
        """ Take note of a verb object specification with an $error pragma """
        VerbObjects.check_args(args)
        corrlist = corr.split(",")
        errlist = corrlist[0].split("-")
        errkind = errlist[0].strip()
        verb_with_cases = "_".join([verb] + args)
        if errkind == "OBJ":
            vargs = cast(VerbWithArgErrorDict, VerbObjects.VERBS_ERRORS[len(args)])
            arglists = vargs[verb]
            arglists[verb_with_cases] = corr
        elif errkind == "PP":
            d = VerbObjects.PREPOSITIONS_ERRORS[verb_with_cases]
            for p, kind in prepositions:
                d[p] = corr
                d[p + "_" + kind] = corr
        elif errkind == "PRTCL":
            # !!! TODO: Parse the corr string
            if particle is None:
                raise ConfigError("Particle error specification must specify particle")
            VerbObjects.VERB_PARTICLES_ERRORS[verb_with_cases][particle] = corr
        elif errkind == "ALL":
            # !!! TODO: Implement this (store specification of a
            # !!! TODO: replacement of the entire construct)
            pass
        elif errkind == "PREDS":
            # !!! TODO: Implement this
            pass
        elif errkind == "WRONG":
            wrong_kind = errlist[1].strip()
            if wrong_kind == "VERB":
                # Wrong verb, must point to completely different verb + args
                if len(corrlist) != 2:
                    raise ConfigError("WRONG-VERB must specify correct verb")
                if particle:
                    verb_with_cases += "*" + particle
                if verb_with_cases in VerbObjects.WRONG_VERBS:
                    pass
                    # raise ConfigError("WRONG-VERB has already been specified for this verb, argument list and particle")
                VerbObjects.WRONG_VERBS[verb_with_cases] = corrlist[1]
            elif wrong_kind == "OBJ":
                # !!! TODO: Implement this
                pass
            else:
                raise ConfigError("Unknown type of WRONG-XXX in $error pragma")
        else:
            raise ConfigError(
                "Unknown error type in $error pragma: '{0}'".format(errkind)
            )

    @staticmethod
    def verb_matches_preposition(verb_with_cases: str, prep_with_case: str) -> bool:
        """ Does the given preposition with the given case fit the verb? """
        # if Settings.DEBUG:
        #    print("verb_matches_preposition: verb {0}, prep {1}, verb found {2}, prep found {3}"
        #        .format(verb_with_cases, prep_with_case,
        #            verb_with_cases in VerbObjects.PREPOSITIONS,
        #            verb_with_cases in VerbObjects.PREPOSITIONS and
        #            prep_with_case in VerbObjects.PREPOSITIONS[verb_with_cases]))
        return prep_with_case in VerbObjects.PREPOSITIONS.get(verb_with_cases, set())

    @staticmethod
    def verb_matches_particle(verb_with_cases: str, particle: str) -> bool:
        """ Does the given particle fit the verb? """
        return particle in VerbObjects.VERB_PARTICLES.get(verb_with_cases, set())


class VerbSubjects:

    """ Wrapper around dictionary of verbs and their subjects,
        initialized from the config file """

    # Dictionary of verbs and their associated set of subject cases
    VERBS: Dict[str, Set[str]] = defaultdict(set)
    _CASE = "þgf"  # Default subject case
    # dict { verb : (wrong_case, correct_case) }
    VERBS_ERRORS: Dict[str, Dict[str, str]] = defaultdict(dict)

    @staticmethod
    def set_case(case: str) -> None:
        """ Set the case of the subject for the following verbs """
        # if case not in { "þf", "þgf", "ef", "none", "lhþt" }:
        #     raise ConfigError("Unknown verb subject case '{0}' in verb_subjects".format(case))
        VerbSubjects._CASE = case

    @staticmethod
    def add(verb: str) -> None:
        """ Add a verb and its arguments. Called from the config file handler. """
        VerbSubjects.VERBS[verb].add(VerbSubjects._CASE)

    @staticmethod
    def add_error(verb: str, corr: str) -> None:
        """ Add a verb and the correct case. Called from the config file handler. """
        corrlist = corr.split(",")
        errlist = corrlist[0].split("-")
        errkind = errlist[0].strip()
        if errkind == "SUBJ":
            if len(errlist) != 2:
                raise ConfigError("Expected $error(SUBJ-XXX, ...)")
            subj_type = errlist[1].strip()
            if subj_type == "CASE":
                corr_case = corrlist[1].strip()
                VerbSubjects.VERBS_ERRORS[verb][VerbSubjects._CASE] = corr_case
            else:
                raise ConfigError(
                    "Unknown subject specification: 'SUBJ-{0}'".format(subj_type)
                )
        else:
            raise ConfigError(
                "Unknown error type in $error pragma: '{0}'".format(errkind)
            )

    @staticmethod
    def is_strictly_impersonal(verb: str) -> bool:
        """ Returns True if the given verb is only impersonal, i.e. if it appears
            with an $error() pragma in the subject = nf section of verb_subjects
            and cannot be used with a nominative subject: ?'ég dreymdi þig' """
        return "nf" in VerbSubjects.VERBS_ERRORS.get(verb, set())


class Prepositions:

    """ Wrapper around dictionary of prepositions, initialized from the config file """

    # Dictionary of prepositions: preposition -> { set of cases that it controls }
    PP = defaultdict(set)  # type: Dict[str, Set[str]]
    # Prepositions that can be followed by an infinitive verb phrase
    # 'Beiðnin um að handtaka manninn var send lögreglunni'
    PP_NH = set()  # type: Set[str]
    # Set of common, 'plain' prepositions that require matching with BÍN meanings,
    # cf. logic in matcher_fs() in binparser.py. If filtering according to Phrases.conf
    # is important for a preposition, include it here.
    PP_COMMON = set()  # type: Set[str]
    # A dictionary containing information from $error() pragmas associated
    # with the preposition. Each entry is again a dict of {case: error} specifications,
    # where each error spec is usually a tuple.
    PP_ERRORS = defaultdict(dict)  # type: Dict[str, Dict[str, Tuple]]

    @staticmethod
    def add(prep: str, case: str, nh: bool) -> None:
        """ Add a preposition and its case. Called from the config file handler. """
        if prep.endswith("*"):
            # Star-marked prepositions are 'plain'
            prep = prep[:-1]
            if not prep:
                raise ConfigError("Asterisk should be affixed to a preposition")
            if " " in prep:
                raise ConfigError("An asterisk-marked preposition must be a single word")
            # Add to set of 'common'/'plain' prepositions
            Prepositions.PP_COMMON.add(prep)
        Prepositions.PP[prep].add(case)
        if nh:
            Prepositions.PP_NH.add(prep)

    @staticmethod
    def add_error(prep: str, case: str, corr: Tuple) -> None:
        """ Add an error correction entry for a preposition and a case.
            An error correction entry is usually a tuple. """
        Prepositions.PP_ERRORS[prep][case] = corr


class AdjectiveTemplate:

    """ Wrapper around template list of adjective endings """

    # List of tuples: (ending, form_spec)
    ENDINGS = []  # type: List[Tuple[str, str]]

    @classmethod
    def add(cls, ending: str, form: str) -> None:
        """ Add an adjective ending and its associated form. """
        cls.ENDINGS.append((ending, form))


class DisallowedNames:

    """ Wrapper around list of disallowed person name forms """

    # Dictionary of name stems : sets of cases
    STEMS = {}  # type: Dict[str, Set[str]]

    @classmethod
    def add(cls, name: str, cases: Iterable[str]) -> None:
        """ Add an adjective ending and its associated form. """
        cls.STEMS[name] = set(cases)


class UndeclinableAdjectives:

    """ Wrapper around list of undeclinable adjectives """

    # Set of adjectives
    ADJECTIVES = set()  # type: Set[str]

    @classmethod
    def add(cls, wrd: str) -> None:
        """ Add an adjective """
        cls.ADJECTIVES.add(wrd)


class StaticPhrases:

    """ Wrapper around dictionary of static phrases, initialized from the config file """

    # Default meaning for static phrases
    MEANING = ("ao", "frasi", "-")  # type: StaticPhraseTuple
    # Dictionary of the static phrases with their meanings
    MAP = {}  # type: Dict[str, MeaningTuple]
    # Dictionary of the static phrases with their IFD tags and lemmas
    # { static_phrase : (tag string, lemma string) }
    DETAILS = {}  # type: Dict[str, Tuple[str, str]]
    # List of all static phrases and their meanings
    LIST = []  # type: List[Tuple[str, MeaningTuple]]
    # Parsing dictionary keyed by first word of phrase
    DICT = defaultdict(list)  # type: Dict[str, List[Tuple[List[str], int]]]
    # Error dictionary, { phrase : (error_code, right_phrase, right_tag_string, right_lemma_string) }
    ERROR_DICT = {}  # type: Dict[str, Tuple[str, str, str, str]]

    @staticmethod
    def add(spec: str) -> None:
        """ Add a static phrase to the dictionary. Called from the config file handler. """
        parts = spec.split(",")
        if len(parts) not in {1, 3}:
            raise ConfigError("Static phrase must include IFD tag list and lemmas")

        phrase = parts[0].strip()

        if len(phrase) < 3 or phrase[0] != '"' or phrase[-1] != '"':
            raise ConfigError("Static phrase must be enclosed in double quotes")

        phrase = phrase[1:-1]

        if phrase in StaticPhrases.MAP:
            raise ConfigError(
                "Static phrase '{0}' is defined more than once".format(phrase)
            )

        # First add to phrase list
        ix = len(StaticPhrases.LIST)
        m = StaticPhrases.MEANING

        mtuple = (phrase, 0, m[0], m[1], phrase, m[2])

        # Append the phrase as well as its meaning in tuple form
        StaticPhrases.LIST.append((phrase, mtuple))

        # Add to the main phrase dictionary
        StaticPhrases.MAP[phrase] = mtuple

        # If details are supplied, store them
        if len(parts) == 3:
            tags = parts[1].strip()
            lemmas = parts[2].strip()
            if len(tags) < 3 or tags[0] != '"' or tags[-1] != '"':
                raise ConfigError("IFD tag list must be enclosed in double quotes")
            if len(lemmas) < 3 or lemmas[0] != '"' or lemmas[-1] != '"':
                raise ConfigError("Lemmas must be enclosed in double quotes")
            StaticPhrases.DETAILS[phrase] = (tags[1:-1], lemmas[1:-1])

        # Dictionary structure: dict { firstword: [ (restword_list, phrase_index) ] }

        # Split phrase into words
        wlist = phrase.split()
        # Dictionary is keyed by first word
        StaticPhrases.DICT[wlist[0]].append((wlist[1:], ix))

    @staticmethod
    def add_errors(words: str, error: Tuple[str, str, str, str]) -> None:
        # Dictionary structure:
        # { phrase : (error_code, right_phrase, right_tag_string, right_lemma_string) }
        StaticPhrases.ERROR_DICT[words] = error

    @staticmethod
    def set_meaning(meaning: Iterable) -> None:
        """ Set the default meaning for static phrases """
        StaticPhrases.MEANING = cast(StaticPhraseTuple, tuple(meaning))
        assert len(StaticPhrases.MEANING) == 3

    @staticmethod
    def get_meaning(ix: int) -> List[MeaningTuple]:
        """ Return the meaning of the phrase with index ix """
        return [StaticPhrases.LIST[ix][1]]

    @staticmethod
    def get_length(ix: int) -> int:
        """ Return the length of the phrase with index ix """
        return len(StaticPhrases.LIST[ix][0].split())

    @staticmethod
    def lookup(phrase: str) -> Optional[MeaningTuple]:
        """ Lookup an entire phrase """
        return StaticPhrases.MAP.get(phrase)

    @staticmethod
    def has_details(phrase: str) -> bool:
        """ Return True if tag and lemma details are available for this phrase """
        return phrase in StaticPhrases.DETAILS

    @staticmethod
    def tags(phrase: str) -> Optional[List[str]]:
        """ Lookup a list of IFD tags for a phrase, if available """
        details = StaticPhrases.DETAILS.get(phrase)
        return None if details is None else details[0].split()

    @staticmethod
    def lemmas(phrase: str) -> Optional[List[str]]:
        """ Lookup a list of lemmas for a phrase, if available """
        details = StaticPhrases.DETAILS.get(phrase)
        return None if details is None else details[1].split()


class AmbigPhrases:

    """ Wrapper around dictionary of potentially ambiguous phrases,
        initialized from the config file """

    # List of tuples of ambiguous phrases and their word category lists,
    # i.e. (words, cats) where words and cats are tuples
    LIST = []  # type: List[Tuple[Tuple[str, ...], Tuple[str, ...]]]
    # Parsing dictionary keyed by first word of phrase
    DICT = defaultdict(list)  # type: Dict[str, List[Tuple[List[str], int]]]
    # Error dictionary, { phrase : (error_code, right_phrase, right_parts_of_speech) }
    ERROR_DICT = defaultdict(list)  # type: Dict[str, List[Tuple[str, ...]]]

    @staticmethod
    def add(words, cats):
        """ Add an ambiguous phrase to the dictionary.
            Called from the config file handler. """

        # First add to phrase list
        ix = len(AmbigPhrases.LIST)

        # Append the phrase as well as its meaning in tuple form
        AmbigPhrases.LIST.append((words, cats))

        # Dictionary structure: dict { firstword: [ (restword_list, phrase_index) ] }
        AmbigPhrases.DICT[words[0]].append((words[1:], ix))

    @staticmethod
    def add_error(words, error):
        # Dictionary structure:
        # dict { phrase : (error_code, right_phrase, right_parts_of_speech) }
        AmbigPhrases.ERROR_DICT[words].append(error)

    @staticmethod
    def get_cats(ix):
        """ Return the word categories for the phrase with index ix """
        return AmbigPhrases.LIST[ix][1]

    @staticmethod
    def get_words(ix):
        """ Return the words for the phrase with index ix """
        return AmbigPhrases.LIST[ix][0]


class NoIndexWords:

    """ Wrapper around set of word stems and categories that should
        not be indexed """

    # Set of (stem, cat) tuples
    SET = set()  # type: Set[Tuple[str, str]]
    # Default category
    _CAT = "so"

    # The word categories that are indexed in the words table
    CATEGORIES_TO_INDEX = frozenset(
        ("kk", "kvk", "hk", "person_kk", "person_kvk", "entity", "lo", "so")
    )  # Type: Set[str]

    @staticmethod
    def set_cat(cat):
        """ Set the category for the following word stems """
        NoIndexWords._CAT = cat

    @staticmethod
    def add(stem):
        """ Add a word stem and its category. Called from the config file handler. """
        NoIndexWords.SET.add((stem, NoIndexWords._CAT))


class Topics:

    """ Wrapper around topics, represented as a dict (name: set) """

    # Dict of topic name: set
    DICT = defaultdict(set)  # type: Dict[str, Set[str]]
    # Dict of identifier: topic name
    ID = dict()  # type: Dict[str, str]
    # Dict of identifier: threshold (as a float)
    THRESHOLD = dict()  # type: Dict[str, Optional[float]]
    _name = None  # type: Optional[str]

    @staticmethod
    def set_name(name):
        """ Set the topic name for the words that follow """
        a = name.split("|")
        Topics._name = tname = a[0].strip()
        identifier = a[1].strip() if len(a) > 1 else None
        if identifier is not None and not identifier.isidentifier():
            raise ConfigError(
                "Topic identifier ('{0}') must be a valid Python identifier".format(
                    identifier
                )
            )
        try:
            threshold = float(a[2].strip()) if len(a) > 2 else None
        except ValueError:
            raise ConfigError("Topic threshold must be a floating point number")
        Topics.ID[tname] = identifier
        Topics.THRESHOLD[tname] = threshold

    @staticmethod
    def add(word):
        """ Add a word stem and its category. Called from the config file handler. """
        if Topics._name is None:
            raise ConfigError(
                "Must set topic name (topic = X) before specifying topic words"
            )
        if "/" not in word:
            raise ConfigError(
                "Topic words must include a slash '/' and a word category"
            )
        cat = word.split("/", maxsplit=1)[1]
        if cat not in {
            "kk",
            "kvk",
            "hk",
            "lo",
            "so",
            "entity",
            "person",
            "person_kk",
            "person_kvk",
        }:
            raise ConfigError(
                "Topic words must be nouns, verbs, adjectives, entities or persons"
            )
        # Add to topic set, after replacing spaces with underscores
        Topics.DICT[Topics._name].add(word.replace(" ", "_"))


class AdjectivePredicates:

    """ A set of arguments and prepositions associated with
        adjectives, for instance 'tengdur þgf', typically read from
        the [adjective_predicates] section of AdjectivePredicates.conf """

    # dict { adjective lemma : set of possible argument cases }
    ARGUMENTS = defaultdict(set)  # type: Dict[str, Set[str]]
    # dict { adjective lemma : set of (preposition, case) }
    PREPOSITIONS = defaultdict(set)  # type: Dict[str, Set[Tuple[str, str]]]

    # dict { adjective lemma : [ (argument case, error code) ] }
    ERROR_DICT = defaultdict(list)  # type: Dict[str, List[Tuple[str, str]]]

    # dict { adjective lemma : set of (preposition, case) }
    ERROR_PREPOSITIONS = defaultdict(set)  # type: Dict[str, Set[Tuple[str, str]]]

    @staticmethod
    def add(adj, arg, prepositions):
        if arg:
            # Add a case that is associated with an adjective
            AdjectivePredicates.ARGUMENTS[adj].update(arg)
        if prepositions:
            # Add a (preposition, case) tuple that is associated with an adjective
            AdjectivePredicates.PREPOSITIONS[adj].update(prepositions)

    @staticmethod
    def add_error(adj, arg, prepositions, error):
        if arg and error:
            for a in arg:
                AdjectivePredicates.ERROR_DICT[adj].append((a, error))
        if prepositions:
            AdjectivePredicates.ERROR_PREPOSITIONS[adj].update(prepositions)


class Preferences:

    """ Wrapper around disambiguation hints, initialized from the config file """

    # Dictionary keyed by word containing a list of tuples (worse, better)
    # where each is a list of terminal prefixes
    DICT = defaultdict(list)  # type: Dict[str, List[PreferenceTuple]]

    @staticmethod
    def add(word: str, worse: List[str], better: List[str], factor: int) -> None:
        """ Add a preference to the dictionary. Called from the config file handler. """
        Preferences.DICT[word].append((worse, better, factor))

    @staticmethod
    def get(word: str) -> Optional[List[PreferenceTuple]]:
        """ Return a list of (worse, better, factor) tuples for the given word """
        return Preferences.DICT.get(word, None)


class StemPreferences:

    """ Wrapper around stem disambiguation hints, initialized from the config file """

    # Dictionary keyed by word form containing a tuple (worse, better)
    # where each is a list word stems
    DICT = dict()  # type: Dict[str, Tuple[List[str], List[str]]]

    @staticmethod
    def add(word, worse, better):
        """ Add a preference to the dictionary. Called from the config file handler. """
        if word in StemPreferences.DICT:
            raise ConfigError(
                "Duplicate stem preference for word form {0}".format(word)
            )
        StemPreferences.DICT[word] = (worse, better)

    @staticmethod
    def get(word):
        """ Return a (worse, better) tuple for the given word form """
        return StemPreferences.DICT.get(word, None)


class NounPreferences:

    """ Wrapper for noun preferences, i.e. to assign priorities to different
        noun stems that can have identical word forms. """

    # This is a dict of noun word forms, giving the relative priorities
    # of different genders
    DICT = defaultdict(dict)  # type: Dict[str, Dict[str, int]]

    @staticmethod
    def add(word, worse, better):
        """ Add a preference to the dictionary. Called from the config file handler. """
        if worse not in _ALL_GENDERS or better not in _ALL_GENDERS:
            raise ConfigError("Noun priorities must specify genders (kk, kvk, hk)")
        d = NounPreferences.DICT[word]
        worse_score = d.get(worse)
        better_score = d.get(better)
        if worse_score is not None:
            if better_score is not None:
                raise ConfigError("Conflicting priorities for noun {0}".format(word))
            better_score = worse_score + 4
        elif better_score is not None:
            worse_score = better_score - 4
        else:
            worse_score = -2
            better_score = 2
        d[worse] = worse_score
        d[better] = better_score
        # print("Noun prefs for '{0}' are now {1}".format(word, d))


class NamePreferences:

    """ Wrapper around well-known person names, initialized from the config file """

    SET = set()  # type: Set[str]

    @staticmethod
    def add(name):
        """ Add a preference to the dictionary. Called from the config file handler. """
        NamePreferences.SET.add(name)


class BinErrata:

    """ Wrapper around BÍN errata, initialized from the config file """

    DICT = dict()  # type: Dict[Tuple[str, str], str]

    @staticmethod
    def add(stem, ordfl, fl):
        """ Add a BÍN fix. Used by bincompress.py when generating a new
            compressed vocabulary file. """
        BinErrata.DICT[(stem, ordfl)] = fl


class BinDeletions:

    """ Wrapper around BÍN deletions, initialized from the config file """

    SET = set()  # type: Set[Tuple[str, str, str]]

    @staticmethod
    def add(stem, ordfl, fl):
        """ Add a BÍN fix. Used by bincompress.py when generating a new
            compressed vocabulary file. """
        BinDeletions.SET.add((stem, ordfl, fl))


# Global settings


class Settings:

    _lock = threading.Lock()
    loaded = False

    # Postgres SQL database server hostname and port
    DB_HOSTNAME = os.environ.get("GREYNIR_DB_HOST", "localhost")
    # Default PostgreSQL port
    DB_PORT = os.environ.get("GREYNIR_DB_PORT", "5432")  # type: Union[str,int]

    try:
        DB_PORT = int(DB_PORT)
    except ValueError:
        raise ConfigError(
            "Invalid environment variable value: DB_PORT = {0}".format(DB_PORT)
        )

    BIN_DB_HOSTNAME = os.environ.get("GREYNIR_BIN_DB_HOST", DB_HOSTNAME)
    BIN_DB_PORT = os.environ.get("GREYNIR_BIN_DB_PORT", DB_PORT)  # type: Union[str,int]

    try:
        BIN_DB_PORT = int(BIN_DB_PORT)
    except ValueError:
        raise ConfigError(
            "Invalid environment variable value: BIN_DB_PORT = {0}".format(BIN_DB_PORT)
        )

    # Flask server host and port
    HOST = os.environ.get("GREYNIR_HOST", "localhost")
    PORT = os.environ.get("GREYNIR_PORT", "5000")  # type: Union[str,int]
    try:
        PORT = int(PORT)
    except ValueError:
        raise ConfigError(
            "Invalid environment variable value: GREYNIR_PORT = {0}".format(PORT)
        )

    # Flask debug parameter
    DEBUG = False

    # Similarity server
    SIMSERVER_HOST = os.environ.get("SIMSERVER_HOST", "localhost")
    SIMSERVER_PORT = os.environ.get("SIMSERVER_PORT", "5001")  # type: Union[str,int]
    try:
        SIMSERVER_PORT = int(SIMSERVER_PORT)
    except ValueError:
        raise ConfigError(
            "Invalid environment variable value: SIMSERVER_PORT = {0}".format(
                SIMSERVER_PORT
            )
        )

    # Configuration settings from the GreynirPackage.conf file

    @staticmethod
    def _handle_settings(s: str) -> None:
        """ Handle config parameters in the settings section """
        a = s.lower().split("=", maxsplit=1)
        par = a[0].strip().lower()
        sval = a[1].strip()
        val = sval  # type: Union[None, str, bool]
        if sval.lower() == "none":
            val = None
        elif sval.lower() == "true":
            val = True
        elif sval.lower() == "false":
            val = False
        try:
            if par == "db_hostname":
                if not isinstance(val, str):
                    raise ConfigError("Expected database host name as a string")
                Settings.DB_HOSTNAME = Settings.BIN_DB_HOSTNAME = val
            elif par == "db_port":
                if not isinstance(val, str):
                    raise ConfigError("Expected port number")
                Settings.DB_PORT = Settings.BIN_DB_PORT = int(val)
            elif par == "host":
                if not isinstance(val, str):
                    raise ConfigError("Expected host name as a string")
                Settings.HOST = val
            elif par == "port":
                if not isinstance(val, str):
                    raise ConfigError("Expected port number")
                Settings.PORT = int(val)
            elif par == "simserver_host":
                if not isinstance(val, str):
                    raise ConfigError("Expected simserver host name as a string")
                Settings.SIMSERVER_HOST = val
            elif par == "simserver_port":
                if not isinstance(val, str):
                    raise ConfigError("Expected port number")
                Settings.SIMSERVER_PORT = int(val)
            elif par == "debug":
                Settings.DEBUG = bool(val)
            else:
                raise ConfigError("Unknown configuration parameter '{0}'".format(par))
        except ValueError:
            raise ConfigError("Invalid parameter value: {0} = {1}".format(par, val))

    @staticmethod
    def _handle_static_phrases(s: str) -> None:
        """ Handle static phrases in the settings section """
        error = False
        if "=" not in s:
            ix = s.rfind("$error(")  # Must be at the end
            if ix >= 0:
                error = True
                # A typical format is
                # $error(error_code, right_phrase, right_parts_of_speech)
                e = s[ix + 7 :].lstrip().rstrip(" )").split(",")
                if len(e) != 4:
                    raise ConfigError("Error pragma should have four parameters")
                s = s[:ix].strip()
            StaticPhrases.add(s)
            if error:
                StaticPhrases.add_errors(s.split(",")[0], (e[0], e[1], e[2], e[3]))
            return
        # Check for a meaning spec
        a = s.split("=", maxsplit=1)
        par = a[0].strip()
        val = a[1].strip()
        if par.lower() == "meaning":
            m = val.split()
            if len(m) == 3:
                StaticPhrases.set_meaning(m)
            else:
                raise ConfigError("Meaning in static_phrases should have 3 arguments")
        else:
            raise ConfigError(
                "Unknown configuration parameter '{0}' in static_phrases".format(par)
            )

    @staticmethod
    def _handle_abbreviations(s: str) -> None:
        """ Handle abbreviations in the settings section """
        # Not required in the GreynirPackage module
        # and should not occur in its settings files
        assert False

    @staticmethod
    def _handle_meanings(s: str) -> None:
        """ Handle additional word meanings in the settings section """
        # Not required in the GreynirPackage module
        # and should not occur in its settings files
        assert False

    @staticmethod
    def _handle_verb_objects(s: str) -> None:
        """ Handle verb object specifications in the settings section """
        # Format: verb [arg1] [arg2] [/preposition arg]... [*particle] [$pragma(txt)]
        # arg can be nf, þf, þgf, ef, nh, falls, sig/sér/sín, bági_kk_ft_þf

        # Start by handling the $score() pragma, if present
        score = 0
        ix = s.rfind("$score(")  # Must be at the end
        if ix >= 0:
            sc = s[ix:]
            s = s[0:ix].strip()
            if not sc.endswith(")"):
                raise ConfigError("Invalid score pragma; form should be $score(n)")
            # There is an associated score with this verb form, to be taken
            # into consideration by the reducer
            sc = sc[7:-1].strip()
            try:
                score = int(sc)
            except ValueError:
                raise ConfigError("Invalid score ('{0}') for verb form".format(sc))

        # Check for $error
        error = None
        ix = s.rfind("$error(")
        if ix >= 0:
            if not s.endswith(")"):
                raise ConfigError("Invalid error pragma; form should be $error(...)")
            error = s[ix + 7 : -1].strip()
            s = s[0:ix].strip()
            if not error:
                raise ConfigError("Expected error specification in $error(...)")

        # Process particles, should only be one in each line
        particle = None
        ix = s.rfind("*")
        if ix >= 0:
            particle = s[ix:].strip()
            s = s[0:ix].strip()
            if " " in particle:
                raise ConfigError("Particle should only be one word")
            elif len(particle) < 2:
                raise ConfigError("Particle should be at least one letter")

        # Process preposition arguments, if any
        prepositions = []  # type: List[Tuple[str, str]]
        ap = s.split("/")
        s = ap[0]
        ix = 1
        while ix < len(ap):
            # We expect something like 'af þgf', or possibly
            # 'fyrir_hönd þf' (where the underscore needs to be replaced by a space)
            p = ap[ix].strip()
            parg = p.split()
            if len(parg) != 2:
                raise ConfigError("Preposition should have exactly one argument")
            if parg[1] not in _ALL_CASES and parg[1] not in _SUBCLAUSES:
                parg[1] = _REFLPRN.get(parg[1], parg[1])
                spl = parg[1].split("_")
                if spl[-1] == "gr":
                    spl = spl[:-1]
                if spl[-1] not in _ALL_CASES:
                    raise ConfigError("Preposition argument must have a case as its last variant")
            prepositions.append((parg[0].replace("_", " "), parg[1]))
            ix += 1

        # Process verb arguments
        a = s.split()
        if len(a) < 1 or len(a) > 3:
            raise ConfigError("Verb should have zero, one or two arguments")
        verb = a[0]
        if not verb.isalpha():
            raise ConfigError("Verb '{0}' is not a valid word".format(verb))

        # Add to verb database
        if error:
            VerbObjects.add_error(verb, a[1:], prepositions, particle, error)
        else:
            VerbObjects.add(verb, a[1:], prepositions, particle, score)

    @staticmethod
    def _handle_verb_subjects(s):
        """ Handle verb subject specifications in the settings section """
        # Format: subject = [case] followed by verb list
        a = s.lower().split("=", maxsplit=1)
        if len(a) == 2:
            par = a[0].strip()
            val = a[1].strip()
            if par == "subject":
                VerbSubjects.set_case(val)
            else:
                raise ConfigError("Unknown setting '{0}' in verb_subjects".format(par))
            return
        assert len(a) == 1
        par = s.strip()
        # Check for $error
        e = None
        ix = par.rfind("$error(")
        if ix >= 0:
            if par[-1] != ")":
                raise ConfigError("Missing right parenthesis in $error()")
            e = par[ix + 7 : -1].strip()
            par = par[0:ix].strip()

        if e is not None:
            VerbSubjects.add_error(par, e)
        else:
            VerbSubjects.add(par)

    @staticmethod
    def _handle_undeclinable_adjectives(s):
        """ Handle list of undeclinable adjectives """
        s = s.lower().strip()
        if not s.isalpha():
            raise ConfigError(
                "Expected word but got '{0}' in undeclinable_adjectives".format(s)
            )
        UndeclinableAdjectives.add(s)

    @staticmethod
    def _handle_noindex_words(s):
        """ Handle no index instructions in the settings section """
        # Format: category = [cat] followed by word stem list
        a = s.lower().split("=", maxsplit=1)
        par = a[0].strip()
        if len(a) == 2:
            val = a[1].strip()
            if par == "category":
                NoIndexWords.set_cat(val)
            else:
                raise ConfigError("Unknown setting '{0}' in noindex_words".format(par))
            return
        assert len(a) == 1
        NoIndexWords.add(par)

    @staticmethod
    def _handle_topics(s):
        """ Handle topic specifications """
        # Format: name = [topic name] followed by word stem list in the form word/cat
        a = s.split("=", maxsplit=1)
        par = a[0].strip()
        if len(a) == 2:
            val = a[1].strip()
            if par.lower() == "topic":
                Topics.set_name(val)
            else:
                raise ConfigError("Unknown setting '{0}' in topics".format(par))
            return
        assert len(a) == 1
        Topics.add(par)

    @staticmethod
    def _handle_prepositions(s):
        """ Handle preposition specifications in the settings section """
        # Format: pw1 pw2... case [nh]  [$error(X)]
        error = False
        corr = None  # type: Optional[Tuple[str, Optional[str]]]
        ix = s.rfind("$error(")  # Must be at the end
        if ix >= 0:
            # A typical format is $error(FORM-inn_á)
            error = True
            e = s[ix + 7 :].lstrip().rstrip(" )").split("-")
            if len(e) == 2:
                # Probably $error(FORM-xxx_xxx)
                corr = (e[0], " ".join(e[1].split("_")))
            elif len(e) == 1:
                # Probably $error(COMPOUND)
                corr = (e[0], None)
            else:
                raise ConfigError(
                    "$error() pragma should have the form XXX[-yyy] "
                    "where XXX is a category and yyy is a phrase"
                )
            s = s[:ix].strip()
        a = s.split()
        if len(a) < 2:
            raise ConfigError("Preposition must specify a word and a case argument")
        c = a[-1]  # Case or 'nh'
        nh = c == "nh"
        if nh:
            # This is a preposition that can be followed by an infinitive verb phrase:
            # 'Beiðnin um að handtaka manninn var send lögreglunni'
            a = a[:-1]
            if len(a) < 2:
                raise ConfigError(
                    "Preposition must specify a word, case and 'nh' argument"
                )
            c = a[-1]
        if c not in {"nf", "þf", "þgf", "ef"}:  # Not a valid case
            raise ConfigError("Preposition must have a case argument (nf/þf/þgf/ef)")
        # Preposition, possibly multi-word, and possibly suffixed by an asterisk
        pp = " ".join(a[:-1])
        Prepositions.add(pp, c, nh)
        if error:
            assert corr is not None
            Prepositions.add_error(pp, c, corr)

    @staticmethod
    def _handle_preferences(s):
        """ Handle ambiguity preference hints in the settings section """
        # Format: word worse1 worse2... < better
        # If two less-than signs are used, the preference is even stronger (tripled)
        # If three less-than signs are used, the preference is super strong (nine-fold)
        factor = 9
        a = s.lower().split("<<<", maxsplit=1)
        if len(a) != 2:
            factor = 3
            a = s.lower().split("<<", maxsplit=1)
            if len(a) != 2:
                # Not doubled preference: try a normal one
                a = s.lower().split("<", maxsplit=1)
                factor = 1
        if len(a) != 2:
            raise ConfigError("Ambiguity preference missing less-than sign '<'")
        w = a[0].split()
        if len(w) < 2:
            raise ConfigError(
                "Ambiguity preference must have at least one 'worse' category"
            )
        b = a[1].split()
        if len(b) < 1:
            raise ConfigError(
                "Ambiguity preference must have at least one 'better' category"
            )
        Preferences.add(w[0], w[1:], b, factor)

    @staticmethod
    def _handle_stem_preferences(s):
        """ Handle stem ambiguity preference hints in the settings section """
        # Format: word worse1 worse2... < better
        a = s.lower().split("<", maxsplit=1)
        if len(a) != 2:
            raise ConfigError("Ambiguity preference missing less-than sign '<'")
        w = a[0].split()
        if len(w) < 2:
            raise ConfigError(
                "Ambiguity preference must have at least one 'worse' category"
            )
        b = a[1].split()
        if len(b) < 1:
            raise ConfigError(
                "Ambiguity preference must have at least one 'better' category"
            )
        StemPreferences.add(w[0], w[1:], b)

    @staticmethod
    def _handle_noun_preferences(s):
        """ Handle noun preference hints in the settings section """
        # Format: noun worse1 worse2... < better
        # The worse and better specifiers are gender names (kk, kvk, hk)
        a = s.lower().split("<", maxsplit=1)
        if len(a) != 2:
            raise ConfigError("Noun preference missing less-than sign '<'")
        w = a[0].split()
        if len(w) != 2:
            raise ConfigError("Noun preference must have exactly one 'worse' gender")
        b = a[1].split()
        if len(b) != 1:
            raise ConfigError("Noun preference must have exactly one 'better' gender")
        NounPreferences.add(w[0], w[1], b[0])

    @staticmethod
    def _handle_name_preferences(s):
        """ Handle well-known person names in the settings section """
        NamePreferences.add(s)

    @staticmethod
    def _handle_bin_errata(s):
        """ Handle changes to BÍN categories ('fl') """
        a = s.split()
        if len(a) != 3:
            raise ConfigError("Expected 'stem ordfl fl' fields in bin_errata section")
        stem, ordfl, fl = a
        if not ordfl.islower() or not fl.islower():
            raise ConfigError(
                "Expected lowercase ordfl and fl fields in bin_errata section"
            )
        BinErrata.add(stem, ordfl, fl)

    @staticmethod
    def _handle_bin_deletions(s):
        """ Handle deletions from BÍN, given as stem/ordfl/fl triples """
        a = s.split()
        if len(a) != 3:
            raise ConfigError(
                "Expected 'stem ordfl fl' fields in bin_deletions section"
            )
        stem, ordfl, fl = a
        if not ordfl.islower() or not fl.islower():
            raise ConfigError(
                "Expected lowercase ordfl and fl fields in bin_deletions section"
            )
        BinDeletions.add(stem, ordfl, fl)

    @staticmethod
    def _handle_ambiguous_phrases(s):
        """ Handle ambiguous phrase guidance in the settings section """
        # Format: "word1 word2..." cat1 cat2...
        error = False
        if s[0] != '"':
            raise ConfigError("Ambiguous phrase must be enclosed in double quotes")
        ix = s.rfind("$error(")  # Must be at the end
        if ix >= 0:
            error = True
            # A typical format is
            # $error(error_code, right_phrase, right_parts_of_speech)
            e = s[ix + 7 :].lstrip().rstrip(" )").split(", ")
            s = s[:ix].strip()
        q = s.rfind('"')
        if q <= 0:
            raise ConfigError("Ambiguous phrase must be enclosed in double quotes")
        # Obtain a list of the words in the phrase
        words = s[1:q].strip().lower().split()
        if any("*" in word and not word.endswith("*") for word in words):
            raise ConfigError("An asterisk is only allowed at the end of lemmas")
        if len(words) < 2:
            raise ConfigError("Ambiguous phrase must contain at least two words")
        # Obtain a list of the corresponding word categories
        cats = s[q + 1 :].strip().lower().split()
        if len(words) != len(cats):
            raise ConfigError(
                "Ambiguous phrase has {0} words but {1} category sets".format(
                    len(words), len(cats)
                )
            )
        # Convert the list of category specifiers to a tuple of frozensets of
        # word categories
        cats_t = tuple(frozenset(cat.split("/")) for cat in cats)
        # Check for something like ao/ or so//fs
        if any("" in cats_set for cats_set in cats_t):
            raise ConfigError("Empty category set not allowed")
        # Check for something like ao/*
        if any("*" in cats_set and len(cats_set) > 1 for cats_set in cats_t):
            raise ConfigError("Redundant category specified alongside wildcard '*'")
        AmbigPhrases.add(words, cats_t)
        if error:
            AmbigPhrases.add_error(s[1:q].strip().lower(), e)

    @staticmethod
    def _handle_adjective_template(s):
        """ Handle the template for new adjectives in the settings section """
        # Format: adjective-ending bin-meaning
        a = s.split()
        if len(a) != 2:
            raise ConfigError(
                "Adjective template should have an ending and a form specifier"
            )
        AdjectiveTemplate.add(a[0], a[1])

    @staticmethod
    def _handle_disallowed_names(s):
        """ Handle disallowed person name forms from the settings section """
        # Format: Name-stem case1 case2...
        a = s.split()
        if len(a) < 2:
            raise ConfigError(
                "Disallowed names must specify a name and at least one case"
            )
        DisallowedNames.add(a[0], a[1:])

    @staticmethod
    def _handle_adjective_predicates(s):
        # Process preposition arguments, if any
        error = False
        ix = s.rfind("$error(")  # Must be at the end
        if ix >= 0:
            error = True
            # A typical format is
            # $error(error_code, right_phrase, right_parts_of_speech)
            e = s[ix + 7 :].lstrip().rstrip(" )").split(",")
            s = s[:ix].strip()

        prepositions = []
        ap = s.split("/")
        s = ap[0]
        ix = 1
        while len(ap) > ix:
            # We expect something like 'af þgf'
            p = ap[ix].strip()
            parg = p.split()
            if len(parg) != 2:
                raise ConfigError("Preposition should have exactly one argument")
            if parg[1] not in _ALL_CASES:
                raise ConfigError("Unknown argument case for preposition")
            prepositions.append((parg[0], parg[1]))
            ix += 1
        a = s.split()
        adj = a[0]
        if error:
            AdjectivePredicates.add_error(adj, a[1:], prepositions, e)
        else:
            AdjectivePredicates.add(adj, a[1:], prepositions)

    @staticmethod
    def read(fname):
        """ Read configuration file """

        with Settings._lock:

            if Settings.loaded:
                return

            CONFIG_HANDLERS = {
                "settings": Settings._handle_settings,
                "static_phrases": Settings._handle_static_phrases,
                "abbreviations": Settings._handle_abbreviations,
                "verb_objects": Settings._handle_verb_objects,
                "verb_subjects": Settings._handle_verb_subjects,
                "prepositions": Settings._handle_prepositions,
                "preferences": Settings._handle_preferences,
                "noun_preferences": Settings._handle_noun_preferences,
                "name_preferences": Settings._handle_name_preferences,
                "stem_preferences": Settings._handle_stem_preferences,
                "ambiguous_phrases": Settings._handle_ambiguous_phrases,
                "meanings": Settings._handle_meanings,
                "adjective_template": Settings._handle_adjective_template,
                "undeclinable_adjectives": Settings._handle_undeclinable_adjectives,
                "disallowed_names": Settings._handle_disallowed_names,
                "noindex_words": Settings._handle_noindex_words,
                "topics": Settings._handle_topics,
                "adjective_predicates": Settings._handle_adjective_predicates,
                "bin_errata": Settings._handle_bin_errata,
                "bin_deletions": Settings._handle_bin_deletions,
            }
            handler = None  # Current section handler

            rdr = None
            try:
                rdr = LineReader(fname)
                for s in rdr.lines():
                    # Ignore comments
                    ix = s.find("#")
                    if ix >= 0:
                        s = s[0:ix]
                    s = s.strip()
                    if not s:
                        # Blank line: ignore
                        continue
                    if s[0] == "[" and s[-1] == "]":
                        # New section
                        section = s[1:-1].strip().lower()
                        if section in CONFIG_HANDLERS:
                            handler = CONFIG_HANDLERS[section]
                            continue
                        raise ConfigError("Unknown section name '{0}'".format(section))
                    if handler is None:
                        raise ConfigError("No handler for config line '{0}'".format(s))
                    # Call the correct handler depending on the section
                    try:
                        handler(s)
                    except ConfigError as e:
                        # Add file name and line number information to the exception
                        # if it's not already there
                        e.set_pos(rdr.fname(), rdr.line())
                        raise e

            except ConfigError as e:
                # Add file name and line number information to the exception
                # if it's not already there
                if rdr:
                    e.set_pos(rdr.fname(), rdr.line())
                raise e

            Settings.loaded = True
