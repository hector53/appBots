from flask import  jsonify, request, abort, make_response
from app.clases.mainFix import MainFix
from app import fixM
class FixSocketController:
    @staticmethod
    async def init_socket():
        print("iniciar socket")
        req_obj = request.get_json()
        print("req iniciar fix", req_obj)
        mainFixC = MainFix(req_obj["user"], req_obj["account"], req_obj["accountFixId"], req_obj["puertows"])
        await fixM.add_task(mainFixC)
        return jsonify({"status": True})
