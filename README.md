# Music Flow Therapy

Music Flow Therapy is web application that uses Spotify Web API to create playlist for the mood chosen by the user. It uses Flask framework and python.

## Installation
Steps:

1. Clone this repository to a folder in your local computer.

2. Create virtual environment for python version 11 or above at the folder where the code exists.
   
Note: Virtual environments helps us to manage dependencies well. We can install the libraries we need our project in a virtual environment without affecting other projects or libraries in our computer. For more information see https://docs.python.org/3/library/venv.html

3. In the config.py file, set the client id, client secret of your Spotify developer account. 

Note: For protection of your account, avoid checking the config.py with the credentials to GitHub repository. You can add the file to .gitignore.


4. Install the dependencies using the following command within your virtual enviroment.

 ```bash
   pip install -r requirements.txt
 ```

## Running the application locally

1. Ton run the application locally, set the client side variables as shown below:

 ```python
   CLIENT_SIDE_URL = "http://127.0.0.1"
   CLIENT_PORT = 5000
 ```

2. Run the application by executing the following command from within the virtual environment:

 ```python
   python app.py
 ```
Alternatively, you can run it as a Flask app using

 ```python
   flask --app soundflowtherapy --debug run
 ```

"--debug" flag is optional. You use it when you want to run the app locally to test.

## How to use the website?

To see how the website works, go to https://www.musicflowtherapy.com/

The website has good information on how music helps. The "Music Recommender" page provides an option to the user to choose a mood and create a Spotify Playlist.

1. Choose a mode - Normal, or Random
2. Choose a mood - Happy, Sad, Angry, or Relaxed. (Random mode chooses a mood automatically).
3. Create a Playlist. 


## Help me!
1. This is my High School Project. 
Please fill out the survey forms linked at the website https://www.musicflowtherapy.com



## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)