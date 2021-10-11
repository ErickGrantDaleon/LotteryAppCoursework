# IMPORTS
import logging

from flask import Blueprint, render_template, request, flash
from app import db
from models import Draw, User

# CONFIG
lottery_blueprint = Blueprint('lottery', __name__, template_folder='templates')

# Temporary code to test user key.
# TODO: Probably update this code when dealing with multiple users.
user = User.query.filter_by(id=1).first()
drawkey = user.draw_key


# VIEWS
# view lottery page
@lottery_blueprint.route('/lottery')
def lottery():
    return render_template('lottery.html')


@lottery_blueprint.route('/add_draw', methods=['POST'])
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
    new_draw = Draw(user_id=1, draw=submitted_draw, win=False, round=0,
                    draw_key=drawkey)  # TODO: update user_id [user_id=1 is a placeholder]

    # add the new draw to the database
    db.session.add(new_draw)
    db.session.commit()

    # re-render lottery.page
    flash('Draw %s submitted.' % submitted_draw)

    return lottery()


# view all draws that have not been played
@lottery_blueprint.route('/view_draws', methods=['POST'])
def view_draws():
    # get all draws that have not been played [played=0]
    playable_draws = Draw.query.filter_by(played=False).all()  # TODO: filter playable draws for current user

    # if playable draws exist
    if len(playable_draws) != 0:
        # re-render lottery page with playable draws
        for d in playable_draws:
            d.view_draw(drawkey)

        return render_template('lottery.html', playable_draws=playable_draws)
    else:
        flash('No playable draws.')
        return lottery()


# view lottery results
@lottery_blueprint.route('/check_draws', methods=['POST'])
def check_draws():
    # get played draws
    played_draws = Draw.query.filter_by(played=True).all()  # TODO: filter played draws for current user

    # if played draws exist
    if len(played_draws) != 0:
        for d in played_draws:
            d.view_draw(drawkey)
        return render_template('lottery.html', results=played_draws, played=True)

    # if no played draws exist [all draw entries have been played therefore wait for next lottery round]
    else:
        flash("Next round of lottery yet to play. Check you have playable draws.")
        return lottery()


# delete all played draws
@lottery_blueprint.route('/play_again', methods=['POST'])
def play_again():
    delete_played = Draw.__table__.delete().where(Draw.played)  # TODO: delete played draws for current user only
    db.session.execute(delete_played)
    db.session.commit()

    flash("All played draws deleted.")
    return lottery()
