from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Assignment
from . import db
from datetime import datetime

#Bluepring allows me to organize all assignment-related routes into one file instead of putting everything in app.py
views = Blueprint('views', __name__)
# Returns an assignment only if it belongs to the logged-in user.
# This prevents users from editing or deleting someone else's data.
def get_user_assignment(id):
    return Assignment.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first()


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    # Show only assignments that are not completed yet.
    assignments = Assignment.query.filter_by(
        user_id=current_user.id,
        completed=False
    ).order_by(
        Assignment.due_date
    ).all()
    #opens up home.html and variables become availble in jinja
    return render_template(
        "home.html",
        user=current_user,
        assignments=assignments
    )


@views.route('/add-assignment', methods=['GET', 'POST'])
@login_required
def add_assignment():
    # If the user submits the form, create a new assignment.
    if request.method == 'POST':

        course = request.form.get('course')
        title = request.form.get('title')
        due_date_str = request.form.get('due_date')
        notes = request.form.get('notes')
        category = request.form.get('category')
        # Convert the HTML date into a Python date object.
        due_date = datetime.strptime(due_date_str,'%Y-%m-%d').date()

        assignment = Assignment(
            course=course,
            title=title,
            due_date=due_date,
            category=category,
            notes=notes,
            user_id=current_user.id)

        # db.session.add tells the sqlalchemy that I wanna save this object.
        db.session.add(assignment)
        #this saves the changes to the database
        db.session.commit()

        #redirect sends users to another page, aka back to assignments page
        return redirect(url_for('views.home'))

    return render_template('add_assignment.html',user=current_user)

@views.route('/delete-assignment/<int:id>')
@login_required
def delete_assignment(id):
    assignment = get_user_assignment(id)

    if assignment:
        db.session.delete(assignment)
        db.session.commit()
                    
    return redirect(url_for('views.home'))


@views.route('/edit-assignment/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_assignment(id):

    assignment = get_user_assignment(id)

    if not assignment:
        flash('Assignment not found.', category='error')
        return redirect(url_for('views.home'))
    

    if request.method == 'POST':

        # Update assignment information with new values.
        # request form gets information submitted through a form
        assignment.course = request.form.get('course')
        assignment.title = request.form.get('title')
        
        due_date_str = request.form.get('due_date')
        assignment.notes = request.form.get('notes')
        assignment.category = request.form.get('category')
        assignment.due_date = datetime.strptime(due_date_str,'%Y-%m-%d').date()

        db.session.commit()
        from_page = request.form.get('from_page')
        #need this to refrence the currenct page we are on
        if from_page == 'completed':
            return redirect(url_for('views.completed'))

        return redirect(url_for('views.home'))
    
    from_page = request.args.get('from_page')   

    return render_template('edit_assignment.html', assignment=assignment, user=current_user, from_page=from_page)


@views.route('/completed')
@login_required
def completed():

    # Display assignments that have been marked complete.
    assignments = Assignment.query.filter_by(
        user_id=current_user.id,
        completed=True).order_by(Assignment.due_date).all()
    


    return render_template(
        'completed.html',
        assignments=assignments,
        user=current_user
    )
    
@views.route('/complete-assignment/<int:id>')
@login_required
def complete_assignment(id):

    assignment = get_user_assignment(id)

    if assignment:
        assignment.completed = True
        db.session.commit()



    return redirect(url_for('views.home'))

@views.route('/uncomplete-assignment/<int:id>')
@login_required
def uncomplete_assignment(id):

    assignment = get_user_assignment(id)
    # Make sure users can only edit their own assignments
    if assignment:
        assignment.completed = False
        db.session.commit()

    return redirect(url_for('views.completed'))
        


@views.route('/calendar')
@login_required
def calendar():

    # Get all assignments for the calendar view.
    assignments = Assignment.query.filter_by(user_id=current_user.id).all()

    colors = {
        "Exam": "#F79090",
        "Quiz": "#C59BF8",
        "Classwork": "#E5C975",
        "Homework": "#F59E6B"
    }
    return render_template(
        'calendar.html',
        assignments=assignments,
        colors=colors,
        user=current_user)