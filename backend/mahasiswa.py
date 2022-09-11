
from flask import Blueprint, render_template,jsonify,redirect,url_for,flash,request
from backend.auth import login_required
from backend.db import db, get_all_collection, storage

mahasiswa = Blueprint('mahasiswa', __name__)

@mahasiswa.route('/mahasiswa')
@login_required
def daftar_mahasiswa():
    daftar_mahasiswa = get_all_collection('mahasiswa')
    return render_template('mahasiswa.html', mahasiswa=daftar_mahasiswa)

@mahasiswa.route('/mahasiswa/tambah', methods=['POST','GET'])
def tambah_mahasiswa():
    if request.method == 'POST':
        data = {
            'nama_lengkap' : request.form['nama_lengkap'],
            'jurusan' : request.form['jurusan'],
            'email' : request.form['email'],
            'umur' : request.form['umur'],
            'fakusltas': request.form['fakultas'],
            'status' : 'lulus'
        }
        if 'image' in request.files and request.files['image']:
            image = request.files['image']
            ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
            filename = image.filename
            lokasi = f"profil/{filename}"
            ext = filename.rsplit('.', 1)[1].lower()
            if ext in ALLOWED_EXTENSIONS:
                storage.child(lokasi).put(image)
                data['photoURL'] = storage.child(lokasi).get_url(None)
            else:
                flash("Foto tidak diperbolehkan", "danger")
                return redirect(url_for('.tambah_mahasiswa'))
        db.collection('mahasiswa').document().set(data)
        return redirect(url_for('mahasiswa.daftar_mahasiswa'))
    return render_template('tambah_mahasiswa.html')


# update
@mahasiswa.route('/mahasiswa/edit/<uid>', methods=['POST','GET'])
@login_required
def edit_mahasiswa(uid):
    if request.method == 'POST':
        mhs = {
            'nama_lengkap' : request.form['nama_lengkap'],
            'jurusan' : request.form['jurusan'],
            'email' : request.form['email'],
            'umur' : request.form['umur'],
            'fakultas' : request.form['fakultas'],
        }
        db.collection('mahasiswa').document(uid).update(mhs)
        flash('data sudah terupdate','success')
        return redirect(url_for('.daftar_mahasiswa'))
    
    data = db.collection('mahasiswa').document(uid).get().to_dict()

    return render_template('edit_mahasiswa.html', data=data)



    


