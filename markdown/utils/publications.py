import datetime
from collections.abc import Sequence
from enum import Enum, auto
from typing import NamedTuple

from pydantic import BaseModel, ConfigDict, RootModel, model_validator


# Later states must come later in the enum
class State(Enum):
    # Intermediate
    SUBMITTED = auto()
    ACCEPTED = auto()
    # Bad end states
    ABANDONED = auto()
    WITHDRAWN = auto()
    REJECTED = auto()
    # Good end states
    SELF_PUBLISHED = auto()
    PUBLISHED = auto()


class Date(NamedTuple):
    state: State
    date: datetime.date


class Publication(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        strict=True,
        extra="forbid",
        alias_generator=lambda s: s.replace("_", "-"),
    )

    venue: str
    urls: Sequence[str] = []
    notes: str = ""
    paid: str = ""
    submitted: datetime.date | None = None
    accepted: datetime.date | None = None
    abandoned: datetime.date | None = None
    withdrawn: datetime.date | None = None
    rejected: datetime.date | None = None
    self_published: datetime.date | None = None
    published: datetime.date | None = None

    @property
    def dates(self) -> tuple[Date, ...]:
        return tuple(d for d in self._all_dates() if d)

    @property
    def latest(self) -> Date:
        return self.dates[-1]

    @property
    def active(self) -> bool:
        return not [d for d in self._bad_end_dates() if d]

    @model_validator(mode="after")
    def _validate(self) -> "Publication":
        if not any(self._all_dates()):
            raise ValueError("At least one date must be set")

        if len([d for d in self._end_dates() if d]) > 1:
            raise ValueError("At most one end date can be set")

        if self.self_published and any(self._intermediate_dates()):
            raise ValueError("Intermediate dates cannot be used with self_published")

        if self.accepted and any(self._bad_end_dates()):
            raise ValueError("Bad end dates cannot be used with accepted")

        if self.published and not all(self._intermediate_dates()):
            raise ValueError("All intermediate dates must be set when published is set")

        if any(self._bad_end_dates()) and not self.submitted:
            raise ValueError("Submitted must be set if any bad end dates are set")

        dates = [d.date for d in self._all_dates() if d]
        if dates != sorted(dates):
            raise ValueError("Dates must be in increasing order")

        return self

    def _bad_end_dates(self) -> list[Date | None]:
        return Publication._filter_dates(
            (State.ABANDONED, self.abandoned),
            (State.WITHDRAWN, self.withdrawn),
            (State.REJECTED, self.rejected),
        )

    def _good_end_dates(self) -> list[Date | None]:
        return Publication._filter_dates(
            (State.SELF_PUBLISHED, self.self_published),
            (State.PUBLISHED, self.published),
        )

    def _end_dates(self) -> list[Date | None]:
        return self._bad_end_dates() + self._good_end_dates()

    def _intermediate_dates(self) -> list[Date | None]:
        return Publication._filter_dates(
            (State.SUBMITTED, self.submitted),
            (State.ACCEPTED, self.accepted),
        )

    def _all_dates(self) -> list[Date | None]:
        return self._intermediate_dates() + self._end_dates()

    @staticmethod
    def _filter_dates(*dates: tuple[State, datetime.date | None]) -> list[Date | None]:
        out: list[Date | None] = []
        for s, d in dates:
            if d:
                out.append(Date(s, d))
            else:
                out.append(None)
        return out


class Publications(RootModel[Sequence[Publication]]):
    model_config = ConfigDict(
        frozen=True,
        strict=True,
    )

    @model_validator(mode="after")
    def _validate(self) -> "Publications":
        if not self.root:
            raise ValueError("No publications specified")
        return self

    @property
    def publications(self) -> Sequence[Publication]:
        return self.root

    @property
    def active(self) -> bool:
        return any(p.active for p in self.root)

    @property
    def highest_active_state(self) -> State | None:
        states = []
        for p in self.root:
            if p.active:
                d = p.latest
                states.append((d.state.value, d.state))
        states.sort()
        if states:
            return states[-1][1]
        return None
