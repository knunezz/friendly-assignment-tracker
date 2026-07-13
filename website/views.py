from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Assignment
from . import db
from datetime import datetime

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():

    assignments = Assignment.query.filter_by(
        user_id=current_user.id,
        completed=False
    ).order_by(
        Assignment.due_date
    ).all()

    return render_template(
        "home.html",
        user=current_user,
        assignments=assignments
    )


@views.route('/add-assignment', methods=['GET', 'POST'])
@login_required
def add_assignment():

    if request.method == 'POST':

        course = request.form.get('course')
        title = request.form.get('title')
        due_date_str = request.form.get('due_date')
        due_date = datetime.strptime(
            due_date_str,
            '%Y-%m-%d'
        ).date()
        assignment = Assignment(
            course=course,
            title=title,
            due_date=due_date,
            user_id=current_user.id
        )

        db.session.add(assignment)
        db.session.commit()

        flash(
            'Assignment added!',
            category='success'
        )

        return redirect(url_for('views.home'))

    return render_template(
        'add_assignment.html',
        user=current_user
    )

@views.route('/delete-assignment/<int:id>')
@login_required
def delete_assignment(id):

    assignment = Assignment.query.get(id)

    if assignment and assignment.user_id == current_user.id:
        db.session.delete(assignment)
        db.session.commit()

    return redirect(url_for('views.home'))


@views.route('/edit-assignment/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_assignment(id):

    assignment = Assignment.query.get_or_404(id)

    if assignment.user_id != current_user.id:
        flash('Unauthorized.', category='error')
        return redirect(url_for('views.home'))

    if request.method == 'POST':

        assignment.course = request.form.get('course')
        assignment.title = request.form.get('title')

        due_date_str = request.form.get('due_date')
        assignment.due_date = datetime.strptime(
            due_date_str,
            '%Y-%m-%d'
        ).date()

        db.session.commit()

        flash('Assignment updated!', category='success')

        return redirect(url_for('views.home'))

    return render_template(
        'edit_assignment.html',
        assignment=assignment,
        user=current_user
    )

@views.route('/completed')
@login_required
def completed():
    assignments = Assignment.query.filter_by(
        user_id = current_user.id,
        completed=True
    ).order_by(
        Assignment.due_date
    ).all()

    return render_template(
        'completed.html',
        assignments=assignments,
        user=current_user
    )
    
@views.route('/complete-assignment/<int:id>')
@login_required
def complete_assignment(id):

    assignment = Assignment.query.get_or_404(id)

    if assignment.user_id == current_user.id:
        assignment.completed = True
        db.session.commit()

    return redirect(url_for('views.home'))  
@views.route('/calendar')
@login_required
def calendar():

    assignments = Assignment.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        'calendar.html',
        assignments=assignments,
        user=current_user
    )  