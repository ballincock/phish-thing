import os
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import current_app

class GalleryService:
    @staticmethod
    def save_image(file, user_id):
        if not file or file.filename == '':
            return None

        filename = secure_filename(file.filename)

        timestamp = int(datetime.now().timestamp())
        unique_name = f"user_{user_id}_{timestamp}_{filename}"

        upload_folder = os.path.join(current_app.static_folder, 'uploads', 'gallery')

        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder, exist_ok=True)

        full_save_path = os.path.join(upload_folder, unique_name)
        file.save(full_save_path)

        return f"uploads/gallery/{unique_name}"

    @staticmethod
    def delete_image(image_path):
        if not image_path:
            return False

        full_path = os.path.join(current_app.static_folder, image_path)

        if os.path.exists(full_path):
            try:
                os.remove(full_path)
                return True
            except OSError:
                return False
        return False
