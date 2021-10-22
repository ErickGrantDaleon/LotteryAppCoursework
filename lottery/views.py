"""User functions for playing the lottery game"""
# IMPORTS
import logging
import copy
from flask import Blueprint, render_template, request, flash
from app import db
from models import Draw, User
from flask_login import login_required, current_user

# CONFIG
lottery_blueprint = Blueprint('lottery', __name__, template_folder='templates')


# VIEWS
# view lottery page
@lottery_blueprint.route('/lottery')
@login_required
def lottery():
    return render_template('lottery.html')


@lottery_blueprint.route('/add_draw', methods=['POST'])
@login_required
def add_draw():
    submitted_draw = ''
    for i in range(6):
        strip_number = request.form.get('no' + str(i + 1))
        if strip_number != '':
            if not 1 <= int(strip_number) <= 60:
                flash('Slots must be between 1 and 60')
                return lottery()
            submitted_draw += strip_number + ' '
        else:
            flash('Must fill all slots.')
            return lottery()

    submitted_draw.strip()

    # create a new draw with the form data.
    new_draw = Draw(user_id=current_user.id, draw=submitted_draw, win=False, round=0, draw_key=current_user.draw_key)

    # add the new draw to the database
    db.session.add(new_draw)
    try:
        db.session.commit()
        flash('Draw %s submitted.' % submitted_draw)
    except:
        flash('Draw submission failed.')
        db.session.rollback()
    finally:
        db.session.close()

    # re-render lottery.page
    return lottery()


# view all draws that have not been played
@lottery_blueprint.route('/view_draws', methods=['POST'])
@login_required
def view_draws():
    # get all draws that have not been played [played=0]
    playable_draws = Draw.query.filter_by(played=False).all()
    draw_copies = list(map(lambda x: copy.deepcopy(x), playable_draws))
    decrypted_draws = []

    # if playable draws exist
    if len(draw_copies) != 0:
        # re-render lottery page with playable draws
        for d in draw_copies:
            user = User.query.filter_by(id=d.user_id).first()
            if not (user is None):
                d.view_draw(user.draw_key)
                decrypted_draws.append(d)

        return render_template('lottery.html', playable_draws=decrypted_draws)
    else:
        flash('No playable draws.')
        return lottery()


# view lottery results
@lottery_blueprint.route('/check_draws', methods=['POST'])
@login_required
def check_draws():
    # get played draws
    played_draws = Draw.query.filter_by(played=True).all()
    draw_copies = list(map(lambda x: copy.deepcopy(x), played_draws))
    decrypted_draws = []

    # if played draws exist
    if len(draw_copies) != 0:
        for d in draw_copies:
            user = User.query.filter_by(id=d.user_id).first()
            if not (user is None):
                d.view_draw(user.draw_key)
                decrypted_draws.append(d)
        return render_template('lottery.html', results=decrypted_draws,
                               played=True)

    # if no played draws exist [all draw entries have been played therefore wait for next lottery round]
    else:
        flash("Next round of lottery yet to play. Check you have playable draws.")
        return lottery()


# delete all played draws
@lottery_blueprint.route('/play_again', methods=['POST'])
@login_required
def play_again():
    delete_played = Draw.__table__.delete().where(Draw.played, Draw.user_id == current_user.id)
    db.session.execute(delete_played)
    db.session.commit()

    flash("All played draws deleted.")
    return lottery()
