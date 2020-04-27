from flask import Blueprint, render_template, request
import os
import re


def render_file_index_template(index_template, index_path):
    return render_template(
        index_template,
        ui_mocks=sorted(
            map(
                lambda page:
                page.rpartition(".")[0],
                os.listdir(index_path))))


def create_blueprint(
        app,
        blueprint_name="flask_template_previewer", 
        blueprint_url_prefix="/preview",
        before_request_func=None,
        db=None):
    bp = Blueprint(
        blueprint_name, __name__,
        url_prefix=blueprint_url_prefix,
        template_folder="templates")

    if before_request_func:
        bp.before_request(before_request_func)

    @bp.route(
        '/<path:template_path>',
        methods=['GET'],
        endpoint='show_template')
    def show_template(template_path):
        template_path = template_path.replace("-", "_")
        full_path = app.root_path + "/templates/" + template_path
        template_args = {}
        for arg, v in request.args.items():
            match = re.match(r'models\.(?P<model_name>\w+)\.(?P<model_id>\d+)', v)
            if match and db is not None:
                model_name = match.group('model_name')
                model_id = int(match.group('model_id'))
                model_obj = db.session.query(
                    db.Model._decl_class_registry[model_name]).get(model_id)
                template_args[arg] = model_obj
            else:
                template_args[arg] = v
        if os.path.isdir(full_path):
            return render_file_index_template(full_path)
        if template_path.endswith(".html"):
            return render_template(template_path, **template_args)
        return render_template(
            "{}.html".format(template_path), **template_args)

    return bp
