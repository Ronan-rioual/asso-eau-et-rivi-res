from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import pymongo


def get_db_connection():
    client = pymongo.MongoClient("mongodb+srv://Admin:yYytmhJ9gw2HMiX@cluster0.zmqoc.mongodb.net/don_asso?retryWrites=true&w=majority")
    return client


app = Flask(__name__)

app.config['SECRET_KEY'] = 'your secret key'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        adresse = request.form['adresse']
        mail = request.form['mail']
        montant = int(request.form['montant'])
        valider = request.form.get('valider')

        if not nom or not prenom or not adresse or not mail or not montant or not valider:
            flash('Toutes les informations sont requises!')
        else:
            donation = {
                "nom": nom,
                "prenom": prenom,
                "adresse": adresse,
                "mail": mail,
                "montant": montant
            }
            client = get_db_connection()
            db = client.don_asso
            db.don.insert_one(donation)
            client.close()
            return redirect(url_for('index'))
    return render_template('create.html')


def liste_don():
    client = get_db_connection()
    db = client.don_asso
    don = db.don.find()
    client.close()
    return don

def total_don():
    client = get_db_connection()
    db = client.don_asso
    total = list(db.don.aggregate([{'$group':{'_id':'null', 'total' : {'$sum' : '$montant'}}}]))
    total_don = total[0]['total']
    client.close()
    return total_don

@app.route('/affichage_don', methods=('GET', 'POST'))
def affichage_don():
    don = liste_don()
    total = total_don()
    return render_template('affichage_don.html', don=don, total=total)

'''


def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)


@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))

'''

if __name__ == '__main__':
    app.run(debug=True)

