import app.basic
import tornado.web
import lib.pg
import functools
import inspect

import models.courses.courses as model
import models.courses.courses_functions as model_functions

class CoursesHandler(app.basic.BaseHandler):
    pgquery = lib.pg.PGQuery(model, model_functions)
    query_arguments = inspect.getmembers(model_functions, inspect.isfunction)

    @tornado.web.asynchronous
    def get(self):
        recognized_arguments = self.valid_query_arguments(model_functions)
        queries = self.get_recognized_arguments(recognized_arguments)
        limit = self.get_int_argument("limit", 0)
        page = self.get_int_argument("page", 0)
        pretty = self.get_bool_argument("pretty", None)
        if not queries:
            return self.render('docs.html', endpoint='courses', params=self.query_arguments)
        internal_callback = functools.partial(self._finish, pretty=pretty)
        self.pgquery.execute(queries, page=page, limit=limit, callback=internal_callback)

    def _finish(self, response, pretty=None):
        if response:
            return self.api_response(response, pretty=pretty)
        else:
            return self.error(status_code=204, status_txt="NO_CONTENT_FOR_REQUEST")
