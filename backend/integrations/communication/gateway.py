# backend/integrations/communication/gateway.py

"""
Communication Gateway
---------------------
Single controlled entry/exit point between ChetnaOS core
and external communication channels (API, chat, agents, future robotics).
"""

from typing import Dict, Any
from datetime import datetime


class CommunicationGateway:
    def _init_(self):
        self.channel_status = {
            "api": True,
            "chat": True,
            "agent": True,
            "robotics": False  # future
        }
        self.logs = []

    # ---------- INTERNAL ----------
    def _log(self, direction: str, channel: str, payload: Dict[str, Any]):
        self.logs.append({
            "time": datetime.utcnow().isoformat(),
            "direction": direction,
            "channel": channel,
            "payload": payload
        })

    # ---------- INBOUND ----------
    def receive(self, channel: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        External → ChetnaOS
        """
        if not self.channel_status.get(channel, False):
            return {
                "status": "blocked",
                "reason": f"Channel '{channel}' disabled"
            }

        self._log("inbound", channel, payload)

        return {
            "status": "received",
            "channel": channel,
            "data": payload
        }

    # ---------- OUTBOUND ----------
    def send(self, channel: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        ChetnaOS → External
        """
        if not self.channel_status.get(channel, False):
            return {
                "status": "blocked",
                "reason": f"Channel '{channel}' disabled"
            }

        self._log("outbound", channel, payload)

        return {
            "status": "sent",
            "channel": channel,
            "data": payload
        }

    # ---------- CONTROL ----------
    def enable_channel(self, channel: str):
        self.channel_status[channel] = True

    def disable_channel(self, channel: str):
        self.channel_status[channel] = False

    def get_logs(self):
        return self.logs
