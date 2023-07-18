from flask import Flask, flash, request, redirect, render_template
from PIL import ExifTags
from PIL import Image as Image01
from exif import Image
import PIL


app = Flask(__name__)  

app.secret_key = "secret key"
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('About.html')


@app.route('/contact', methods=['GET','POST'])
def contact():
        return 'Message sent successfully'  


@app.route("/contacts")
def contacts():
    return render_template('Contacts.html')

@app.route("/feedback")
def feedback():
    return render_template('Feedback.html') 

@app.route("/Map.html")
def Map():
    latitude,longitude=image_coordinates()
    return render_template('Map.html',latitude=latitude,longitude=longitude)   

def image_coordinates():
         image = "image1.jpg"
         with open(image, 'rb') as src:
            img = Image(src)
    #checking if image has exif data or not
         if img.has_exif:
             try:
                img.gps_longitude
                coords = (decimal_coords(img.gps_latitude,
                                        img.gps_latitude_ref),
                            decimal_coords(img.gps_longitude,
                                        img.gps_longitude_ref))
             except AttributeError:
                print('No Coordinates')
         else:
                print('The Image has no EXIF information')
                
         lati,longi=coords
         return(lati,longi)

def decimal_coords(coords, ref):
    decimal_degrees = coords[0] + \
                      coords[1] / 60 + \
                      coords[2] / 3600
    if ref == "S" or ref == "W":
        decimal_degrees = -decimal_degrees
    return decimal_degrees



@app.route("/features", methods=['GET', 'POST'])
def features():
          if request.method == 'POST':
             if 'image' not in request.files:
                return redirect('upload.html') 
             
             try:
                info_dict,exif_info = Data()
                return render_template('upload.html', info_dict=info_dict , exif_info=exif_info)
             except PIL.UnidentifiedImageError:
               flash('No image uploaded! Try Again.......')
               return redirect(request.url)
          return render_template('upload.html',error='Please upload image...') 


def Data():
        image = request.files['image']
        img = Image01.open(image) 
        exif_data = img._getexif()
    

        info_dict = {
            "Filename": image.filename,
            "Image Size": img.size,
            "Image Height": img.height,
            "Image Width": img.width,
            "Image Format": img.format,
            "Image Mode": img.mode,
            "Image Palette": img.palette,
            "Image is Animated": getattr(img, "is_animated", False),
            "Frames in Image": getattr(img, "n_frames", 1)
        }
        for label,value in info_dict.items():
            print(f"{label:25}: {value}")
        exif_info = {}
        if exif_data is not None:
            for tag, value in exif_data.items():
                if tag in ExifTags.TAGS:
                    exif_info[ExifTags.TAGS[tag]] = value
                    exif_data1 =img.getexif()
                    img.save("image1.jpg", format="JPEG", exif=exif_data1)
                    print(ExifTags.TAGS[tag])
        return(info_dict,exif_info) 



if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True)

