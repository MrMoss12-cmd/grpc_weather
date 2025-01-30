import grpc
import server.weather_pb2
import server.weather_pb2_grpc

def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = weather_pb2_grpc.WeatherServiceStub(channel)
        city = input("Ingrese la ciudad para consultar el clima: ").strip()
        try:
            response = stub.GetWeather(weather_pb2.WeatherRequest(city=city))
            print(f"clima en {response.city} : {response.temperature}, {response.condition}")
        except grpc.RpcError as e:
            print(f"Error:{e.details()} (Codigo: {e.code()})")

def __name__ = "__main__":
     run()