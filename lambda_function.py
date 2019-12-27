#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:Lijiacai
Email:1050518702@qq.com
===========================================
CopyRight@JackLee.com
===========================================
"""

import os
import sys
import json
import logging
from flask import Flask, jsonify
from flask_cors import CORS
from flask import request
from flask_graphql import GraphQLView

try:
    reload(sys)
    sys.setdefaultencoding("utf8")
except:
    pass
from controller.schema import schema


def lambda_handler(event, context):
    # TODO implement
    operationName = event.get("operationName")
    query = event.get("query")
    if not query:
        return {
            "statusCode": 200,
            "body": json.dumps({"errors": [{"message": "请给query参数"}]})}
    variables = event.get("variables")
    headers = event.get("headers", {})
    result = schema.execute(query, variables=variables, context={"headers": headers})
    if result.errors:
        logging.exception(str(result.errors))
        errors_list = []
        for error in result.errors:
            if "Cannot query field" in str(error.message):
                message = "字段错误"
            # todo: 这里新增错误类型
            else:
                message = str(error.message)
            try:
                stack = str(error.stack) + "-" + str(error.message) + "-" + str(error.locations)
            except:
                stack = str(error.message)
            errors_list.append(
                {"message": message, "stack": stack})
        body = {"errors": errors_list}
    else:
        body = {"data": result.data}
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }
    return response


def flask_handler():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)

    @app.route("/graphql_api", methods=["POST"])
    def api():
        event = request.data.decode("utf8")
        event = json.loads(event)
        event["headers"] = request.headers
        return jsonify(json.loads(lambda_handler(event, None).get("body")))

    app.add_url_rule('/graphql_doc_ui', view_func=GraphQLView.as_view('graphql',
                                                               schema=schema, graphiql=True))

    return app


app = flask_handler()

if __name__ == '__main__':
    app.run(port=4901, debug=True, host="0.0.0.0")
