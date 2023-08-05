"""This module contains plugins for controlling the Websocket RPC server
status."""
from teatime.plugins import Context, Plugin
from teatime.reporting import Issue, Severity


class GethStartWebsocket(Plugin):
    """Try to start the websocket service.

    Severity: Critical

    Geth: https://geth.ethereum.org/docs/rpc/ns-admin#admin_startws
    """

    INTRUSIVE = True

    def _check(self, context: Context) -> None:
        payload = self.get_rpc_json(context.target, method="admin_startWS")
        context.report.add_issue(
            Issue(
                title="Admin Websocket Start Rights",
                description="The RPC Websocket service can be started using the admin_startWS RPC call.",
                raw_data=payload,
                severity=Severity.CRITICAL,
            )
        )


class GethStopWebsocket(Plugin):
    """Try to stop the websocket service.

    Severity: Critical

    Geth: https://geth.ethereum.org/docs/rpc/ns-admin#admin_stopws
    """

    INTRUSIVE = True

    def _check(self, context: Context) -> None:
        payload = self.get_rpc_json(context.target, method="admin_stopWS")
        context.report.add_issue(
            Issue(
                title="Admin Websocket Stop Rights",
                description="The RPC Websocket service can be stopped using the admin_stopWS RPC call.",
                raw_data=payload,
                severity=Severity.CRITICAL,
            )
        )
