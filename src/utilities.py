
import easyocr
import os
import cv2
import base64
import pypdfium2 as pdfium
from io import BytesIO


class SupportFun():
    def __init__ (self, ):
        self.ocr_reader = easyocr.Reader(['en']) 
        

    def save_file (self, file_data, file_name, st):
        """ Save Uploaded file in temp location """
        if not os.path.exists('./temp'):
            os.mkdir('./temp')

        if '.pdf' in file_name:
            pdf_stream = BytesIO(file_data)

            save_file_path = os.path.join('./temp', file_name)

            with open(save_file_path, 'wb') as f:
                f.write(pdf_stream.getbuffer())

            success = st.success(f"PDF file saved to : {save_file_path}") 

        if '.png' in file_name or 'jpeg' in file_name:
            img_stream = BytesIO(file_data)

            save_file_path = os.path.join('./temp', file_name)

            with open(save_file_path, 'wb') as f:
                f.write(img_stream.getbuffer())

            success = st.success(f"Image file saved to : {save_file_path}") 

    def create_image(self, file_name):
        """create images from the document uploaded and save it in temp location"""

        if '.pdf' in file_name:
            pdf = pdfium.PdfDocument(os.path.join('temp', file_name))
            images = dict()
            ocr_data = dict()

            for i in range(len(pdf)):
                page = pdf[i]
                image = page.render(scale=4).to_pil()
                pdf_root_name = file_name.split('.')[0]
                img_name = f"{pdf_root_name}_output_{i:03d}.jpg"
                # newsize = (200, 200)
                # image = image.resize(newsize)

                image.save(os.path.join("temp", img_name))

                with open(os.path.join("temp", img_name), "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read())
                    base64_encoded = encoded_string.decode()

                images[img_name] = base64_encoded
                ocr_data[img_name] = self.run_ocr(img_path=os.path.join("temp", img_name))

        if '.png' in file_name or 'jpeg' in file_name:
            images = dict()
            ocr_data = dict()
            with open(os.path.join("temp", file_name), "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read())
                    base64_encoded = encoded_string.decode()

            images[file_name] = base64_encoded
            ocr_data[file_name] = self.run_ocr(img_path=os.path.join("temp", file_name))


        clean_ocr_data = self.clean_ocr_data(ocr_data_dict=ocr_data)
        return images, ocr_data, clean_ocr_data
    
    def clean_ocr_data(self, ocr_data_dict):
        final_data = list()

        for key,value in ocr_data_dict.items():
            for sentesne in value:
                final_data.append(sentesne[1])
    
        return final_data
    
    def run_ocr(self, img_path):
        """Run OCR engine through the images after preprocessing"""
        try:
   
            img = cv2.imread(img_path, 0)
            blur = cv2.GaussianBlur(img,(5,5),0)
            result = self.ocr_reader.readtext(blur)

        except Exception as e:
            print("Error while Processing OCR : ",e)
            return None
        
        else:
            return result