import unittest
from datetime import date
from markdown_makefile.utils.publications import Date, Dates, Publication, Publications


class TestDate(unittest.TestCase):
    def test_date(self) -> None:
        self.assertEqual(Date("foo", date(2023, 5, 16)).date_str(), "2023-05-16")
        self.assertEqual(Date("foo", None).date_str(), "")


class TestDates(unittest.TestCase):
    def test_good_submitted(self) -> None:
        d = Dates(submitted=date(2023, 5, 16))
        self.assertEqual(d.submitted, date(2023, 5, 16))
        self.assertIsNone(d.accepted)
        self.assertIsNone(d.rejected)
        self.assertIsNone(d.withdrawn)
        self.assertIsNone(d.abandoned)
        self.assertIsNone(d.self_published)
        self.assertIsNone(d.published)
        self.assertEqual(d.dates, (("submitted", date(2023, 5, 16)),))
        self.assertEqual(d.latest, ("submitted", date(2023, 5, 16)))
        self.assertTrue(d.active)

    def test_good_accepted(self) -> None:
        d = Dates(submitted=date(2023, 5, 16), accepted=date(2023, 5, 17))
        self.assertEqual(d.submitted, date(2023, 5, 16))
        self.assertEqual(d.accepted, date(2023, 5, 17))
        self.assertIsNone(d.rejected)
        self.assertIsNone(d.withdrawn)
        self.assertIsNone(d.abandoned)
        self.assertIsNone(d.self_published)
        self.assertIsNone(d.published)
        self.assertEqual(
            d.dates, (("submitted", date(2023, 5, 16)), ("accepted", date(2023, 5, 17)))
        )
        self.assertEqual(d.latest, ("accepted", date(2023, 5, 17)))
        self.assertTrue(d.active)

    def test_good_rejected(self) -> None:
        d = Dates(submitted=date(2023, 5, 16), rejected=date(2023, 5, 17))
        self.assertEqual(d.submitted, date(2023, 5, 16))
        self.assertIsNone(d.accepted)
        self.assertEqual(d.rejected, date(2023, 5, 17))
        self.assertIsNone(d.withdrawn)
        self.assertIsNone(d.abandoned)
        self.assertIsNone(d.self_published)
        self.assertIsNone(d.published)
        self.assertEqual(
            d.dates, (("submitted", date(2023, 5, 16)), ("rejected", date(2023, 5, 17)))
        )
        self.assertEqual(d.latest, ("rejected", date(2023, 5, 17)))
        self.assertFalse(d.active)

    def test_good_withdrawn(self) -> None:
        d = Dates(submitted=date(2023, 5, 16), withdrawn=date(2023, 5, 17))
        self.assertEqual(d.submitted, date(2023, 5, 16))
        self.assertIsNone(d.accepted)
        self.assertIsNone(d.rejected)
        self.assertEqual(d.withdrawn, date(2023, 5, 17))
        self.assertIsNone(d.abandoned)
        self.assertIsNone(d.self_published)
        self.assertIsNone(d.published)
        self.assertEqual(
            d.dates, (("submitted", date(2023, 5, 16)), ("withdrawn", date(2023, 5, 17)))
        )
        self.assertEqual(d.latest, ("withdrawn", date(2023, 5, 17)))
        self.assertFalse(d.active)

    def test_good_abandoned(self) -> None:
        d = Dates(submitted=date(2023, 5, 16), abandoned=date(2023, 5, 17))
        self.assertEqual(d.submitted, date(2023, 5, 16))
        self.assertIsNone(d.accepted)
        self.assertIsNone(d.rejected)
        self.assertIsNone(d.withdrawn)
        self.assertEqual(d.abandoned, date(2023, 5, 17))
        self.assertIsNone(d.self_published)
        self.assertIsNone(d.published)
        self.assertEqual(
            d.dates, (("submitted", date(2023, 5, 16)), ("abandoned", date(2023, 5, 17)))
        )
        self.assertEqual(d.latest, ("abandoned", date(2023, 5, 17)))
        self.assertFalse(d.active)

    def test_good_self_published(self) -> None:
        d = Dates(self_published=date(2023, 5, 16))
        self.assertIsNone(d.submitted)
        self.assertIsNone(d.accepted)
        self.assertIsNone(d.rejected)
        self.assertIsNone(d.withdrawn)
        self.assertIsNone(d.abandoned)
        self.assertEqual(d.self_published, date(2023, 5, 16))
        self.assertIsNone(d.published)
        self.assertEqual(d.dates, (("self-published", date(2023, 5, 16)),))
        self.assertEqual(d.latest, ("self-published", date(2023, 5, 16)))
        self.assertTrue(d.active)

    def test_good_published(self) -> None:
        d = Dates(
            submitted=date(2023, 5, 16), accepted=date(2023, 5, 17), published=date(2023, 5, 18)
        )
        self.assertEqual(d.submitted, date(2023, 5, 16))
        self.assertEqual(d.accepted, date(2023, 5, 17))
        self.assertIsNone(d.rejected)
        self.assertIsNone(d.withdrawn)
        self.assertIsNone(d.abandoned)
        self.assertIsNone(d.self_published)
        self.assertEqual(d.published, date(2023, 5, 18))
        self.assertEqual(
            d.dates,
            (
                ("submitted", date(2023, 5, 16)),
                ("accepted", date(2023, 5, 17)),
                ("published", date(2023, 5, 18)),
            ),
        )
        self.assertEqual(d.latest, ("published", date(2023, 5, 18)))
        self.assertTrue(d.active)

    def test_bad_none(self) -> None:
        with self.assertRaises(ValueError):
            Dates()

    def test_bad_too_many_end_dates(self) -> None:
        with self.assertRaises(ValueError):
            Dates(rejected=date(2023, 5, 16), published=date(2023, 5, 16))

    def test_bad_self_published_intermediate(self) -> None:
        with self.assertRaises(ValueError):
            Dates(submitted=date(2023, 5, 16), self_published=date(2023, 5, 17))

    def test_bad_accepted_bad_end_dates(self) -> None:
        with self.assertRaises(ValueError):
            Dates(rejected=date(2023, 5, 16), accepted=date(2023, 5, 16))

    def test_bad_published_missing_intermediate(self) -> None:
        with self.assertRaises(ValueError):
            Dates(submitted=date(2023, 5, 16), published=date(2023, 5, 16))

    def test_bad_bad_missing_submitted(self) -> None:
        with self.assertRaises(ValueError):
            Dates(rejected=date(2023, 5, 16))

    def test_bad_wrong_order(self) -> None:
        with self.assertRaises(ValueError):
            Dates(
                submitted=date(2023, 5, 16), accepted=date(2023, 5, 16), published=date(2023, 5, 15)
            )

    def test_from_json_good(self) -> None:
        d = Dates.from_json(
            {
                "submitted": "2023-05-16",
                "accepted": "2023-05-17",
                "published": "2023-05-18",
            }
        )
        self.assertEqual(d.submitted, date(2023, 5, 16))
        self.assertEqual(d.accepted, date(2023, 5, 17))
        self.assertIsNone(d.rejected)
        self.assertIsNone(d.withdrawn)
        self.assertIsNone(d.abandoned)
        self.assertIsNone(d.self_published)
        self.assertEqual(d.published, date(2023, 5, 18))
        self.assertEqual(
            d.dates,
            (
                ("submitted", date(2023, 5, 16)),
                ("accepted", date(2023, 5, 17)),
                ("published", date(2023, 5, 18)),
            ),
        )
        self.assertEqual(d.latest, ("published", date(2023, 5, 18)))
        self.assertTrue(d.active)

    def test_from_json_good_self_published(self) -> None:
        d = Dates.from_json(
            {
                "self-published": "2023-05-18",
            }
        )
        self.assertIsNone(d.submitted)
        self.assertIsNone(d.accepted)
        self.assertIsNone(d.rejected)
        self.assertIsNone(d.withdrawn)
        self.assertIsNone(d.abandoned)
        self.assertEqual(d.self_published, date(2023, 5, 18))
        self.assertIsNone(d.published)
        self.assertEqual(d.dates, (("self-published", date(2023, 5, 18)),))
        self.assertEqual(d.latest, ("self-published", date(2023, 5, 18)))
        self.assertTrue(d.active)

    def test_from_json_bad_unknown_key(self) -> None:
        with self.assertRaises(ValueError):
            Dates.from_json({"foo": "2023-05-16"})

    def test_from_json_bad_invalid_date(self) -> None:
        with self.assertRaises(ValueError):
            Dates.from_json(
                {
                    "submitted": "2023-05-16",
                    "accepted": "2023/05/16",
                    "published": "2023-05-18",
                }
            )


class TestPublication(unittest.TestCase):
    def test_good(self) -> None:
        p = Publication(
            "Book",
            Dates(
                submitted=date(2023, 5, 16), accepted=date(2023, 5, 17), published=date(2023, 5, 18)
            ),
            ["foo", "bar"],
            "baz",
            "quux",
        )
        self.assertEqual(p.venue, "Book")
        d = p.dates
        self.assertEqual(d.submitted, date(2023, 5, 16))
        self.assertEqual(d.accepted, date(2023, 5, 17))
        self.assertIsNone(d.rejected)
        self.assertIsNone(d.withdrawn)
        self.assertIsNone(d.abandoned)
        self.assertIsNone(d.self_published)
        self.assertEqual(d.published, date(2023, 5, 18))
        self.assertEqual(p.urls, ("foo", "bar"))
        self.assertEqual(p.notes, "baz")
        self.assertEqual(p.paid, "quux")

    def test_bad_no_venue(self) -> None:
        with self.assertRaises(ValueError):
            Publication(
                "",
                Dates(
                    submitted=date(2023, 5, 16),
                    accepted=date(2023, 5, 17),
                    published=date(2023, 5, 18),
                ),
                ["foo", "bar"],
                "baz",
                "quux",
            )

    def test_from_json_good(self) -> None:
        p = Publication.from_json(
            {
                "venue": "Book",
                "submitted": "2023-05-16",
                "accepted": "2023-05-17",
                "published": "2023-05-18",
                "urls": ["foo", "bar"],
                "notes": "baz",
                "paid": "quux",
            }
        )
        self.assertEqual(p.venue, "Book")
        d = p.dates
        self.assertEqual(d.submitted, date(2023, 5, 16))
        self.assertEqual(d.accepted, date(2023, 5, 17))
        self.assertIsNone(d.rejected)
        self.assertIsNone(d.withdrawn)
        self.assertIsNone(d.abandoned)
        self.assertIsNone(d.self_published)
        self.assertEqual(d.published, date(2023, 5, 18))
        self.assertEqual(p.urls, ("foo", "bar"))
        self.assertEqual(p.notes, "baz")
        self.assertEqual(p.paid, "quux")

    def test_from_json_good_minimal(self) -> None:
        p = Publication.from_json(
            {
                "venue": "Book",
                "submitted": "2023-05-16",
            }
        )
        self.assertEqual(p.venue, "Book")
        d = p.dates
        self.assertEqual(d.submitted, date(2023, 5, 16))
        self.assertIsNone(d.accepted)
        self.assertIsNone(d.rejected)
        self.assertIsNone(d.withdrawn)
        self.assertIsNone(d.abandoned)
        self.assertIsNone(d.self_published)
        self.assertIsNone(d.published)
        self.assertEqual(p.urls, ())
        self.assertEqual(p.notes, "")
        self.assertEqual(p.paid, "")

    def test_from_json_bad_unknown_key(self) -> None:
        with self.assertRaises(ValueError):
            Publication.from_json(
                {
                    "venue": "Book",
                    "submitted": "2023-05-16",
                    "accepted": "2023-05-17",
                    "published": "2023-05-18",
                    "urls": ["foo", "bar"],
                    "notes": "baz",
                    "paid": "quux",
                    "foo": "bar",
                }
            )

    def test_from_json_bad_date_type(self) -> None:
        with self.assertRaises(ValueError):
            Publication.from_json(
                {
                    "venue": "Book",
                    "submitted": 2,
                    "accepted": "2023-05-17",
                    "published": "2023-05-18",
                    "urls": ["foo", "bar"],
                    "notes": "baz",
                    "paid": "quux",
                }
            )

    def test_from_json_bad_venue_type(self) -> None:
        with self.assertRaises(ValueError):
            Publication.from_json(
                {
                    "venue": 2,
                    "submitted": "2023-05-16",
                    "accepted": "2023-05-17",
                    "published": "2023-05-18",
                    "urls": ["foo", "bar"],
                    "notes": "baz",
                    "paid": "quux",
                }
            )

    def test_from_json_bad_notes_type(self) -> None:
        with self.assertRaises(ValueError):
            Publication.from_json(
                {
                    "venue": "Book",
                    "submitted": "2023-05-16",
                    "accepted": "2023-05-17",
                    "published": "2023-05-18",
                    "urls": ["foo", "bar"],
                    "notes": 2,
                    "paid": "quux",
                }
            )

    def test_from_json_bad_paid_type(self) -> None:
        with self.assertRaises(ValueError):
            Publication.from_json(
                {
                    "venue": "Book",
                    "submitted": "2023-05-16",
                    "accepted": "2023-05-17",
                    "published": "2023-05-18",
                    "urls": ["foo", "bar"],
                    "notes": "baz",
                    "paid": 2,
                }
            )

    def test_from_json_bad_urls_type(self) -> None:
        with self.assertRaises(ValueError):
            Publication.from_json(
                {
                    "venue": "Book",
                    "submitted": "2023-05-16",
                    "accepted": "2023-05-17",
                    "published": "2023-05-18",
                    "urls": 2,
                    "notes": "baz",
                    "paid": "quux",
                }
            )

    def test_from_json_bad_url_type(self) -> None:
        with self.assertRaises(ValueError):
            Publication.from_json(
                {
                    "venue": "Book",
                    "submitted": "2023-05-16",
                    "accepted": "2023-05-17",
                    "published": "2023-05-18",
                    "urls": ["foo", 2],
                    "notes": "baz",
                    "paid": "quux",
                }
            )


class TestPublications(unittest.TestCase):
    def test_good_active(self) -> None:
        ps = Publications(
            [
                Publication(
                    "Book",
                    Dates(
                        submitted=date(2023, 5, 16),
                        accepted=date(2023, 5, 17),
                        published=date(2023, 5, 18),
                    ),
                    ["foo", "bar"],
                    "baz",
                    "quux",
                ),
                Publication(
                    "Book2",
                    Dates(
                        submitted=date(2023, 5, 19),
                        accepted=date(2023, 5, 20),
                    ),
                    ["foo2", "bar2"],
                    "baz2",
                    "quux2",
                ),
            ]
        )

        self.assertEqual(len(ps.publications), 2)
        self.assertTrue(ps.active)
        self.assertEquals(ps.highest_active_state, "published")

        p = ps.publications[0]
        self.assertEqual(p.venue, "Book")
        d = p.dates
        self.assertEqual(d.submitted, date(2023, 5, 16))
        self.assertEqual(d.accepted, date(2023, 5, 17))
        self.assertIsNone(d.rejected)
        self.assertIsNone(d.withdrawn)
        self.assertIsNone(d.abandoned)
        self.assertIsNone(d.self_published)
        self.assertEqual(d.published, date(2023, 5, 18))
        self.assertEqual(p.urls, ("foo", "bar"))
        self.assertEqual(p.notes, "baz")
        self.assertEqual(p.paid, "quux")

        p = ps.publications[1]
        self.assertEqual(p.venue, "Book2")
        d = p.dates
        self.assertEqual(d.submitted, date(2023, 5, 19))
        self.assertEqual(d.accepted, date(2023, 5, 20))
        self.assertIsNone(d.rejected)
        self.assertIsNone(d.withdrawn)
        self.assertIsNone(d.abandoned)
        self.assertIsNone(d.self_published)
        self.assertIsNone(d.published)
        self.assertEqual(p.urls, ("foo2", "bar2"))
        self.assertEqual(p.notes, "baz2")
        self.assertEqual(p.paid, "quux2")

    def test_good_inactive(self) -> None:
        ps = Publications(
            [
                Publication(
                    "Book",
                    Dates(
                        submitted=date(2023, 5, 16),
                        rejected=date(2023, 5, 17),
                    ),
                    ["foo", "bar"],
                    "baz",
                    "quux",
                ),
                Publication(
                    "Book2",
                    Dates(
                        submitted=date(2023, 5, 19),
                        withdrawn=date(2023, 5, 20),
                    ),
                    ["foo2", "bar2"],
                    "baz2",
                    "quux2",
                ),
            ]
        )

        self.assertEqual(len(ps.publications), 2)
        self.assertFalse(ps.active)
        self.assertEqual(ps.highest_active_state, "")

        p = ps.publications[0]
        self.assertEqual(p.venue, "Book")
        d = p.dates
        self.assertEqual(d.submitted, date(2023, 5, 16))
        self.assertIsNone(d.accepted)
        self.assertEqual(d.rejected, date(2023, 5, 17))
        self.assertIsNone(d.withdrawn)
        self.assertIsNone(d.abandoned)
        self.assertIsNone(d.self_published)
        self.assertIsNone(d.published)
        self.assertEqual(p.urls, ("foo", "bar"))
        self.assertEqual(p.notes, "baz")
        self.assertEqual(p.paid, "quux")

        p = ps.publications[1]
        self.assertEqual(p.venue, "Book2")
        d = p.dates
        self.assertEqual(d.submitted, date(2023, 5, 19))
        self.assertIsNone(d.accepted)
        self.assertIsNone(d.rejected)
        self.assertEqual(d.withdrawn, date(2023, 5, 20))
        self.assertIsNone(d.abandoned)
        self.assertIsNone(d.self_published)
        self.assertIsNone(d.published)
        self.assertEqual(p.urls, ("foo2", "bar2"))
        self.assertEqual(p.notes, "baz2")
        self.assertEqual(p.paid, "quux2")

    def test_bad(self) -> None:
        with self.assertRaises(ValueError):
            Publications([])

    def test_from_json_good(self) -> None:
        ps = Publications.from_json(
            [
                {
                    "venue": "Book",
                    "submitted": "2023-05-16",
                    "accepted": "2023-05-17",
                    "published": "2023-05-18",
                    "urls": ["foo", "bar"],
                    "notes": "baz",
                    "paid": "quux",
                },
                {
                    "venue": "Book2",
                    "submitted": "2023-05-19",
                    "accepted": "2023-05-20",
                    "published": "2023-05-21",
                    "urls": ["foo2", "bar2"],
                    "notes": "baz2",
                    "paid": "quux2",
                },
            ]
        )

        self.assertEqual(len(ps.publications), 2)

        p = ps.publications[0]
        self.assertEqual(p.venue, "Book")
        d = p.dates
        self.assertEqual(d.submitted, date(2023, 5, 16))
        self.assertEqual(d.accepted, date(2023, 5, 17))
        self.assertIsNone(d.rejected)
        self.assertIsNone(d.withdrawn)
        self.assertIsNone(d.abandoned)
        self.assertIsNone(d.self_published)
        self.assertEqual(d.published, date(2023, 5, 18))
        self.assertEqual(p.urls, ("foo", "bar"))
        self.assertEqual(p.notes, "baz")
        self.assertEqual(p.paid, "quux")

        p = ps.publications[1]
        self.assertEqual(p.venue, "Book2")
        d = p.dates
        self.assertEqual(d.submitted, date(2023, 5, 19))
        self.assertEqual(d.accepted, date(2023, 5, 20))
        self.assertIsNone(d.rejected)
        self.assertIsNone(d.withdrawn)
        self.assertIsNone(d.abandoned)
        self.assertIsNone(d.self_published)
        self.assertEqual(d.published, date(2023, 5, 21))
        self.assertEqual(p.urls, ("foo2", "bar2"))
        self.assertEqual(p.notes, "baz2")
        self.assertEqual(p.paid, "quux2")

    def test_from_json_bad(self) -> None:
        with self.assertRaises(ValueError):
            Publications.from_json([])


if __name__ == "__main__":
    unittest.main()
