''' Weiland cohort controller '''
from werkzeug.exceptions import BadRequest

weiland = [
    {'id': 1, 'name': 'Raj', 'status': 'student'},
    {'id': 2, 'name': 'Tonderai', 'status': 'student'},
    {'id': 3, 'name': 'Tara', 'status': 'student'}
]


def index():
    return [p for p in weiland], 200


def show(req, id):
    return find_by_id(id), 200


def find_by_id(id):
    try:
        return next(p for p in weiland if p['id'] == id)
    except:
        raise BadRequest(f'We could not find the person with id: {id}')


def create(req):
    new_student = req.get_json()
    new_student['id'] = sorted([p['id'] for p in weiland])[-1] + 1
    weiland.append(new_student)
    return new_student, 201


def update(req, id):
    cohort = find_by_id(id)
    data = req.get_json()
    print(data)
    for key, val in data.items():
        cohort[key] = val
    return cohort, 200


def destroy(req, id):
    cohort = find_by_id(id)
    weiland.remove(cohort)
    return cohort, 204
