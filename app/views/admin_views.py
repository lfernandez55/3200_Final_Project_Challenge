from flask import Blueprint, redirect, render_template, flash
from flask import request, url_for, current_app
from flask_user import current_user, login_required, roles_required
import copy

from app import db
from app.models.user_models import User, Role, Course, UsersRoles
from app.forms.admin_forms import UserCustomForm

admin_blueprint = Blueprint('admin', __name__, template_folder='templates')

@admin_blueprint.route('/admin')
@roles_required('admin')  # Limits access to users with the 'admin' role
def admin_page():
    return render_template('admin/admin_page.html')

@admin_blueprint.route('/admin/list_users', methods=['GET', 'POST'] )
@roles_required('admin')  # Limits access to users with the 'admin' role
def admin_list_users():
    if request.method == 'GET':
        # users = User.query.all()
        users = User.query.order_by(User.email.asc())
    else:
        search_term = request.form["search_term"]
        search_term = "%{}%".format(search_term)
        users = User.query.filter(User.email.like(search_term)).all()
    
    return render_template('admin/admin_list_users.html', users=users)  

@admin_blueprint.route('/admin/create_user', methods=['GET', 'POST'] )
@roles_required('admin')  # Limits access to users with the 'admin' role
def admin_create_user():
    error_msg = ""
    user = User()
    roles = Role.query.all()

    if request.method == 'POST':
        # email validation
        other_user = User.query.filter(User.email == request.form['email'] ).first()
        if (other_user is not None) and (other_user.id != user.id):
            user.role_ids = request.form.getlist('roles') # keeps appropriate roles selected
            error_msg = "This email is already being used by another user"
            flash('Email already being used by another user!!', 'error')
        else:
            
            user.first_name  = request.form['first_name']
            user.last_name = request.form['last_name']
            user.email = request.form['email'] 
            user.password=current_app.user_manager.password_manager.hash_password(request.form['password'])
            user.role_ids = request.form.getlist('roles')
            user.active = 1
            for role_id in request.form.getlist('roles'):
                roleObj = Role.query.filter(Role.id == role_id).first()
                user.roles.append(roleObj)
            db.session.add(user)
            db.session.commit()
            flash('User Created!!', 'success')
            return redirect(url_for('admin.admin_list_users'))
    return render_template('admin/admin_create_edit_user.html', user=user, roles=roles, error_msg=error_msg, verb="Create")



@admin_blueprint.route('/admin/edit_user/<user_id>', methods=['GET', 'POST'] )
@roles_required('admin')  # Limits access to users with the 'admin' role
def admin_edit_user(user_id):
    error_msg=""
    user = User.query.filter(User.id == user_id).first()
    roles = Role.query.all()

    # using user.roles creates complications. so we make a new attribute instead. this
    # is used in the form to select what roles are associated with the user
    user.role_ids = []
    for role in user.roles:
        user.role_ids.append(str(role.id))

    user.password = "stubstub" #we set this to a dummy value. its not updated unless it changes
    if request.method == 'GET':
        request.form.first_name = user.first_name
        request.form.last_name = user.last_name
        request.form.email = user.email
        request.form.password = user.password
    elif request.method == 'POST':
        # email validation
        other_user = User.query.filter(User.email == request.form['email'] ).first()
        if (other_user is not None) and (other_user.id != user.id):
            user.role_ids = request.form.getlist('roles') # keeps appropriate roles selected
            error_msg = "This email is already being used by another user"
            flash('Email already being used by another user!!', 'error')
        else:
            user.first_name  = request.form['first_name']
            user.last_name = request.form['last_name']
            user.email = request.form['email'] 
            if request.form['password'] != 'stubstub':
                user.password=current_app.user_manager.password_manager.hash_password(request.form['password'])
            user.role_ids = request.form.getlist('roles')
            user.active = 1
            user.roles = [] # needs to be reset otherwise u just append duplicates
            for role_id in request.form.getlist('roles'):
                roleObj = Role.query.filter(Role.id == role_id).first()
                user.roles.append(roleObj)
            db.session.add(user)
            db.session.commit()
            flash('User Created!!', 'success')
            return redirect(url_for('admin.admin_list_users'))
    return render_template('admin/admin_create_edit_user.html', user=user, roles=roles, error_msg=error_msg, verb="Edit")


@admin_blueprint.route('/admin/delete_user/<user_id>')
@roles_required('admin')  
def admin_delete_user(user_id):
    user = User.query.filter(User.id == user_id).first()
    db.session.delete(user)
    db.session.commit()
    flash('User Deleted!!', 'success')
    return redirect(url_for('admin.admin_list_users'))


@admin_blueprint.route('/admin/list_roles', methods=['GET', 'POST'] )
@roles_required('admin')  
def admin_list_roles():
    roles = Role.query.order_by(Role.name.asc())
    for role in roles:
        print(role.name)
    return render_template('admin/admin_list_roles.html', roles=roles) 




@admin_blueprint.route('/admin/create_role', methods=['GET', 'POST'])
@roles_required('admin')  
def admin_create_role():
    
    if request.method == 'POST':
        if len(request.form['role_name']) < 3:
            flash('Role name too short', 'error')
        else:
            role = Role()
            role.name  = request.form['role_name']
            db.session.add(role)
            db.session.commit()
            flash('Role Created!!', 'success')
            return redirect(url_for('admin.admin_list_roles'))
    return render_template('admin/admin_create_edit_role.html', verb="Create")


@admin_blueprint.route('/admin/edit_role/<role_id>', methods=['GET', 'POST'] )
@roles_required('admin')  
def admin_edit_role(role_id):
    role = Role.query.filter(Role.id == role_id).first()
    if request.method == 'GET':
        request.form.role_name = role.name
    elif request.method == 'POST':
        if len(request.form['role_name']) < 3:
            flash('Role name too short', 'error')
        else:
            role.name  = request.form['role_name']
            db.session.add(role)
            db.session.commit()
            flash('Role Updated!!', 'success')
            return redirect(url_for('admin.admin_list_roles'))
    return render_template('admin/admin_create_edit_role.html', verb="Edit")


@admin_blueprint.route('/admin/delete_role/<role_id>')
@roles_required('admin')  
def admin_delete_role(role_id):
    role = Role.query.filter(Role.id == role_id).first()
    db.session.delete(role)
    db.session.commit()
    flash('Role Deleted!!', 'success')
    return redirect(url_for('admin.admin_list_roles'))

####################################################################################
#############################Course Views###########################################




#############################End Course Views#######################################
####################################################################################

# the below views are for testing roles
# you must create teacher and student roles to test them
@admin_blueprint.route('/admin/teacher_or_admin')
@roles_required(['admin', 'teacher'])  # requires admin OR teacher role
def admin_teacher_or_admin():
    return "You have the right roles to access this page - it requires admin OR teacher roles"

@admin_blueprint.route('/admin/teacher_and_admin')
@roles_required('admin','teacher')  # requires admin AND teacher roles
def admin_teacher_and_admin():
    return "You have the right roles to access this view"

@admin_blueprint.route('/admin/student')
@roles_required('student')  
def admin_student():
    return "You have the right roles to access this page - requires student role"


