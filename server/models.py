from config import db, association_proxy
from sqlalchemy.orm import validates

class Hero(db.Model):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    super_name = db.Column(db.String(100), nullable=False)
    
    hero_powers = db.relationship('HeroPower', back_populates='hero', cascade='all, delete-orphan')
    powers = association_proxy('hero_powers', 'power',
        creator=lambda power_obj: HeroPower(power=power_obj, strength='Average'))

class Power(db.Model):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    
    hero_powers = db.relationship('HeroPower', back_populates='power', cascade='all, delete-orphan')

    @validates('description')
    def validate_description(self, key, description):
        if not description:
            raise ValueError("Description cannot be empty")
        if len(description) < 20:
            raise ValueError("Description must be at least 20 characters long")
        return description

class HeroPower(db.Model):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(50), nullable=False)
    
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id', ondelete='CASCADE'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id', ondelete='CASCADE'), nullable=False)
    
    hero = db.relationship('Hero', back_populates='hero_powers')
    power = db.relationship('Power', back_populates='hero_powers')

    @validates('strength')
    def validate_strength(self, key, strength):
        valid_strengths = ['Strong', 'Weak', 'Average']
        if strength not in valid_strengths:
            raise ValueError(f"Strength must be one of: {', '.join(valid_strengths)}")
        return strength