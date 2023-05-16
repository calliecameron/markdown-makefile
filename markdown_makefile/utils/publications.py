from typing import Any, Dict, List, Optional, Tuple
import datetime

_VENUE = "venue"
_PAID = "paid"
_NOTES = "notes"
_SUBMITTED = "submitted"
_ACCEPTED = "accepted"
_REJECTED = "rejected"
_WITHDRAWN = "withdrawn"
_ABANDONED = "abandoned"
_SELF_PUBLISHED = "self-published"

_PUBLISHED = "published"
_URLS = "urls"

_DATE_KEYS = frozenset(
    [
        _SUBMITTED,
        _ACCEPTED,
        _REJECTED,
        _WITHDRAWN,
        _ABANDONED,
        _SELF_PUBLISHED,
        _PUBLISHED,
    ]
)

_KEYS = _DATE_KEYS | frozenset([_VENUE, _PAID, _NOTES, _URLS])


class Dates:
    def __init__(
        self,
        submitted: Optional[datetime.date] = None,
        accepted: Optional[datetime.date] = None,
        rejected: Optional[datetime.date] = None,
        withdrawn: Optional[datetime.date] = None,
        abandoned: Optional[datetime.date] = None,
        self_published: Optional[datetime.date] = None,
        published: Optional[datetime.date] = None,
    ) -> None:
        super().__init__()

        self._submitted = submitted
        self._accepted = accepted
        self._rejected = rejected
        self._withdrawn = withdrawn
        self._abandoned = abandoned
        self._self_published = self_published
        self._published = published

        if not any(self._all_dates()):
            raise ValueError("At least one date must be set")

        if len([d for d in self._end_dates() if d]) > 1:
            raise ValueError("At most one end date can be set")

        if self._self_published and any(self._intermediate_dates()):
            raise ValueError("Intermediate dates cannot be used with self_published")

        if self._accepted and any(self._bad_end_dates()):
            raise ValueError("Bad end dates cannot be used with accepted")

        if self._published and not all(self._intermediate_dates()):
            raise ValueError("All intermediate dates must be set with published")

        if any(self._bad_end_dates()) and not self._submitted:
            raise ValueError("Bad end dates must set submitted")

        dates = [d for d in self._all_dates() if d]
        if dates != sorted(dates):
            raise ValueError("Dates must be in increasing order")

    @property
    def submitted(self) -> Optional[datetime.date]:
        return self._submitted

    @property
    def accepted(self) -> Optional[datetime.date]:
        return self._accepted

    @property
    def rejected(self) -> Optional[datetime.date]:
        return self._rejected

    @property
    def withdrawn(self) -> Optional[datetime.date]:
        return self._withdrawn

    @property
    def abandoned(self) -> Optional[datetime.date]:
        return self._abandoned

    @property
    def self_published(self) -> Optional[datetime.date]:
        return self._self_published

    @property
    def published(self) -> Optional[datetime.date]:
        return self._published

    def _bad_end_dates(self) -> List[Optional[datetime.date]]:
        return [
            self._rejected,
            self._withdrawn,
            self._abandoned,
        ]

    def _good_end_dates(self) -> List[Optional[datetime.date]]:
        return [
            self._self_published,
            self._published,
        ]

    def _end_dates(self) -> List[Optional[datetime.date]]:
        return self._bad_end_dates() + self._good_end_dates()

    def _intermediate_dates(self) -> List[Optional[datetime.date]]:
        return [
            self._submitted,
            self._accepted,
        ]

    def _all_dates(self) -> List[Optional[datetime.date]]:
        return self._intermediate_dates() + self._end_dates()

    @staticmethod
    def from_json(j: Dict[str, str]) -> "Dates":
        out = {}
        for k, v in j.items():
            if k not in _DATE_KEYS:
                raise ValueError("Unknown date key '%s'" % k)
            try:
                d = datetime.date.fromisoformat(v)
                out[k.replace("-", "_")] = d
            except ValueError as e:
                raise ValueError(
                    "Value of key '%s' must be a date in YYYY-MM-DD format; got '%s'" % (k, v)
                ) from e
        return Dates(**out)


class Publication:
    def __init__(self, venue: str, dates: Dates, urls: List[str], notes: str, paid: str) -> None:
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
    def urls(self) -> Tuple[str, ...]:
        return self._urls

    @property
    def notes(self) -> str:
        return self._notes

    @property
    def paid(self) -> str:
        return self._paid

    @staticmethod
    def from_json(j: Dict[str, Any]) -> "Publication":
        def assert_str(k: str, v: Any) -> None:
            if not isinstance(v, str):
                raise ValueError("Value of key '%s' must be a string; got '%s'" % (k, str(type(v))))

        unknown_keys = frozenset(j.keys()) - _KEYS
        if unknown_keys:
            raise ValueError("Found unknown keys '%s'" % unknown_keys)

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
                    raise ValueError(
                        "Value of key '%s' must be a list; got '%s'" % (k, str(type(v)))
                    )
                for url in v:
                    if not isinstance(url, str):
                        raise ValueError("URLs must be strings; got '%s'" % str(type(url)))
                    urls.append(url)

        dates = Dates.from_json(date_strings)

        return Publication(venue, dates, urls, notes, paid)


class Publications:
    def __init__(self, publications: List[Publication]) -> None:
        super().__init__()
        if not publications:
            raise ValueError("No publications specified")
        self._publications = tuple(publications)

    @property
    def publications(self) -> Tuple[Publication, ...]:
        return self._publications

    @staticmethod
    def from_json(j: List[Dict[str, Any]]) -> "Publications":
        return Publications([Publication.from_json(p) for p in j])
