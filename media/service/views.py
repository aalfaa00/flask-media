from cmath import log
from flask import Blueprint, request, url_for
from flask.json import jsonify
from media.service.database import MediaService, db, MediaServiceSchema
from media.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
import urllib.request
from werkzeug.utils import secure_filename, send_from_directory
import os
import uuid
import json

media = Blueprint('media', __name__, url_prefix='/api/v1')

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
@media.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(directory=os.environ.get('UPLOAD_FOLDER'), path=filename, environ=request.environ)


@media.route('/files', methods=['POST', 'GET', 'PUT'])
def media_files():
    if request.method == 'POST':
        data = dict(request.form)
        # file = request.files['file_url']
        # filename = file.filename
        uid = str(uuid.uuid4())
        
        if 'file_url' not in request.files:
            resp = jsonify({'message' : 'No file part in the request'})
            resp.status_code = 400
            return resp
        
        files = request.files.getlist('file_url')
        success = False
        errors = []
        print(files)
        
        for i in range(len(files)):	
            print(files[i])	
            
            filename = files[i].filename
            
            file_name = f'{uid}-{filename}'
            
            url = url_for('media.get_file', filename=file_name)
            url_file = str(request.url_root) + str(url)
            
            files[i].save(os.path.join(os.environ.get('UPLOAD_FOLDER'), filename))
            
            service = MediaService(
                uid=uuid.uuid4(),
                file = files[i],
                file_url = url_file
            )
            
            service.save()
            
            serializer = MediaServiceSchema()
            data = serializer.dump(service)
            
            return jsonify({'message' : data}), HTTP_201_CREATED
        
        # else:
        #     errors[files[i].filename] = 'File type is not allowed'
            
        #     return jsonify(errors)

    
    elif request.method == 'GET':
        obj = get_search(request=request)
        
        return jsonify(obj)


    elif request.method == 'PUT':
        args = request.args
        file_url = str(args.get("url"))
        file_url = file_url.replace('"', '')
        
        obj = MediaService.objects.get(file_url=file_url)
        
        if media is None:
            return {'error': 'Page Not found'}, HTTP_404_NOT_FOUND
        
        obj.assigned = request.json['assigned']
        print(request.json['assigned'])
        service = obj.save()
        
        serializer = MediaServiceSchema()
        data = serializer.dump(service)
        
        return jsonify(data)        
            
            
def get_search(request):
    args = request.args
    uid = str(args.get("id"))
    print(uid)
    
    if uid is None or uid == 'None':
        objects = MediaService.objects.all()
        
        # serializer = MediaServiceSchema()
        # data = serializer.dumps(objects)
        json_data = []
        
        for obj in objects:
            json_data.append({
                'assigned': obj.assigned,
                'created_at': str(obj.created_at),
                'file_url': obj.file_url,
                'uid': str(obj.uid),
            })
        return json_data
    
    else:
        media = MediaService.objects.get(uid=uid)
        serializer = MediaServiceSchema()
        data = serializer.dump(media)
        
        return data
    
   

@media.route('files/<uuid:uid>', methods=['GET', 'DELETE'])
def delete(uid):
    if request.method == 'DELETE':
        print('DELETE')
        obj = MediaService.objects.get(uid=uid)
    
        if obj is None:
            return {'error': 'Page Not found'}, HTTP_404_NOT_FOUND
        
        obj.delete()
        return {'status': 'Sucess'}
    elif request.method == 'GET':
        return jsonify({'key': "success"})
    
    
    
    