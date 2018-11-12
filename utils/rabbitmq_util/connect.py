
import pika


credentials = pika.PlainCredentials("root", "123456")
connect = pika.BlockingConnection(pika.ConnectionParameters(host="localhost", port="5672",
                                                            virtual_host="/", credentials=credentials))

channel = connect.channel()