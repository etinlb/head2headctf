from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    score = db.Column(db.Integer)
    current_flag = db.Column(db.String(80))
    next_score = db.Column(db.Integer)
    avatar_id = db.Column(db.Integer)

    def __init__(self, username, avatar_id):
        self.username = username
        self.avatar_id = avatar_id
        self.score = 0
        self.current_flag = ""
        self.next_score = 0

    def __repr__(self):
        return '<User %r>' % self.username

    @staticmethod
    def get_user(username):
        return User.query.filter_by(username=username).first()

    def set_user_score(self, score):
        self.score = score

    def add_score(self, score):
        self.score += score

    def add_user_next_score(self, next_score):
        self.score += next_score


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Integer, nullable=False)
    user_id_1 = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_id_2 = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestarted = db.Column(db.Integer)
    score = db.Column(db.Integer)
    winner = db.Column(db.Integer)

    def __init__(self, user_id_1, user_id_2, active=0):
        self.user_id_1 = user_id_1
        self.user_id_2 = user_id_2
        self.active = active

    # @staticmethod
    # def create_and_start_match(db_session, user_id_1, user_id_2):
    #     mat
