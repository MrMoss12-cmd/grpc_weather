import grpc
import json
from concurrent import futures
import weather_pb2
import weather_pb2_grpc

class WeatherService(weather_pb2_grpc.WeatherServiceServicer):
    def __init__(self):
        with open("data.json", "r") as f:
            self.weather_data = json.load(f)

    def GetWeather(self, request, context):
        city = request.city.lower()
        if city in self.weather_data:
            data = self.weather_data[city]
            return weather_pb2.WeatherResponse(
                city=request.city,
                temperature=data["temperature"],
                condition=data["condition"]
            )
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Ciudad no encontrada")
            return weather_pb2.WeatherResponse()

def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    weather_pb2_grpc.add_WeatherServiceServicer_to_server(WeatherService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Servidor gRPC ejecutandose en el puerto 50051...")
    server.wait_for_termination()

if __name__ == "__name__":
    server()

