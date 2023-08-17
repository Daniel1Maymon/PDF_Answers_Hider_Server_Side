from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import os

# app = Flask(__name__)



def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS
    
    # Allow requests from your frontend's domain
    CORS(app, resources={r"/*": {"origins": "http://localhost:3002"}})

    @app.route("/")
    def homePage():
        return "Hello"
    
    @app.route("/getPdf", methods=["POST"])
    def getPdf():
        try:
            pdf_file = request.files["pdfFile"]
            if pdf_file:
                
                upload_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # '/root/Environments'
                file_name = pdf_file.filename
                file_dest_path = os.path.join(upload_directory, file_name)
                
                pdf_file.save(dst=file_dest_path)
                
                print("pdfFile = ")
                print(pdf_file)
                
                if os.path.isfile(file_dest_path):
                    return send_file(file_dest_path)        
            
                data = {"message": "Success!"}
                return jsonify(data)
            else:
                return jsonify({"message": "No file uploaded"}), 400
        except Exception as e:
            return jsonify({"error" : str(e)}), 500   
    

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(port=3001)