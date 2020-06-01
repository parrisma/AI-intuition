import threading
from kafka import KafkaConsumer
from journey11.src.lib.uniqueref import UniqueRef
from journey11.src.lib.protocopy import ProtoCopy
from journey11.src.lib.kpubsub.pb_notification_pb2 import PBNotification
from journey11.src.lib.kpubsub.messagetypemap import MessageTypeMap


class Kconsumer:
    def __init__(self,
                 listener,
                 topic: str,
                 server: str,
                 port: str,
                 protoc: ProtoCopy,
                 message_type_map: MessageTypeMap,
                 group: str = UniqueRef().ref):
        """
        Boot strap a Kafka listener
        :param listener: The callable object that will be passed the message as key word arg 'msg'
        :param topic:  The Topic to subscribe to
        :param server: The Kafka Server
        :param port: The Kafka Server Port
        :param protoc: The Protoc instance to handle serialise/de-serialise
        :param message_type_map: The mapping between message types and protobuf object handlers
        :param group: The Kafka group to listen as - default is a UUID
        """
        self.consumer = KafkaConsumer(bootstrap_servers='{}:{}'.format(server, port),
                                      group_id=group)
        self.consumer.subscribe([topic])
        self._stop = True
        self._listener = listener
        self._protoc = protoc
        self._message_type_map = message_type_map
        self._runner = threading.Timer(.25, self).start()
        self._stop = False
        return

    def __call__(self, *args, **kwargs):
        messages_by_partition = self.consumer.poll(timeout_ms=5, max_records=10)
        for topic, messages in messages_by_partition.items():
            for message in messages:
                wrapper_message = PBNotification()
                wrapper_message.ParseFromString(message.value)
                listener_message = self._protoc.deserialize(serialized_src=wrapper_message.payload,
                                                            target_type=self._message_type_map.get_native_type_by_uuid(
                                                                wrapper_message.type_uuid))
                self._listener(msg=listener_message)
        if not self._stop:
            self._runner = threading.Timer(.25, self).start()
        return

    def stop(self) -> None:
        self._stop = True
        return

    def __del__(self):
        self.stop()
        runner = getattr(self, "_runner", None)
        if runner is not None:
            del runner
        return
