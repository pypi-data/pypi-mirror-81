from __future__ import annotations

from typing import Any, Callable, Dict, List, Union

import pandas as pd

from miner.friends import Friends
from miner.message.conversations import Conversations
from miner.person import Person
from miner.utils import utils


class People:
    """
    Class that manages and represents people from different kind of
    Facebook interactions.
    """

    def __init__(self, **kwargs: Any) -> None:
        self.source_map = self._get_source_map()
        self._data: Dict[str, Person] = self._get_data_from_source(**kwargs)

    def __iter__(self) -> Any:
        # NOTE: not sure if this is needed.
        # Wanted to try out object as its own iterator.
        return PeopleIterator(self)

    def get(self, output: Union[str, None] = None) -> str:
        """
        Exposed function for getting data on people.

        @param output: where do we want to write the return value,
        an be any of: {csv|json|/some/path.{json|csv}}.
        @return: either the data formatted as csv or json,
        or a success message about where was the data saved.
        """
        name = [person.name for person in self.data.values()]
        friend = [person.friend for person in self.data.values()]
        message_dir = [person.thread_path for person in self.data.values()]
        media_dir = [person.media_dir for person in self.data.values()]

        df = pd.DataFrame(
            {
                "name": name,
                "friend": friend,
                "message_dir": message_dir,
                "media_dir": media_dir,
            }
        )

        return utils.df_to_file(output, df)

    @property
    def data(self) -> Dict[str, Person]:
        return self._data

    @property
    def names(self) -> List[str]:
        return list(self._data.keys())

    def _get_source_map(self) -> Dict[str, Callable]:
        return {
            "friends": self._convert_friends_to_persons,
            "conversations": self._convert_conversation_partners_to_persons,
        }

    def _get_data_from_source(self, **kwargs: Any) -> Dict[str, Person]:
        data: Dict[str, Person] = {}
        for key, source in kwargs.items():
            other = data
            this = self.source_map[key](source)
            data = self._unify_people(this, other)
        return data

    @staticmethod
    def _unify_people(
        this: Dict[str, Person], other: Dict[str, Person]
    ) -> Dict[str, Person]:
        for name, person in this.items():
            if not other.get(name):
                other[name] = person
            else:
                other[name] = other.get(name) + person  # type: ignore
        return other

    @staticmethod
    def _convert_friends_to_persons(friends: Friends) -> Dict[str, Person]:
        persons = {}
        for i, friend in friends.data.iterrows():
            persons[friend["name"]] = Person(name=friend["name"], friend=True)
        return persons

    @staticmethod
    def _convert_conversation_partners_to_persons(
        conversations: Conversations,
    ) -> Dict[str, Person]:
        participant_to_channel_map = utils.particip_to_channel_mapping(
            conversations.group
        )
        persons = {}
        # looping over private message participants
        for name, convo in conversations.private.items():
            persons[name] = Person(
                name=name,
                messages=convo.data,
                thread_path=convo.metadata.thread_path,
                media_dir=convo.metadata.media_dir,
                member_of=participant_to_channel_map.get(name) or [],
            )
        # looping over group message participants
        for name, convos in participant_to_channel_map.items():
            if not persons.get(name):
                persons[name] = Person(
                    name=name, member_of=participant_to_channel_map[name]
                )
        return persons


class PeopleIterator:
    def __init__(self, container: People) -> None:
        self.container = container
        self.n = -1
        self.max = len(self.container.names)

    def __next__(self) -> Person:
        self.n += 1
        if self.n > self.max:
            raise StopIteration
        return self.container.data[self.container.names[self.n]]

    def __iter__(self) -> PeopleIterator:
        return self
