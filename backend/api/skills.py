import backend
from flask import Blueprint, jsonify, request

skills = Blueprint('skills', __name__)

@skills.route('/', methods=['GET'])
def get_skills():
    
    min_rating = request.args.get('min_rating')
    min_freq = request.args.get('min_frequency')

    if min_rating is None:
        min_rating = 0

    if min_freq is None:
        min_freq = 0

    skills = backend.query_db('select * from skills')
    skill_count = {}
    skill_rating = {}
    for skill in skills:
        if skill['rating'] >= min_rating:
            if skill_count.get(skill['name']) is None:
                skill_count[skill['name']] = 1
                skill_rating[skill['name']] = skill['rating']
            else:
                skill_count[skill['name']] += 1
                skill_rating[skill['name']] += skill['rating']
    
    for skill, count in skill_count.iteritems():
        if count < min_freq:
            del skill_count[skill]
            del skill_rating[skill]

    for name, rating in skill_rating.items():
        skill_rating[name] = rating / skill_count[name]
        skill_rating[name] = round(skill_rating[name], 1)

    return '%s' % skill_rating
