import datetime
from collections.abc import Mapping, Sequence
from typing import Any, NamedTuple

_VENUE = "venue"
_PAID = "paid"
_NOTES = "notes"
_URLS = "urls"

SUBMITTED = "submitted"
ACCEPTED = "accepted"
ABANDONED = "abandoned"
WITHDRAWN = "withdrawn"
REJECTED = "rejected"
SELF_PUBLISHED = "self-published"
PUBLISHED = "published"

# Later states must come later in the sequence
_DATE_KEYS = (
    # Intermediate
    SUBMITTED,
    ACCEPTED,
    # Bad end states
    ABANDONED,
    WITHDRAWN,
    REJECTED,
    # Good end states
    SELF_PUBLISHED,
    PUBLISHED,
)

_KEYS = frozenset([*_DATE_KEYS, _VENUE, _PAID, _NOTES, _URLS])


class Date(NamedTuple):
    state: str
    date: datetime.date | None

    def date_str(self) -> str:
        if self.date:
            return self.date.isoformat()
        return ""


class Dates:
    def __init__(
        self,
        submitted: datetime.date | None = None,
        accepted: datetime.date | None = None,
        abandoned: datetime.date | None = None,
        withdrawn: datetime.date | None = None,
        rejected: datetime.date | None = None,
        self_published: datetime.date | None = None,
        published: datetime.date | None = None,
    ) -> None:
        super().__init__()

        self._submitted = Date(SUBMITTED, submitted)
        self._accepted = Date(ACCEPTED, accepted)
        self._abandoned = Date(ABANDONED, abandoned)
        self._withdrawn = Date(WITHDRAWN, withdrawn)
        self._rejected = Date(REJECTED, rejected)
        self._self_published = Date(SELF_PUBLISHED, self_published)
        self._published = Date(PUBLISHED, published)

        if not any(d.date for d in self._all_dates()):
            raise ValueError("At least one date must be set")

        if len([d.date for d in self._end_dates() if d.date]) > 1:
            raise ValueError("At most one end date can be set")

        if self._self_published.date and any(d.date for d in self._intermediate_dates()):
            raise ValueError("Intermediate dates cannot be used with self_published")

        if self._accepted.date and any(d.date for d in self._bad_end_dates()):
            raise ValueError("Bad end dates cannot be used with accepted")

        if self._published.date and not all(d.date for d in self._intermediate_dates()):
            raise ValueError("All intermediate dates must be set with published")

        if any(d.date for d in self._bad_end_dates()) and not self._submitted.date:
            raise ValueError("Bad end dates must set submitted")

        dates = [d.date for d in self._all_dates() if d.date]
        if dates != sorted(dates):
            raise ValueError("Dates must be in increasing order")

    @property
    def submitted(self) -> datetime.date | None:
        return self._submitted.date

    @property
    def accepted(self) -> datetime.date | None:
        return self._accepted.date

    @property
    def abandoned(self) -> datetime.date | None:
        return self._abandoned.date

    @property
    def withdrawn(self) -> datetime.date | None:
        return self._withdrawn.date

    @property
    def rejected(self) -> datetime.date | None:
        return self._rejected.date

    @property
    def self_published(self) -> datetime.date | None:
        return self._self_published.date

    @property
    def published(self) -> datetime.date | None:
        return self._published.date

    @property
    def dates(self) -> tuple[Date, ...]:
        return tuple(d for d in self._all_dates() if d.date)

    @property
    def latest(self) -> Date:
        return self.dates[-1]

    @property
    def active(self) -> bool:
        return not any(d.date for d in self._bad_end_dates())

    def _bad_end_dates(self) -> list[Date]:
        return [
            self._abandoned,
            self._withdrawn,
            self._rejected,
        ]

    def _good_end_dates(self) -> list[Date]:
        return [
            self._self_published,
            self._published,
        ]

    def _end_dates(self) -> list[Date]:
        return self._bad_end_dates() + self._good_end_dates()

    def _intermediate_dates(self) -> list[Date]:
        return [
            self._submitted,
            self._accepted,
        ]

    def _all_dates(self) -> list[Date]:
        return self._intermediate_dates() + self._end_dates()

    @staticmethod
    def from_json(j: Mapping[str, str]) -> "Dates":
        out = {}
        for k, v in j.items():
            if k not in _DATE_KEYS:
                raise ValueError(f"Unknown date key '{k}'")
            try:
                d = datetime.date.fromisoformat(v)
                out[k.replace("-", "_")] = d
            except ValueError as e:
                raise ValueError(
                    f"Value of key '{k}' must be a date in YYYY-MM-DD format; got '{v}'",
                ) from e
        return Dates(**out)


class Publication:
    def __init__(
        self,
        venue: str,
        dates: Dates,
        urls: Sequence[str],
        notes: str,
        paid: str,
    ) -> None:
        super().__init__()

        if not venue:
            raise ValueError("Venue must be non-empty")

        self._venue = venue
        self._dates = dates
        self._urls = tuple(urls)
        self._notes = notes
        self._paid = paid

    @property
    def venue(self) -> str:
        return self._venue

    @property
    def dates(self) -> Dates:
        return self._dates

    @property
    def urls(self) -> tuple[str, ...]:
        return self._urls

    @property
    def notes(self) -> str:
        return self._notes

    @property
    def paid(self) -> str:
        return self._paid

    @staticmethod
    def from_json(j: Mapping[str, Any]) -> "Publication":
        def assert_str(k: str, v: Any) -> None:  # noqa: ANN401
            if not isinstance(v, str):
                raise ValueError(f"Value of key '{k}' must be a string; got '{type(v)}'")

        unknown_keys = frozenset(j.keys()) - _KEYS
        if unknown_keys:
            raise ValueError(f"Found unknown keys '{unknown_keys}'")

        venue = ""
        date_strings = {}
        urls = []
        notes = ""
        paid = ""

        for k, v in j.items():
            if k in _DATE_KEYS:
                assert_str(k, v)
                date_strings[k] = v
            elif k == _VENUE:
                assert_str(k, v)
                venue = v
            elif k == _NOTES:
                assert_str(k, v)
                notes = v
            elif k == _PAID:
                assert_str(k, v)
                paid = v
            elif k == _URLS:
                if not isinstance(v, list):
                    raise ValueError(f"Value of key '{k}' must be a list; got '{type(v)}'")
                for url in v:
                    if not isinstance(url, str):
                        raise ValueError(f"URLs must be strings; got '{type(url)}'")
                    urls.append(url)

        dates = Dates.from_json(date_strings)

        return Publication(venue, dates, urls, notes, paid)


class Publications:
    def __init__(self, publications: Sequence[Publication]) -> None:
        super().__init__()
        if not publications:
            raise ValueError("No publications specified")
        self._publications = tuple(publications)

    @property
    def publications(self) -> tuple[Publication, ...]:
        return self._publications

    @property
    def active(self) -> bool:
        return any(p.dates.active for p in self._publications)

    @property
    def highest_active_state(self) -> str:
        states = []
        for p in self._publications:
            if p.dates.active:
                state = p.dates.latest
                states.append((_DATE_KEYS.index(state.state), state.state))
        states.sort()
        if states:
            return states[-1][1]
        return ""

    @staticmethod
    def from_json(j: Sequence[Mapping[str, Any]]) -> "Publications":
        return Publications([Publication.from_json(p) for p in j])
