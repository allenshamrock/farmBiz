from config import app,api
from models import User,Animal,Order,Transaction,Produce
from routes import Signup, Login, Logout, AnimalsRoutes, OrderRoutes, Transactions,Produces

api.add_resource(Signup,'/signup')
api.add_resource(Login,'/login')
api.add_resource(Logout,'/logout')
api.add_resource(Transactions,'/transactions')
api.add_resource(AnimalsRoutes, '/animals', '/animals/<string:id>')
api.add_resource(OrderRoutes, '/orders')
api.add_resource(Produces, '/produces', '/produces/<string:id>')

if __name__ == '__main__':
    app.run(port=5555,debug=True)