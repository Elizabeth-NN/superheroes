from flask import Flask, request, jsonify, make_response
from config import db
from models import Hero, Power, HeroPower

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///superheroes.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    # Route a: GET /heroes
    @app.route('/heroes', methods=['GET'])
    def get_heroes():
        heroes = Hero.query.all()
        heroes_data = [{
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name
        } for hero in heroes]
        return jsonify(heroes_data)
    
    # Route b: GET /heroes/:id
    @app.route('/heroes/<int:id>', methods=['GET'])
    def get_hero(id):
        hero = Hero.query.get(id)
        if not hero:
            return make_response(jsonify({'error': 'Hero not found'}), 404)
        
        hero_powers_data = []
        for hp in hero.hero_powers:
            hero_powers_data.append({
                'id': hp.id,
                'hero_id': hp.hero_id,
                'power_id': hp.power_id,
                'strength': hp.strength,
                'power': {
                    'id': hp.power.id,
                    'name': hp.power.name,
                    'description': hp.power.description
                }
            })
        
        return jsonify({
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name,
            'hero_powers': hero_powers_data
        })
    
    # Route c: GET /powers
    @app.route('/powers', methods=['GET'])
    def get_powers():
        powers = Power.query.all()
        powers_data = [{
            'id': power.id,
            'name': power.name,
            'description': power.description
        } for power in powers]
        return jsonify(powers_data)
    
    # Route d: GET /powers/:id
    @app.route('/powers/<int:id>', methods=['GET'])
    def get_power(id):
        power = Power.query.get(id)
        if not power:
            return make_response(jsonify({'error': 'Power not found'}), 404)
        return jsonify({
            'id': power.id,
            'name': power.name,
            'description': power.description
        })
    
    # Route e: PATCH /powers/:id
    @app.route('/powers/<int:id>', methods=['PATCH'])
    def update_power(id):
        power = Power.query.get(id)
        if not power:
            return make_response(jsonify({'error': 'Power not found'}), 404)
        
        data = request.get_json()
        if 'description' not in data:
            return make_response(jsonify({'errors': ['description is required']}), 400)
        
        try:
            power.description = data['description']
            db.session.commit()
            return jsonify({
                'id': power.id,
                'name': power.name,
                'description': power.description
            })
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'errors': [str(e)]}), 400)
    
    # Route f: POST /hero_powers
    @app.route('/hero_powers', methods=['POST'])
    def create_hero_power():
        data = request.get_json()
        required_fields = ['strength', 'power_id', 'hero_id']
        
        if not all(field in data for field in required_fields):
            return make_response(jsonify({'errors': ['strength, power_id, and hero_id are required']}), 400)
        
        try:
            hero_power = HeroPower(
                strength=data['strength'],
                power_id=data['power_id'],
                hero_id=data['hero_id']
            )
            db.session.add(hero_power)
            db.session.commit()
            
            hero = Hero.query.get(data['hero_id'])
            power = Power.query.get(data['power_id'])
            
            return jsonify({
                'id': hero_power.id,
                'hero_id': hero_power.hero_id,
                'power_id': hero_power.power_id,
                'strength': hero_power.strength,
                'hero': {
                    'id': hero.id,
                    'name': hero.name,
                    'super_name': hero.super_name
                },
                'power': {
                    'id': power.id,
                    'name': power.name,
                    'description': power.description
                }
            })
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'errors': [str(e)]}), 400)
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run()