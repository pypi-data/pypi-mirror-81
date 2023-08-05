"""Guild objects."""

import datetime
from typing import Dict, List


class Guild:
    """Guild object."""

    def __init__(
        self,
        _id: str,
        created: datetime.datetime,
        name: str,
        name_lower: str,
        description: str,
        tag: str,
        tagColor: str,
        exp: int,
        members: List,
        achievements: Dict,
        ranks: List,
        joinable: bool,
        legacyRanking: int,
        publiclyListed: bool,
        hideGmTag: bool,
        preferredGames: List[str],
        chatMute: datetime.datetime,
        guildExpByGameType: Dict,
        banner: Dict,
    ) -> None:
        """Init object.

        Args:
            _id (str): Guild ID
            created (datetime.datetime): Timestamp the guild was created.
            name (str): Name of the guild.
            name_lower (str): Name of the guild in lower case.
            description (str): Description of the guild.
            tag (str): Guild tags.
            tagColor (str): Color of the guilds tag.
            exp (int): Guild EXP.
            members (List): List of members in the guild.
            achievements (Dict): Dict of guild achievements earned.
            ranks (List): List of guild ranks
            joinable (bool): If this guild can be joined using /g join
            legacyRanking (int): Ranking of the guild coins in the
                legacy guild system
            publiclyListed (bool): If this guild is publicly listed.
            hideGmTag (bool): If the guild master tag is hidden in guild chat
            preferredGames (List[str]): List of the guild's preferred games.
            chatMute (datetime.datetime): dateTime the guild chat will be
                unmuted at, 0 if not currently muted.
            guildExpByGameType (Dict): Dict of the EXP for this guild by
                which game it was earned in
            banner (Dict): Dict of this guild's Minecraft banner.
        """
        self._id = _id
        self.created = created
        self.name = name
        self.name_lower = name_lower
        self.description = description
        self.tag = tag
        self.tagColour = tagColor
        self.exp = exp
        self.members = members
        self.achievements = achievements
        self.ranks = ranks
        self.joinable = joinable
        self.legacyRanking = legacyRanking
        self.publiclyListed = publiclyListed
        self.hideGmTag = hideGmTag
        self.prefferedGames = preferredGames
        self.chatMute = chatMute
        self.guildExpByGameTYpe = guildExpByGameType
        self.banner = banner
