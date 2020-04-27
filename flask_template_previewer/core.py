###Make your imports
from .views import create_blueprint

#Main Extension Class
class FlaskTemplatePreviewer:
    """
    Doc string.
    """

    def __init__(
            self, app=None, blueprint_name="flask_template_previewer", 
            blueprint_url_prefix="/preview",
            before_request_func=None,
            db=None):
        self.bp = None
        if app is not None:
            self.init_app(
                app, blueprint_name=blueprint_name,
                blueprint_url_prefix=blueprint_url_prefix,
                before_request_func=before_request_func,
                db=db)


    def init_app(
            self, app, blueprint_name="flask_template_previewer", 
            blueprint_url_prefix="/preview",
            before_request_func=None,
            db=None):
        '''Initalizes the application with the extension.
        :param app: The Flask application object.
        '''
        self.bp = create_blueprint(
            app, blueprint_name=blueprint_name,
            blueprint_url_prefix=blueprint_url_prefix,
            before_request_func=before_request_func,
            db=db)
        app.register_blueprint(self.bp)
