import backend
from prettytable import PrettyTable
from flask import Blueprint, jsonify, request, render_template

skills = Blueprint('skills', __name__)

@skills.route('/', methods=['GET'])
def get_skills():
    
    min_rating = request.args.get('min_rating')
    min_freq = request.args.get('min_frequency')

    if min_rating is None:
        min_rating = 0

    if min_freq is None:
        min_freq = 0

    min_rating = int(min_rating)
    min_freq = int(min_freq)

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
    
    skills_to_pop = []
    for skill, count in skill_count.items():
        if count < min_freq:
            skills_to_pop.append(skill)

    for skill in skills_to_pop:
        del skill_count[skill]
        del skill_rating[skill]

    items = []
    for name, rating in skill_rating.items():
        skill_rating[name] = rating / skill_count[name]
        skill_rating[name] = round(skill_rating[name], 1)
        items.append({'name' : name, 'count' : skill_count[name], 
                  'rating' : skill_rating[name]})

    return render_template('skills.html', items=items)
