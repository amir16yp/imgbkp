# imgbkp
A self hosted Imgur-like web application designed for a single user to share images and videos.<br/>
IMGBKP is a self-hosted web application that allows a single user to securely host their images and videos. While uploading is restricted to those with the password, anyone can view the images and videos once they are uploaded.

Features
--------

*   **Image and Video Hosting:** You can easily upload and host your images and videos on your own server.
*   **Basic Authentication:** To ensure security, the application uses basic HTTP authentication. Only users with the correct username and password can upload files.
*   **File Metadata:** IMGBKP records metadata about each uploaded file, including the file's name, MIME type, size, and upload timestamp.
*   **Public Access:** Anyone can view the images and videos you've uploaded without needing authentication.

Installation
------------

To simplify the installation process, we provide an installation script. Follow these steps to set up IMGBKP:

1.  Clone the repository to your server:

            git clone https://github.com/amir16yp/imgbkp.git
            cd imgbkp
        

3.  Install the required python libraries

            pip install -r requirements.txt
        

5.  Make the installation script executable:

            chmod +x install.sh
        

7.  Run the installation script:

            ./install.sh
        

9.  Follow the prompts to provide the required information, such as username, password, host, and port.
10.  The script will generate a systemd service file, copy it to the systemd directory, enable the service, and optionally start the service.

Command-Line Arguments
----------------------

You can configure the IMGBKP application using the following command-line arguments when starting the app:

*   `--username`: Specifies the username for basic authentication (default: \`admin\`).
*   `--password`: Specifies the password for basic authentication (default: \`admin\`).
*   `--host`: Specifies the host IP address (default: \`0.0.0.0\`).
*   `--port`: Specifies the port for the Flask application (default: \`8833\`).

Example usage:

        python imgbkp.py --username your\_username --password your\_password --host your\_host --port your\_port
    

Usage
-----

1.  **Uploading Files:**

\- Access the admin panel by navigating to the \`/bkp/\` URL of the IMGBKP app.  
\- Log in using the provided username and password.  
\- You can upload images and videos using two methods:

*   **Local Upload:** Choose a file from your device.
*   **URL Upload:** Provide the URL of an image or video hosted elsewhere on the internet.

\- Uploaded files are saved on your server and can be accessed later.

5.  **Viewing Files:**

\- Anyone can view the uploaded images and videos by visiting the IMGBKP app's main page.  
\- Uploaded files are listed along with their metadata, and download links are provided.  
\- Please note that only those you shared a file's link with can view it.

Configuration
-------------

You can change the username, password, host, and port by using the command-line arguments as mentioned above.

License
-------

This project is open-source and available under the Unlicense License.
