from datetime import datetime
import flask as f
from flask_sqlalchemy import SQLAlchemy
app = f.Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///note.sqlite3'
app.config['SECRET_KEY'] = 'Dhruv Solanki'
db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column('note_id', db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    label = db.Column(db.String(100), nullable=False)
    note_text = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, title, label, note_text):
        self.title = title
        self.label = label
        self.note_text = note_text
        self.pub_date = datetime.now()

@app.route("/")
def index():
    notes = Note.query.order_by(Note.id.desc()).all()
    labels = db.session.query(Note.label.distinct()).all()
    return f.render_template('home.html', notes = notes, labels = labels)

@app.route("/note/<int:noteID>")
def showNote(noteID):
    note = Note.query.filter_by(id=noteID).first()

    return f.render_template('show.html', note = note)

@app.route("/note/<int:noteID>/delete", methods = ['POST', 'GET'])
def deleteNote(noteID):
    if(f.request.method == 'POST'):
        note = Note.query.filter_by(id=noteID).first()

        db.session.delete(note)
        db.session.commit()

        return f.redirect(f.url_for('index'))

    return f.redirect(f.url_for('index'))

@app.route("/note/<int:noteID>/edit")
def editNote(noteID):
    note = Note.query.filter_by(id=noteID).first()

    return f.render_template('edit.html', note = note)

@app.route("/note/<int:noteID>/update", methods = ['POST', 'GET'])
def updateNote(noteID):
    if(f.request.method == 'POST'):
        note = Note.query.filter_by(id=noteID).first()

        note.title = f.request.form['title'].strip()
        note.label = f.request.form['label'].strip()
        note.note_text = f.request.form['note_text'].strip()
        note.pub_date = datetime.now()

        db.session.commit()

        return f.redirect(f.url_for('showNote', noteID = note.id))

    return f.redirect(f.url_for('index'))

@app.route("/newNote", methods = ['POST', 'GET'])
def newNote():
    if(f.request.method == 'POST'):
        title = f.request.form['title']
        label = f.request.form['label']
        note_text = f.request.form['note_text']
        note = Note(title.strip(), label.strip(), note_text.strip())

        db.session.add(note)
        db.session.commit()
    
        return f.redirect(f.url_for('index'))
        
    return f.render_template('newNote.html')

@app.route("/note/search", methods = ['GET', 'POST'])
def searchNote():
    query = f.request.args.get('query')
    notes = Note.query.filter(Note.title.like('%' + query + '%'))
    notes = notes.order_by(Note.title).all()

    return f.render_template('searchedNotes.html', notes = notes, query = query)

@app.route("/about")
def about():
    return f.render_template('about.html')

ip = '127.0.0.1'
port = 5000
if(__name__ == '__main__'):
    db.create_all()
    app.run(ip, port, debug=True) 