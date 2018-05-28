import unittest
from app import app, db
from app.models import User, Fight


class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(name='test_1', password='cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_score(self):
        u = User(name='test_2', password='dog')
        db.session.add(u)
        db.session.commit()
        u.set_score(300)
        self.assertEqual(u.max_score, 300)
        u.set_score(1500)
        self.assertEqual(u.max_score, 1500)
        u.set_score(600)
        self.assertEqual(u.max_score, 1500)

    def test_fights(self):
        u1 = User(name='test_1', password='cat')
        u2 = User(name='test_2', password='dog')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.fights().all(), [])
        self.assertEqual(u2.fights("friendly").all(), [])

        f = Fight(user1=u1, user2=u2)
        db.session.add(f)
        db.session.commit()

        self.assertEqual(u1.fights().all(), [f])
        self.assertEqual(u2.fights("friendly").all(), [f])
        self.assertEqual(u1.new_fights().all(), [f])
        self.assertEqual(u2.new_fights().all(), [f])

        self.assertFalse(f.is_played(u1))
        f.set_score(u1, 1000)
        self.assertTrue(f.is_played(u1))
        self.assertEqual(u1.new_fights().all(), [])
        self.assertEqual(u2.new_fights().all(), [f])

        self.assertFalse(f.is_played(u2))
        f.set_score(u2, 2000)
        self.assertTrue(f.is_played(u2))
        self.assertEqual(u1.new_fights().all(), [])
        self.assertEqual(u2.new_fights().all(), [])

        self.assertEqual(f.get_winner(), u2)
        self.assertEqual(f.get_looser(), u1)

        self.assertEqual(f.get_users(), (u1, u2))
        self.assertEqual(f.get_scores(), (1000, 2000))


if __name__ == '__main__':
    unittest.main(verbosity=2)
