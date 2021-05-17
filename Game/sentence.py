from typing import List, Optional

from Game.game_obect_types import GameObjectType, GOCategory, TEXT_REFERRALS
from Game.game_object import GameObject


class SentenceNoun:
    def __init__(self, object_type: GameObjectType):
        self.object_type = object_type


class SentenceVerb:
    def __init__(self, object_type: GameObjectType):
        self.object_type = object_type


class SentenceAttribute:
    def __init__(self, object_type: GameObjectType):
        self.object_type = object_type


class Sentence:
    def __init__(self, verb: SentenceVerb, target: SentenceNoun, attribute: SentenceAttribute, objects: List[GameObject]):
        self.verb = verb
        self.target = target
        self.attribute = attribute
        self.objects = objects

    def gives_prop(self, prop: GameObjectType) -> bool:
        return self.verb.object_type == GameObjectType.T_IS and prop == self.attribute.object_type

    def targets_object(self, go: GameObject) -> bool:
        return (self.verb.object_type == GameObjectType.T_IS and
                TEXT_REFERRALS.get(self.target.object_type, None) == go.object_type)

    def targets_type(self, go: GameObjectType) -> bool:
        return (self.verb.object_type == GameObjectType.T_IS and
                TEXT_REFERRALS.get(self.target.object_type, None) == go)

    def get_protected_objects(self) -> List[GameObjectType]:
        if self.verb.object_type == GameObjectType.T_IS and self.target.object_type == self.attribute.object_type:
            return [TEXT_REFERRALS[self.target.object_type]]
        else:
            return []

    def is_transformation(self) -> bool:
        return (self.verb.object_type == GameObjectType.T_IS and
                self.attribute.object_type.get_category() == GOCategory.NOUN and
                self.attribute.object_type != self.target.object_type)

    def transformation_types(self) -> List[GameObjectType]:
        return [self.attribute.object_type]


def parse_sentence(words: List[GameObject]) -> Optional[Sentence]:
    i = {
        0: 0,
        1: []
    }

    def in_range() -> bool:
        return i[0] < len(words)

    def get_noun() -> Optional[SentenceNoun]:
        if not in_range(): return None
        if words[i[0]].object_type.get_category() == GOCategory.NOUN:
            i[1].append(words[i[0]])
            i[0] += 1
            return SentenceNoun(words[i[0] - 1].object_type)
        else:
            return None

    def get_noun_or_prop() -> Optional[SentenceAttribute]:
        if not in_range(): return None
        if words[i[0]].object_type.get_category() in [GOCategory.NOUN, GOCategory.PROPERTY]:
            i[1].append(words[i[0]])
            i[0] += 1
            return SentenceAttribute(words[i[0] - 1].object_type)
        else:
            return None

    def get_verb() -> Optional[SentenceVerb]:
        if not in_range(): return None
        if words[i[0]].object_type.get_category() == GOCategory.VERB:
            i[1].append(words[i[0]])
            i[0] += 1
            return SentenceVerb(words[i[0] - 1].object_type)
        else:
            return None

    def get_phrase() -> Optional[Sentence]:
        noun = get_noun()
        if noun is None: return None
        verb = get_verb()
        if verb is None: return None
        target = get_noun_or_prop()
        if target is None: return None
        if in_range(): return None  # there is extra stuff at the end of the sentence
        return Sentence(verb, noun, target, i[1])

    return get_phrase()


def is_valid_sentence(words: List[GameObject]) -> bool:
    return parse_sentence(words) is not None
