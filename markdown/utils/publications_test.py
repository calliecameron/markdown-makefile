import unittest
from datetime import date

from markdown.utils.publications import Publication, Publications, State


class TestPublication(unittest.TestCase):
    def test_good_minimal(self) -> None:
        p = Publication(
            venue="foo",
            submitted="2023-05-16",  # type: ignore[arg-type]
        )
        self.assertEqual(p.venue, "foo")
        self.assertEqual(p.urls, [])
        self.assertEqual(p.notes, "")
        self.assertEqual(p.paid, "")
        self.assertEqual(p.submitted, date(2023, 5, 16))
        self.assertIsNone(p.accepted)
        self.assertIsNone(p.rejected)
        self.assertIsNone(p.withdrawn)
        self.assertIsNone(p.abandoned)
        self.assertIsNone(p.self_published)
        self.assertIsNone(p.published)
        self.assertEqual(p.dates, ((State.SUBMITTED, date(2023, 5, 16)),))
        self.assertEqual(p.latest, (State.SUBMITTED, date(2023, 5, 16)))
        self.assertTrue(p.active)

    def test_good_submitted(self) -> None:
        p = Publication(
            venue="foo",
            urls=["foo", "bar"],
            notes="baz",
            paid="quux",
            submitted=date(2023, 5, 16),
        )
        self.assertEqual(p.venue, "foo")
        self.assertEqual(p.urls, ["foo", "bar"])
        self.assertEqual(p.notes, "baz")
        self.assertEqual(p.paid, "quux")
        self.assertEqual(p.submitted, date(2023, 5, 16))
        self.assertIsNone(p.accepted)
        self.assertIsNone(p.rejected)
        self.assertIsNone(p.withdrawn)
        self.assertIsNone(p.abandoned)
        self.assertIsNone(p.self_published)
        self.assertIsNone(p.published)
        self.assertEqual(p.dates, ((State.SUBMITTED, date(2023, 5, 16)),))
        self.assertEqual(p.latest, (State.SUBMITTED, date(2023, 5, 16)))
        self.assertTrue(p.active)

    def test_good_accepted(self) -> None:
        p = Publication(
            venue="foo",
            urls=["foo", "bar"],
            notes="baz",
            paid="quux",
            submitted=date(2023, 5, 16),
            accepted=date(2023, 5, 17),
        )
        self.assertEqual(p.venue, "foo")
        self.assertEqual(p.urls, ["foo", "bar"])
        self.assertEqual(p.notes, "baz")
        self.assertEqual(p.paid, "quux")
        self.assertEqual(p.submitted, date(2023, 5, 16))
        self.assertEqual(p.accepted, date(2023, 5, 17))
        self.assertIsNone(p.rejected)
        self.assertIsNone(p.withdrawn)
        self.assertIsNone(p.abandoned)
        self.assertIsNone(p.self_published)
        self.assertIsNone(p.published)
        self.assertEqual(
            p.dates,
            ((State.SUBMITTED, date(2023, 5, 16)), (State.ACCEPTED, date(2023, 5, 17))),
        )
        self.assertEqual(p.latest, (State.ACCEPTED, date(2023, 5, 17)))
        self.assertTrue(p.active)

    def test_good_rejected(self) -> None:
        p = Publication(
            venue="foo",
            urls=["foo", "bar"],
            notes="baz",
            paid="quux",
            submitted=date(2023, 5, 16),
            rejected=date(2023, 5, 17),
        )
        self.assertEqual(p.venue, "foo")
        self.assertEqual(p.urls, ["foo", "bar"])
        self.assertEqual(p.notes, "baz")
        self.assertEqual(p.paid, "quux")
        self.assertEqual(p.submitted, date(2023, 5, 16))
        self.assertIsNone(p.accepted)
        self.assertEqual(p.rejected, date(2023, 5, 17))
        self.assertIsNone(p.withdrawn)
        self.assertIsNone(p.abandoned)
        self.assertIsNone(p.self_published)
        self.assertIsNone(p.published)
        self.assertEqual(
            p.dates,
            ((State.SUBMITTED, date(2023, 5, 16)), (State.REJECTED, date(2023, 5, 17))),
        )
        self.assertEqual(p.latest, (State.REJECTED, date(2023, 5, 17)))
        self.assertFalse(p.active)

    def test_good_withdrawn(self) -> None:
        p = Publication(
            venue="foo",
            urls=["foo", "bar"],
            notes="baz",
            paid="quux",
            submitted=date(2023, 5, 16),
            withdrawn=date(2023, 5, 17),
        )
        self.assertEqual(p.venue, "foo")
        self.assertEqual(p.urls, ["foo", "bar"])
        self.assertEqual(p.notes, "baz")
        self.assertEqual(p.paid, "quux")
        self.assertEqual(p.submitted, date(2023, 5, 16))
        self.assertIsNone(p.accepted)
        self.assertIsNone(p.rejected)
        self.assertEqual(p.withdrawn, date(2023, 5, 17))
        self.assertIsNone(p.abandoned)
        self.assertIsNone(p.self_published)
        self.assertIsNone(p.published)
        self.assertEqual(
            p.dates,
            ((State.SUBMITTED, date(2023, 5, 16)), (State.WITHDRAWN, date(2023, 5, 17))),
        )
        self.assertEqual(p.latest, (State.WITHDRAWN, date(2023, 5, 17)))
        self.assertFalse(p.active)

    def test_good_abandoned(self) -> None:
        p = Publication(
            venue="foo",
            urls=["foo", "bar"],
            notes="baz",
            paid="quux",
            submitted=date(2023, 5, 16),
            abandoned=date(2023, 5, 17),
        )
        self.assertEqual(p.venue, "foo")
        self.assertEqual(p.urls, ["foo", "bar"])
        self.assertEqual(p.notes, "baz")
        self.assertEqual(p.paid, "quux")
        self.assertEqual(p.submitted, date(2023, 5, 16))
        self.assertIsNone(p.accepted)
        self.assertIsNone(p.rejected)
        self.assertIsNone(p.withdrawn)
        self.assertEqual(p.abandoned, date(2023, 5, 17))
        self.assertIsNone(p.self_published)
        self.assertIsNone(p.published)
        self.assertEqual(
            p.dates,
            ((State.SUBMITTED, date(2023, 5, 16)), (State.ABANDONED, date(2023, 5, 17))),
        )
        self.assertEqual(p.latest, (State.ABANDONED, date(2023, 5, 17)))
        self.assertFalse(p.active)

    def test_good_self_published(self) -> None:
        p = Publication.model_validate(
            {
                "venue": "foo",
                "urls": ["foo", "bar"],
                "notes": "baz",
                "paid": "quux",
                "self-published": date(2023, 5, 16),
            },
        )
        self.assertEqual(p.venue, "foo")
        self.assertEqual(p.urls, ["foo", "bar"])
        self.assertEqual(p.notes, "baz")
        self.assertEqual(p.paid, "quux")
        self.assertIsNone(p.submitted)
        self.assertIsNone(p.accepted)
        self.assertIsNone(p.rejected)
        self.assertIsNone(p.withdrawn)
        self.assertIsNone(p.abandoned)
        self.assertEqual(p.self_published, date(2023, 5, 16))
        self.assertIsNone(p.published)
        self.assertEqual(p.dates, ((State.SELF_PUBLISHED, date(2023, 5, 16)),))
        self.assertEqual(p.latest, (State.SELF_PUBLISHED, date(2023, 5, 16)))
        self.assertTrue(p.active)

    def test_good_published(self) -> None:
        p = Publication(
            venue="foo",
            urls=["foo", "bar"],
            notes="baz",
            paid="quux",
            submitted=date(2023, 5, 16),
            accepted=date(2023, 5, 17),
            published=date(2023, 5, 18),
        )
        self.assertEqual(p.venue, "foo")
        self.assertEqual(p.urls, ["foo", "bar"])
        self.assertEqual(p.notes, "baz")
        self.assertEqual(p.paid, "quux")
        self.assertEqual(p.submitted, date(2023, 5, 16))
        self.assertEqual(p.accepted, date(2023, 5, 17))
        self.assertIsNone(p.rejected)
        self.assertIsNone(p.withdrawn)
        self.assertIsNone(p.abandoned)
        self.assertIsNone(p.self_published)
        self.assertEqual(p.published, date(2023, 5, 18))
        self.assertEqual(
            p.dates,
            (
                (State.SUBMITTED, date(2023, 5, 16)),
                (State.ACCEPTED, date(2023, 5, 17)),
                (State.PUBLISHED, date(2023, 5, 18)),
            ),
        )
        self.assertEqual(p.latest, (State.PUBLISHED, date(2023, 5, 18)))
        self.assertTrue(p.active)

    def test_bad_no_venue(self) -> None:
        with self.assertRaises(ValueError):
            Publication(
                urls=["foo", "bar"],
                notes="baz",
                paid="quux",
                submitted=date(2023, 5, 18),
            )  # type: ignore[call-arg]

    def test_bad_no_dates(self) -> None:
        with self.assertRaises(ValueError):
            Publication(
                venue="foo",
                urls=["foo", "bar"],
                notes="baz",
                paid="quux",
            )

    def test_bad_too_many_end_dates(self) -> None:
        with self.assertRaises(ValueError):
            Publication(
                venue="foo",
                urls=["foo", "bar"],
                notes="baz",
                paid="quux",
                rejected=date(2023, 5, 16),
                published=date(2023, 5, 16),
            )

    def test_bad_self_published_intermediate(self) -> None:
        with self.assertRaises(ValueError):
            Publication.model_validate(
                {
                    "venue": "foo",
                    "urls": ["foo", "bar"],
                    "notes": "baz",
                    "paid": "quux",
                    "submitted": date(2023, 5, 16),
                    "self-published": date(2023, 5, 17),
                },
            )

    def test_bad_accepted_bad_end_dates(self) -> None:
        with self.assertRaises(ValueError):
            Publication(
                venue="foo",
                urls=["foo", "bar"],
                notes="baz",
                paid="quux",
                rejected=date(2023, 5, 16),
                accepted=date(2023, 5, 16),
            )

    def test_bad_published_missing_intermediate(self) -> None:
        with self.assertRaises(ValueError):
            Publication(
                venue="foo",
                urls=["foo", "bar"],
                notes="baz",
                paid="quux",
                submitted=date(2023, 5, 16),
                published=date(2023, 5, 16),
            )

    def test_bad_bad_missing_submitted(self) -> None:
        with self.assertRaises(ValueError):
            Publication(
                venue="foo",
                urls=["foo", "bar"],
                notes="baz",
                paid="quux",
                rejected=date(2023, 5, 16),
            )

    def test_bad_wrong_order(self) -> None:
        with self.assertRaises(ValueError):
            Publication(
                venue="foo",
                urls=["foo", "bar"],
                notes="baz",
                paid="quux",
                submitted=date(2023, 5, 16),
                accepted=date(2023, 5, 16),
                published=date(2023, 5, 15),
            )


class TestPublications(unittest.TestCase):
    def test_good_active(self) -> None:
        ps = Publications(
            [
                Publication(
                    venue="Book",
                    submitted=date(2023, 5, 16),
                    accepted=date(2023, 5, 17),
                    published=date(2023, 5, 18),
                    urls=["foo", "bar"],
                    notes="baz",
                    paid="quux",
                ),
                Publication(
                    venue="Book2",
                    submitted=date(2023, 5, 19),
                    accepted=date(2023, 5, 20),
                    urls=["foo2", "bar2"],
                    notes="baz2",
                    paid="quux2",
                ),
            ],
        )

        self.assertTrue(ps)
        self.assertEqual(len(ps), 2)
        self.assertTrue(ps.active)
        self.assertEqual(ps.highest_active_state, State.PUBLISHED)

        p = ps[0]
        self.assertEqual(p.venue, "Book")
        self.assertEqual(p.submitted, date(2023, 5, 16))
        self.assertEqual(p.accepted, date(2023, 5, 17))
        self.assertIsNone(p.rejected)
        self.assertIsNone(p.withdrawn)
        self.assertIsNone(p.abandoned)
        self.assertIsNone(p.self_published)
        self.assertEqual(p.published, date(2023, 5, 18))
        self.assertEqual(p.urls, ["foo", "bar"])
        self.assertEqual(p.notes, "baz")
        self.assertEqual(p.paid, "quux")

        p = ps[1]
        self.assertEqual(p.venue, "Book2")
        self.assertEqual(p.submitted, date(2023, 5, 19))
        self.assertEqual(p.accepted, date(2023, 5, 20))
        self.assertIsNone(p.rejected)
        self.assertIsNone(p.withdrawn)
        self.assertIsNone(p.abandoned)
        self.assertIsNone(p.self_published)
        self.assertIsNone(p.published)
        self.assertEqual(p.urls, ["foo2", "bar2"])
        self.assertEqual(p.notes, "baz2")
        self.assertEqual(p.paid, "quux2")

    def test_good_inactive(self) -> None:
        ps = Publications(
            [
                Publication(
                    venue="Book",
                    submitted=date(2023, 5, 16),
                    rejected=date(2023, 5, 17),
                    urls=["foo", "bar"],
                    notes="baz",
                    paid="quux",
                ),
                Publication(
                    venue="Book2",
                    submitted=date(2023, 5, 19),
                    withdrawn=date(2023, 5, 20),
                    urls=["foo2", "bar2"],
                    notes="baz2",
                    paid="quux2",
                ),
            ],
        )

        self.assertTrue(ps)
        self.assertEqual(len(ps), 2)
        self.assertFalse(ps.active)
        self.assertEqual(ps.highest_active_state, None)

        p = ps[0]
        self.assertEqual(p.venue, "Book")
        self.assertEqual(p.submitted, date(2023, 5, 16))
        self.assertIsNone(p.accepted)
        self.assertEqual(p.rejected, date(2023, 5, 17))
        self.assertIsNone(p.withdrawn)
        self.assertIsNone(p.abandoned)
        self.assertIsNone(p.self_published)
        self.assertIsNone(p.published)
        self.assertEqual(p.urls, ["foo", "bar"])
        self.assertEqual(p.notes, "baz")
        self.assertEqual(p.paid, "quux")

        p = ps[1]
        self.assertEqual(p.venue, "Book2")
        self.assertEqual(p.submitted, date(2023, 5, 19))
        self.assertIsNone(p.accepted)
        self.assertIsNone(p.rejected)
        self.assertEqual(p.withdrawn, date(2023, 5, 20))
        self.assertIsNone(p.abandoned)
        self.assertIsNone(p.self_published)
        self.assertIsNone(p.published)
        self.assertEqual(p.urls, ["foo2", "bar2"])
        self.assertEqual(p.notes, "baz2")
        self.assertEqual(p.paid, "quux2")

    def test_bad(self) -> None:
        with self.assertRaises(ValueError):
            Publications([])

    def test_empty(self) -> None:
        ps = Publications.model_construct([])
        self.assertFalse(ps)
        self.assertEqual(len(ps), 0)
        self.assertFalse(ps.active)
        self.assertEqual(ps.highest_active_state, None)


if __name__ == "__main__":
    unittest.main()
