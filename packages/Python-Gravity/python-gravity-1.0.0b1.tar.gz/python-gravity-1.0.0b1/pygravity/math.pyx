gravitational_constant = 6.67430e-11

def acceleration_due_to_gravity(double mass, double distance):
    return (gravitational_constant * mass) / distance ** 2

__all__ = ['gravitational_constant', 'acceleration_due_to_gravity']