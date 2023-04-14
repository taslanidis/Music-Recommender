from app import app
from src.main_page import PageCreator
from src.callbacks import CallbackManager

# Define the app layout
app.layout = PageCreator.get_main_layout()

CallbackManager.attach_callbacks_to_app(app)


if __name__ == '__main__':
    app.run_server(debug=True)
