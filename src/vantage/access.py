"""Rôles and the Niveaux d'accès each one may see (see CONTEXT.md)."""

from enum import StrEnum

from vantage.corpus.model import AccessLevel

_LADDER = [AccessLevel.PUBLIC, AccessLevel.INTERNE, AccessLevel.CONFIDENTIEL]


class Role(StrEnum):
    """The Rôle is the account: one per Niveau d'accès (ADR 0002)."""

    EMPLOYE = "Employé"
    MANAGER = "Manager"
    CONFORMITE = "Conformité"

    @property
    def highest_level(self) -> AccessLevel:
        return {
            Role.EMPLOYE: AccessLevel.PUBLIC,
            Role.MANAGER: AccessLevel.INTERNE,
            Role.CONFORMITE: AccessLevel.CONFIDENTIEL,
        }[self]

    @property
    def visible_levels(self) -> tuple[AccessLevel, ...]:
        """Its highest level and everything below it on the ladder."""
        return tuple(_LADDER[: _LADDER.index(self.highest_level) + 1])
