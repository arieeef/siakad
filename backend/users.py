
from flask import Blueprint, render_template,url_for,redirect,jsonify, request, flash
from backend.auth import login_required
from backend.db import db, get_all_collection
from werkzeug.security import generate_password_hash

usersapp = Blueprint('usersapp', __name__)

# read all
@usersapp.route('/users')
@login_required
def users():
    users = get_all_collection('users')
    return render_template('users/users.html', users=users)


# create
@usersapp.route('/users/tambah', methods=['POST','GET'])
@login_required
def tambah_users():
    # cek kesamaan password
    if request.method == 'POST':
        if request.form['password'] != request.form['password_1']:
            flash('password tidak sama','danger')
            return redirect(url_for('.tambah_users'))

        #  memanggil database
        cek_username = db.collection('users').where('username','==', request.form['username']).stream()
        username = {}
        # perulangan database
        for p in cek_username:
            user=p.to_dict()
            username = user
        # pengecekan username
        if username:
            flash('username sudah ada','danger')
            return redirect(url_for('.tambah_users'))

        data = {
            'nama_lengkap': request.form['nama_lengkap'],
            'username': request.form['username'],
            'email': request.form['email'],
        }

        data['password'] = generate_password_hash(request.form['password'], 'sha256')
        db.collection('users').document().set(data)
        flash('berhasil menambahkan Users', 'success')
        return redirect(url_for('usersapp.users'))


    return render_template('users/tambah_users.html')


# update
@usersapp.route('/users/edit/<uid>', methods=["POST","GET"])
@login_required
def edit_users(uid):
    if request.method == 'POST':
        user = {
            'nama_lengkap' : request.form['nama_lengkap'],
            'email' : request.form['email'],
        }
        db.collection('users').document(uid).update(user)
        flash('data sudah terupdate','success')
        return redirect(url_for('usersapp.users'))

    data = db.collection('users').document(uid).get().to_dict()

    return render_template('users/edit_users.html', data=data)


# delate
@usersapp.route('/users/hapus/<uid>')
@login_required
def hapus_users(uid):
    db.collection('users').document(uid).delete()
    flash('data berhasil di hapus','danger')
    return redirect(url_for('usersapp.users'))
    


# lihat data spesifik
@usersapp.route('/users/spesifik/<uid>')
@login_required
def spesifik_users(uid):
    data = db.collection('users').document(uid).get().to_dict()
    return render_template('users/spesifik_users.html', data = data)