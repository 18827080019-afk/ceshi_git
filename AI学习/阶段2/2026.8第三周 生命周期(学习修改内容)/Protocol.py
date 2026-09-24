
class ProtocolValidator:
    def _error(
            self,
            code,
            field,
            message,
            response,
            recoverable=True
        ):
    
            return {
                "type":"protocol_error",
                "code":code,
                "field":field,
                "message":message,
                "recoverable":recoverable,
                "response":response
            }

    def validate(self,response):

        # response本身必须是dict
        if not isinstance(response,dict):
            return self._error(
                code="invalid_type",
                field="response",
                message="response must be dict",
                response=response
            )

        # action必须存在
        if "action" not in response:
            return self._error(
                code="missing_field",
                field="action",
                message="missing field: action",
                response=response
            )

        action = response["action"]

        # action必须是字符串
        if not isinstance(action,str):
            return self._error(
                code="invalid_type",
                field="action",
                message="action must be string",
                response=response
            )

        if action == "tool":
            return self._validate_tool(
                response
            )

        if action == "final":
            return self._validate_final(
                response
            )

        return self._error(
            code="invalid_action",
            field="action",
            message="action must be tool or final",
            response=response
        )


    def _validate_tool(self,response):

        if "tool" not in response:
            return self._error(
                code="missing_field",
                field="tool",
                message="missing field: tool",
                response=response
            )

        if not isinstance(response["tool"],str):
            return self._error(
                code="invalid_type",
                field="tool",
                message="tool must be string",
                response=response
            )

        if not response["tool"].strip():  #去除空格
            return self._error(
                code="invalid_value",
                field="tool",
                message="tool cannot be empty",
                response=response
            )

        if "args" not in response:
            return self._error(
                code="missing_field",
                field="args",
                message="missing field: args",
                response=response
            )

        if not isinstance(response["args"],dict):
            return self._error(
                code="invalid_type",
                field="args",
                message="args must be dict",
                response=response
            )

        return None


    def _validate_final(self,response):

        if "answer" not in response:
            return self._error(
                code="missing_field",
                field="answer",
                message="missing field: answer",
                response=response
            )

        if not isinstance(response["answer"],str):
            return self._error(
                code="invalid_type",
                field="answer",
                message="answer must be string",
                response=response
            )

        return None


    