import unittest
from app.models import User,Blog,Comment,Role
from app import db

class UserModelTest(unittest.TestCase):

    def setUp(self):
        self.new_user = User(password = 'books')

    def test_password_setter(self):
        self.assertTrue(self.new_user.password_hash is not None)

    def test_no_access_password(self):
        with self.assertRaises(AttributeError):
            self.new_user.password

    def test_password_verification(self):
        self.assertTrue(self.new_user.verify_password('books'))

class CommentTest(unittest.TestCase):
    def setUp(self):
        self.user_James = User(id=1,username = 'Aomware',password = 'fiddlediddle', email = 'aomware@gmail.com',bio="Change is the only constant")
        self.new_comment = Comment(id=5,Comment='Commnt for blogs',posted="2019-02-17",user = self.user_Aomware )

    def tearDown(self):
        Comment.query.delete()
        User.query.delete()

    def test_check_instance_variables(self):
        self.assertEquals(self.new_comment.id,5)
        self.assertEquals(self.new_comment.comment,'Comment for blogs')
        self.assertEquals(self.new_comment.posted,"2018-09-5")
        self.assertEquals(self.new_comment.user,self.user_James)

    def test_save_comment(self):
        self.new_comment.save_comment()
        self.assertTrue(len(Comment.query.all())>0)

    def test_get_comment_by_id(self):
        self.new_comment.save_comment()
        got_comment = Comment.get_comment(12345)
        self.assertTrue(len(got_comment) == 1)
