from app import app
from app.controllers import *

#rutas con controladores 

###FIX SOCKET###
app.add_url_rule('/api/iniciar_fix/new', view_func=FixSocketController.init_socket, methods=['POST'] )

####BOTS####
app.add_url_rule('/api/get_bots/<string:user_id>/<string:fix>', view_func=BotsController.show_all )
app.add_url_rule('/api/startBot', view_func=BotsController.start_bot_new, methods=['POST'] )
app.add_url_rule('/api/detenerBot', view_func=BotsController.detener_bot, methods=['POST'] )
app.add_url_rule('/api/add_bot', view_func=BotsController.add_bot, methods=['POST'] )
app.add_url_rule('/api/editBot', view_func=BotsController.edit_bot, methods=['POST'] )
app.add_url_rule('/api/deleteBot/<string:id>', view_func=BotsController.deleteBot, methods=['DELETE'] )
app.add_url_rule('/api/bot_data_charts/<string:id>', view_func=BotsController.bot_data_charts, methods=['POST'] )
app.add_url_rule('/api/cancel_order_manual', view_func=BotsController.cancel_order_manual, methods=['POST'] )
